"""Required actual-ty integration: missing ty fails rather than skipping acceptance."""

import asyncio
import shutil
import tempfile
import unittest
from pathlib import Path

from gz_mcp_lsp.config import Config
from gz_mcp_lsp.documents import Documents
from gz_mcp_lsp.session import Session
from gz_mcp_lsp.workspace import Workspace

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "semantic_workspace"


class TyFixture(unittest.IsolatedAsyncioTestCase):
    """A fresh real server sees saved workspace changes without readiness sleeps."""

    async def asyncSetUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = (Path(self.temporary.name) / "workspace").resolve()
        shutil.copytree(FIXTURE, self.root)
        ty = shutil.which("ty")
        self.assertIsNotNone(ty, "Actual pinned ty is required for integration acceptance")
        assert ty is not None
        self.config = Config(self.root, Path(ty))


class InteroperabilityTests(TyFixture):
    """Observe real semantic requests after bounded generation transitions."""

    async def test_real_ty_initialization_hover_and_definition(self):
        uri = (self.root / "sample" / "runtime.py").as_uri()
        async with Session(self.config) as session:
            docs = Documents(Workspace(self.config), session)
            async with docs.query(uri):
                hover = await session.rpc.request(
                    "textDocument/hover",
                    {"textDocument": {"uri": uri}, "position": {"line": 3, "character": 4}},
                    timeout=10,
                )
                self.assertIn("run_configured_cli", str(hover))
                self.assertIn("str", str(hover))
            consumer = (self.root / "sample" / "rotation.py").as_uri()
            async with docs.query(consumer):
                definition = await session.rpc.request(
                    "textDocument/definition",
                    {"textDocument": {"uri": consumer}, "position": {"line": 2, "character": 10}},
                    timeout=10,
                )
                self.assertIn("runtime.py", str(definition))
            await docs.close()

    async def test_unopened_changes_and_configuration_restart_real_server(self):
        target = self.root / "sample" / "runtime.py"
        dependency = self.root / "sample" / "extra.py"
        async with Session(self.config) as session:
            docs = Documents(Workspace(self.config), session)
            async with docs.query(target.as_uri()):
                pass
            actions = [
                lambda: dependency.write_text(
                    'from sample.runtime import run_configured_cli\nvalue = run_configured_cli("extra")\n'
                ),
                lambda: dependency.write_text("value = 1\n"),
                lambda: dependency.rename(self.root / "sample" / "renamed.py"),
                lambda: (self.root / "sample" / "renamed.py").unlink(),
                lambda: (self.root / "ty.toml").write_text(
                    '[rules]\nunused-ignore-comment = "warn"\n'
                ),
            ]
            for action in actions:
                old_generation = session.generation
                previous = session.process
                assert previous is not None
                await asyncio.to_thread(action)
                async with docs.query(target.as_uri()):
                    self.assertNotEqual(session.generation, old_generation)
                    self.assertIsNotNone(previous.returncode)
                    hover = await session.rpc.request(
                        "textDocument/hover",
                        {
                            "textDocument": {"uri": target.as_uri()},
                            "position": {"line": 3, "character": 4},
                        },
                        timeout=10,
                    )
                    self.assertIn("run_configured_cli", str(hover))
                    refs = await session.rpc.request(
                        "textDocument/references",
                        {
                            "textDocument": {"uri": target.as_uri()},
                            "position": {"line": 3, "character": 4},
                            "context": {"includeDeclaration": False},
                        },
                        timeout=10,
                    )
                    assert isinstance(refs, list)
                    observed = {Path(item["uri"]).name for item in refs}
                    expected = {"rotation.py", "inventory.py", "registration.py"}
                    if dependency.exists() and "run_configured_cli" in dependency.read_text():
                        expected.add("extra.py")
                    self.assertEqual(observed, expected)
            await docs.close()
