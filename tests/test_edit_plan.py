"""Immutable edit planning uses exact original bytes and no filesystem IO."""

import hashlib
import json
import tempfile
import unittest
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
from unittest.mock import patch

from gz_mcp_lsp.config import Config, Limits
from gz_mcp_lsp.models import AdapterError, Json, Position, Range, TextEdit
from gz_mcp_lsp.workspace import Workspace


class EditPlanTests(unittest.TestCase):
    """A preview token identifies content; it is never a consent flag."""

    def setUp(self):
        try:
            from gz_mcp_lsp.edit_plan import plan_edits, plan_workspace_edit
        except ImportError as error:
            self.fail(f"Pure edit planning absent: {error}")
        self.plan_edits = plan_edits
        self.plan_workspace_edit = plan_workspace_edit
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.source = self.root / "a.py"
        self.source.write_bytes(b"abcdef\n")
        self.workspace = Workspace(Config(self.root, self.source))
        self.snapshot = self.workspace.read(self.source.as_uri())
        self.uri = self.source.as_uri()

    @staticmethod
    def edit(start, end, text):
        return TextEdit(Range(Position(*start), Position(*end)), text)

    def test_edits_use_original_snapshot(self):
        """An early length-changing replacement never shifts a later original range."""
        edits = [self.edit((0, 1), (0, 3), "LONG"), self.edit((0, 4), (0, 6), "X")]
        self.assertEqual(self.plan_edits(self.snapshot, edits), b"aLONGdX\n")

    def test_adjacent_legal_overlap_rejected(self):
        """End-exclusive adjacency is legal; overlap and coincident inserts are conflicts."""
        self.assertEqual(
            self.plan_edits(
                self.snapshot, [self.edit((0, 0), (0, 2), "A"), self.edit((0, 2), (0, 4), "B")]
            ),
            b"ABef\n",
        )
        for edits in (
            [self.edit((0, 1), (0, 4), ""), self.edit((0, 3), (0, 5), "")],
            [self.edit((0, 2), (0, 2), "x"), self.edit((0, 2), (0, 2), "y")],
        ):
            with self.assertRaises(AdapterError) as raised:
                self.plan_edits(self.snapshot, edits)
            self.assertEqual(raised.exception.code, "CONFLICT")

    def test_duplicate_aliases_rejected(self):
        """Two spellings of one physical target cannot become two transaction entries."""
        alias = self.uri.replace("/a.py", "/%61.py")
        edit: Json = {
            "range": {"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 1}},
            "newText": "x",
        }
        with self.assertRaises(AdapterError) as raised:
            self.plan_workspace_edit(
                {"changes": {self.uri: [edit], alias: [edit]}},
                {self.uri: self.snapshot, alias: self.snapshot},
                "generation",
            )
        self.assertEqual(raised.exception.code, "CONFLICT")

    def test_utf16_crlf_eof_bytes(self):
        """Emoji ranges, mixed delimiters, inserts and explicit EOF preserve all other bytes."""
        self.source.write_bytes("a😀b\r\n".encode())
        snapshot = self.workspace.read(self.uri)
        edits = [self.edit((0, 1), (0, 3), "x")]
        self.assertEqual(self.plan_edits(snapshot, edits), b"axb\r\n")
        cases = json.loads(
            (Path(__file__).parent / "fixtures/edit_cases.json").read_text(encoding="utf-8")
        )
        for case in cases:
            self.source.write_bytes(case["before"].encode("utf-8"))
            snapshot = self.workspace.read(self.uri)
            edits = [self.edit(item["start"], item["end"], item["text"]) for item in case["edits"]]
            self.assertEqual(
                self.plan_edits(snapshot, edits), case["after"].encode("utf-8"), case["name"]
            )

    def test_resource_op_rejects_entire_edit(self):
        """One create/rename/delete operation invalidates the entire mixed WorkspaceEdit."""
        for kind in ("create", "rename", "delete"):
            document: Json = {"textDocument": {"uri": self.uri, "version": 1}, "edits": []}
            with self.assertRaises(AdapterError) as raised:
                self.plan_workspace_edit(
                    {"documentChanges": [document, {"kind": kind, "uri": self.uri}]},
                    {self.uri: self.snapshot},
                    "generation",
                )
            self.assertEqual(raised.exception.code, "UNSUPPORTED")
        with self.assertRaises(AdapterError):
            self.plan_workspace_edit(
                {"changes": {}, "documentChanges": []}, {self.uri: self.snapshot}, "generation"
            )

    def test_versions_and_digest(self):
        """Versions, preimages, exact edits and confirmation labels are bound to identity."""

        def request(version=1, label="Rename") -> Json:
            return {
                "documentChanges": [
                    {
                        "textDocument": {"uri": self.uri, "version": version},
                        "edits": [
                            {
                                "range": {
                                    "start": {"line": 0, "character": 0},
                                    "end": {"line": 0, "character": 1},
                                },
                                "newText": "x",
                                "annotationId": "confirm",
                            }
                        ],
                    }
                ],
                "changeAnnotations": {"confirm": {"label": label, "needsConfirmation": True}},
            }

        first = self.plan_workspace_edit(
            request(), {self.uri: self.snapshot}, "generation", expires_at=9999999999
        )
        same = self.plan_workspace_edit(
            request(), {self.uri: self.snapshot}, "generation", expires_at=9999999999
        )
        other = self.plan_workspace_edit(
            request(label="Different"),
            {self.uri: self.snapshot},
            "generation",
            expires_at=9999999999,
        )
        self.assertEqual(first.plan_id, same.plan_id)
        self.assertNotEqual(first.plan_id, other.plan_id)
        versioned = self.plan_workspace_edit(
            request(version=2),
            {self.uri: replace(self.snapshot, version=2)},
            "generation",
            expires_at=9999999999,
        )
        later = self.plan_workspace_edit(
            request(), {self.uri: self.snapshot}, "generation", expires_at=10000000000
        )
        self.assertNotEqual(first.plan_id, versioned.plan_id)
        self.assertNotEqual(first.plan_id, later.plan_id)
        from gz_mcp_lsp.edit_plan import plan_digest

        changed_after = replace(first, files=(replace(first.files[0], after=b"different\n"),))
        self.assertNotEqual(first.plan_id, plan_digest(changed_after))
        changed_before = replace(
            first,
            files=(
                replace(first.files[0], before=replace(first.files[0].before, data=b"forged\n")),
            ),
        )
        self.assertNotEqual(first.plan_id, plan_digest(changed_before))
        self.assertTrue(first.annotations[0].needs_confirmation)
        self.assertEqual(first.files[0].before.sha256, hashlib.sha256(b"abcdef\n").hexdigest())
        self.assertEqual(first.files[0].after, b"xbcdef\n")
        with self.assertRaises(AdapterError) as raised:
            self.plan_workspace_edit(request(version=2), {self.uri: self.snapshot}, "generation")
        self.assertEqual(raised.exception.code, "CONFLICT")
        with self.assertRaises(FrozenInstanceError):
            first.__setattr__("generation", "changed")
        with self.assertRaises(AdapterError):
            self.plan_workspace_edit(
                request(), {self.uri: replace(self.snapshot, sha256="0" * 64)}, "generation"
            )

    def test_zero_write_and_no_filesystem_read(self):
        """Planning receives immutable snapshots; even metadata lookups are forbidden."""
        before_hashes = {self.uri: hashlib.sha256(self.source.read_bytes()).hexdigest()}
        request: Json = {
            "changes": {
                self.uri: [
                    {
                        "range": {
                            "start": {"line": 0, "character": 1},
                            "end": {"line": 0, "character": 2},
                        },
                        "newText": "",
                    }
                ]
            }
        }
        with (
            patch("builtins.open", side_effect=AssertionError("Unexpected IO")),
            patch("os.open", side_effect=AssertionError("Unexpected IO")),
            patch.object(Path, "stat", side_effect=AssertionError("Unexpected IO")),
        ):
            plan = self.plan_workspace_edit(request, {self.uri: self.snapshot}, "generation")
        after_preview_hashes = {self.uri: hashlib.sha256(self.source.read_bytes()).hexdigest()}
        self.assertEqual(before_hashes, after_preview_hashes)
        self.assertEqual(plan.files[0].after, b"acdef\n")

    def test_limits_and_no_op(self):
        """Count/byte ceilings fail visibly; identical saved bytes remain a truthful no-op."""
        with self.assertRaises(AdapterError) as raised:
            self.plan_edits(
                self.snapshot, [self.edit((0, 0), (0, 0), "x" * 20)], limits=Limits(file_bytes=8)
            )
        self.assertEqual(raised.exception.code, "LIMIT_EXCEEDED")
        plan = self.plan_workspace_edit(
            {"changes": {self.uri: []}}, {self.uri: self.snapshot}, "generation"
        )
        self.assertTrue(plan.no_op)
