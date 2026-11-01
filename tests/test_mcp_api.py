"""Actual SDK composition, strict raw arguments and production hover results."""

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast
from unittest.mock import AsyncMock

from mcp import types
from mcp.client import Client
from mcp.server.context import ServerRequestContext

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.session import Session
from tests.test_documents import FakeSession


class StubSession(FakeSession):
    """Observe lifecycle without changing production semantic registration."""

    def __init__(self):
        super().__init__()
        self.entered = self.closed = False
        self.capabilities["hoverProvider"] = True

    async def __aenter__(self):
        self.entered = True
        return self

    async def __aexit__(self, *args):
        self.closed = True


class MCPCompositionTests(unittest.IsolatedAsyncioTestCase):
    """The SDK exposes only the implemented production tool."""

    async def test_malformed_tool_name_delegates_to_sdk_validation(self):
        """Product middleware leaves malformed protocol envelopes to the SDK."""
        from gz_mcp_lsp.mcp_api import _strict_arguments

        context = cast(
            "ServerRequestContext", SimpleNamespace(method="tools/call", params={"name": []})
        )
        next_handler = AsyncMock(return_value=types.CallToolResult(content=[]))
        await _strict_arguments(context, next_handler)
        next_handler.assert_awaited_once_with(context)

    async def test_lifespan_schema_hover_and_strict_raw_arguments(self):
        """Typed SDK result includes equivalent JSON text; coercions are rejected."""
        from gz_mcp_lsp.mcp_api import create_server

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            source = root / "main.py"
            source.write_bytes(b"answer = 42\n")
            session = StubSession()
            session.rpc.release.set()
            server = create_server(Config(root, source), cast("Session", session))
            async with Client(server) as client:
                self.assertTrue(session.entered)
                tools = (await client.list_tools()).tools
                self.assertEqual(
                    sorted(tool.name for tool in tools),
                    [
                        "definition",
                        "diagnostics",
                        "document_symbols",
                        "edit_file",
                        "hover",
                        "implementations",
                        "references",
                        "rename_symbol",
                        "workspace_symbols",
                    ],
                )
                assert tools[0].annotations is not None
                self.assertTrue(tools[0].annotations.read_only_hint)
                self.assertIsNotNone(tools[0].output_schema)
                result = await client.call_tool(
                    "hover",
                    {
                        "uri": source.as_uri(),
                        "position": {"line": 0, "character": 2},
                    },
                )
                self.assertFalse(result.is_error)
                self.assertEqual(result.structured_content["operation"], "hover")
                assert isinstance(result.content[0], types.TextContent)
                self.assertEqual(json.loads(result.content[0].text), result.structured_content)
                before = len(session.rpc.notifications)
                for invalid in (
                    {"line": True, "character": 0},
                    {"line": "0", "character": 0},
                    {"line": 0.0, "character": 0},
                    '{"line":0,"character":0}',
                    {"line": 0, "character": 0, "extra": 1},
                ):
                    result = await client.call_tool(
                        "hover", {"uri": source.as_uri(), "position": invalid}
                    )
                    self.assertTrue(result.is_error)
                    self.assertEqual(result.structured_content["error"]["code"], "INVALID_INPUT")
                self.assertEqual(len(session.rpc.notifications), before)
                for name, extra in (
                    ("definition", {"context_lines": True}),
                    ("definition", {"context_lines": 21}),
                    ("references", {"include_declaration": "true"}),
                ):
                    result = await client.call_tool(
                        name,
                        {
                            "uri": source.as_uri(),
                            "position": {"line": 0, "character": 2},
                            **extra,
                        },
                    )
                    self.assertTrue(result.is_error)
                    self.assertEqual(result.structured_content["error"]["code"], "INVALID_INPUT")
                result = await client.call_tool(
                    "diagnostics",
                    {
                        "uri": source.as_uri(),
                        "context_lines": True,
                    },
                )
                self.assertTrue(result.is_error)
                self.assertEqual(result.structured_content["error"]["code"], "INVALID_INPUT")
                result = await client.call_tool("diagnostics", {"uri": source.as_uri()})
                self.assertTrue(result.is_error)
                self.assertEqual(result.structured_content["error"]["code"], "UNSUPPORTED")
            self.assertTrue(session.closed)


class MutationLifecycleTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        import asyncio
        import threading
        from dataclasses import replace
        from unittest.mock import patch

        from tests.test_mutations import MemoryTransactions

        temporary = tempfile.TemporaryDirectory(prefix="gz-start-unit-", dir=Path.home())
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name).resolve()
        self.root = self.base / "workspace"
        self.root.mkdir()
        self.source = self.root / "a.py"
        self.source.write_bytes(b"value = 1\n")
        self.session = StubSession()
        self.tx: Any = MemoryTransactions()
        self.config = Config(
            self.root,
            self.source,
            mutations_enabled=True,
            writable_roots=(self.root,),
            state_directory=self.base / "state",
        )
        self.replace = replace
        self.platform = patch("gz_mcp_lsp.mutations.write_platform_supported", return_value=True)
        self.platform_mock = self.platform.start()
        self.addCleanup(self.platform.stop)
        self.factory = patch("gz_mcp_lsp.mcp_api.Transactions", return_value=self.tx, create=True)
        self.factory.start()
        self.addCleanup(self.factory.stop)
        self.started = threading.Event()
        self.release = threading.Event()
        self.addCleanup(self.release.set)
        self.entered = asyncio.Event()

    def server(self, config=None):
        from gz_mcp_lsp.mcp_api import create_server

        return create_server(config or self.config, cast("Session", self.session))

    async def test_lifespan_recovers_before_mutation_admission(self):
        import asyncio

        from tests.test_mutations import until

        def recover():
            self.started.set()
            if not self.release.wait(10):
                raise AssertionError("Recovery barrier timeout")
            return []

        self.tx.recover = recover

        async def connect():
            async with Client(self.server()):
                self.entered.set()

        pending = asyncio.create_task(connect())
        await until(self.started.is_set)
        self.assertFalse(self.entered.is_set())
        self.assertFalse(self.session.entered)
        self.release.set()
        await pending
        self.assertTrue(self.entered.is_set())

    async def test_recovery_lockout_rejects_all_mutations(self):
        self.tx.recovery = [{"status": "recovery_required"}]
        async with Client(self.server()) as client:
            for name, arguments in (
                (
                    "rename_symbol",
                    {
                        "action": "preview",
                        "uri": self.source.as_uri(),
                        "position": {"line": 0, "character": 0},
                        "new_name": "renamed",
                    },
                ),
                (
                    "edit_file",
                    {
                        "action": "preview",
                        "uri": self.source.as_uri(),
                        "edits": [],
                        "expected_hash": "0" * 64,
                    },
                ),
                ("edit_file", {"action": "apply", "plan_id": "0" * 64}),
                ("rename_symbol", {"action": "apply", "plan_id": "0" * 64}),
            ):
                result = await client.call_tool(name, arguments)
                self.assertTrue(result.is_error)
                self.assertEqual(result.structured_content["error"]["code"], "RECOVERY_REQUIRED")
        self.assertEqual(self.source.read_bytes(), b"value = 1\n")
        self.assertNotIn("apply", self.tx.calls)

    async def test_disabled_or_unsupported_startup_never_restores_source(self):
        for disabled in (True, False):
            self.tx.calls.clear()
            self.platform_mock.return_value = disabled
            config = self.replace(self.config, mutations_enabled=not disabled)
            async with Client(self.server(config)) as client:
                result = await client.call_tool(
                    "edit_file", {"action": "apply", "plan_id": "0" * 64}
                )
                self.assertTrue(result.is_error)
                self.assertEqual(
                    result.structured_content["error"]["code"],
                    "MUTATIONS_DISABLED" if disabled else "UNSUPPORTED",
                )
            self.assertNotIn("recover", self.tx.calls)
            self.assertEqual(self.source.read_bytes(), b"value = 1\n")

    async def test_mutation_annotations_and_mutually_exclusive_raw_fields(self):
        async with Client(self.server()) as client:
            tools = {tool.name: tool for tool in (await client.list_tools()).tools}
            for name in ("edit_file", "rename_symbol"):
                annotations = tools[name].annotations
                assert annotations is not None
                self.assertFalse(annotations.read_only_hint)
                self.assertTrue(annotations.destructive_hint)
                self.assertFalse(annotations.open_world_hint)
                for arguments in (
                    {"action": "apply", "plan_id": "0" * 64, "approved": True},
                    {"action": "apply", "plan_id": "0" * 64, "uri": self.source.as_uri()},
                    {"action": "preview", "uri": self.source.as_uri()},
                ):
                    result = await client.call_tool(name, arguments)
                    self.assertTrue(result.is_error)
                    self.assertEqual(result.structured_content["error"]["code"], "INVALID_INPUT")
            for position in ({"line": True, "character": 0}, {"line": "0", "character": 0}):
                result = await client.call_tool(
                    "rename_symbol",
                    {
                        "action": "preview",
                        "uri": self.source.as_uri(),
                        "position": position,
                        "new_name": "renamed",
                    },
                )
                self.assertEqual(result.structured_content["error"]["code"], "INVALID_INPUT")
        self.assertNotIn("apply", self.tx.calls)

    async def test_recovery_exception_is_lockout_not_empty_success(self):
        from gz_mcp_lsp.models import AdapterError

        self.tx.error = AdapterError("RECOVERY_REQUIRED", "Corrupt private state")
        async with Client(self.server()) as client:
            result = await client.call_tool("edit_file", {"action": "apply", "plan_id": "0" * 64})
            self.assertEqual(result.structured_content["error"]["code"], "RECOVERY_REQUIRED")

    async def test_cancel_pending_recovery_releases_owner_and_restart_is_safe(self):
        import asyncio

        from tests.test_mutations import until

        def recover():
            self.started.set()
            if not self.release.wait(10):
                raise AssertionError("Recovery barrier timeout")
            return []

        self.tx.recover = recover

        async def connect():
            async with Client(self.server()):
                self.entered.set()

        pending = asyncio.create_task(connect())
        await until(self.started.is_set)
        pending.cancel()
        await asyncio.sleep(0)
        self.assertFalse(self.session.entered)
        self.release.set()
        with self.assertRaises(asyncio.CancelledError):
            await pending
        self.assertFalse(self.session.entered)
        async with Client(self.server()):
            self.assertTrue(self.session.entered)
        self.assertEqual(self.source.read_bytes(), b"value = 1\n")

    async def test_sdk_cancelled_apply_retains_receipt_and_does_not_reapply(self):
        import asyncio
        import hashlib

        from tests.test_mutations import until

        self.tx.paths = {self.source.as_uri(): self.source}
        async with Client(self.server()) as client:
            preview = await client.call_tool(
                "edit_file",
                {
                    "action": "preview",
                    "uri": self.source.as_uri(),
                    "expected_hash": hashlib.sha256(self.source.read_bytes()).hexdigest(),
                    "edits": [
                        {
                            "range": {
                                "start": {"line": 0, "character": 8},
                                "end": {"line": 0, "character": 9},
                            },
                            "new_text": "9",
                        }
                    ],
                },
            )
            self.assertFalse(preview.is_error, preview.content)
            plan_id = preview.structured_content["result"]["plan_id"]
            self.tx.release.clear()
            self.addCleanup(self.tx.release.set)
            pending = asyncio.create_task(
                client.call_tool("edit_file", {"action": "apply", "plan_id": plan_id})
            )
            await until(self.tx.started.is_set)
            pending.cancel()
            await asyncio.sleep(0)
            self.tx.release.set()
            with self.assertRaises(asyncio.CancelledError):
                await pending
            await until(lambda: plan_id in self.tx.receipts)
            retry = await client.call_tool("edit_file", {"action": "apply", "plan_id": plan_id})
            self.assertFalse(retry.is_error, retry.content)
            self.assertEqual(retry.structured_content["result"], self.tx.receipts[plan_id])
            self.assertEqual(self.tx.calls.count("apply"), 1)
            self.assertEqual(self.source.read_bytes(), b"value = 9\n")
