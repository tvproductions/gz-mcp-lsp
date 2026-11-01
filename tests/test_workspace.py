"""Exercise workspace identity, byte snapshots and UTF-16 coordinates."""

import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from typing import cast


class WorkspaceTests(unittest.TestCase):
    """Use real disposable files without importing or running workspace code."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name).resolve()
        self.root = self.directory / "workspace"
        self.root.mkdir()
        self.source = self.root / "sample.py"
        self.source.write_bytes("a\U0001f600b\r\nsecond\n".encode())

    def workspace(self, **changes):
        """Construct the workspace through its public configuration boundary."""
        try:
            from gz_mcp_lsp.config import load_config
            from gz_mcp_lsp.workspace import Workspace
        except ImportError as error:
            self.fail(f"Workspace behavior is not implemented: {error}")
        data = {
            "schema_version": 1,
            "workspace_root": str(self.root),
            "ty_executable": sys.executable,
        }
        data.update(changes)
        settings = self.directory / "settings.json"
        settings.write_text(json.dumps(data), encoding="utf-8")
        return Workspace(load_config(settings))

    def test_utf16_offsets(self):
        """Non-BMP characters occupy two code units and four UTF-8 bytes."""
        workspace = self.workspace()
        from gz_mcp_lsp.models import AdapterError, Position

        snapshot = workspace.read(self.source.as_uri())
        self.assertEqual(workspace.offset(snapshot, Position(0, 3)), 5)
        self.assertEqual(workspace.offset(snapshot, Position(1, 0)), 8)
        with self.assertRaises(AdapterError):
            workspace.offset(snapshot, Position(0, 2))
        for line, character in [(0, 5), (3, 0), (1, 7)]:
            with self.subTest(position=(line, character)), self.assertRaises(AdapterError):
                workspace.offset(snapshot, Position(line, character))

    def test_positions_reject_bool_float_and_negative(self):
        """No Python bool-as-int or coercion enters semantic coordinates."""
        self.workspace()
        from gz_mcp_lsp.models import AdapterError, Position, Range

        for value in [True, 1.0, -1, "1"]:
            with self.subTest(value=value), self.assertRaises(AdapterError):
                Position(cast("int", value), 0)
        with self.assertRaises(AdapterError):
            Range(Position(1, 0), Position(0, 1))

    def test_newlines_and_eof_are_exact(self):
        """CR, LF and CRLF are line delimiters; vertical tab is source text."""
        workspace = self.workspace()
        from gz_mcp_lsp.models import Position

        self.source.write_bytes(b"a\rb\r\nc\nd\v")
        snapshot = workspace.read(self.source.as_uri())
        for line, offset in [(0, 0), (1, 2), (2, 5), (3, 7)]:
            self.assertEqual(workspace.offset(snapshot, Position(line, 0)), offset)
        self.assertEqual(workspace.offset(snapshot, Position(3, 2)), 9)
        self.source.write_bytes(b"tail\n")
        self.assertEqual(workspace.offset(workspace.read(self.source.as_uri()), Position(1, 0)), 5)
        self.source.write_bytes(b"")
        self.assertEqual(workspace.offset(workspace.read(self.source.as_uri()), Position(0, 0)), 0)

    def test_uri_containment_aliases(self):
        """Aliases retain original URIs but share canonical file identity."""
        workspace = self.workspace()
        from gz_mcp_lsp.models import AdapterError

        unicode_path = self.root / "name space-\u00e9.py"
        unicode_path.write_bytes(b"pass\n")
        uri = unicode_path.as_uri()
        alias = uri.replace("name", "%6eame")
        first, second = workspace.read(uri), workspace.read(alias)
        self.assertEqual(first.identity, second.identity)
        self.assertEqual(workspace.canonical_uri(uri), unicode_path.resolve().as_uri())
        self.assertEqual(second.uri, alias)
        self.assertEqual(workspace.canonical_uri(alias), workspace.canonical_uri(uri))
        outside = self.directory / "workspace-decoy" / "sample.py"
        outside.parent.mkdir()
        outside.write_bytes(b"secret\n")
        for denied in [
            outside.as_uri(),
            self.root.as_uri() + "/../outside.py",
            self.root.as_uri() + "/%2e%2e/outside.py",
            uri + "?query",
            uri + "#fragment",
            uri + "?",
            uri + "#",
            uri.replace("file:///", "file://localhost/"),
            uri + "%ZZ",
            self.root.as_uri() + "/%00.py",
        ]:
            with self.subTest(uri=denied), self.assertRaises(AdapterError):
                workspace.read(denied)

    def test_symlink_and_nonregular_sources_are_denied(self):
        """Sources cannot escape through links or resolve to directories."""
        workspace = self.workspace()
        from gz_mcp_lsp.models import AdapterError

        with self.assertRaises(AdapterError):
            workspace.read(self.root.as_uri())
        link = self.root / "linked.py"
        try:
            link.symlink_to(self.source)
        except OSError:
            self.skipTest("Host lacks symlink creation permission; link rejection is unverified")
        with self.assertRaises(AdapterError):
            workspace.read(link.as_uri())
        with self.assertRaises(AdapterError):
            workspace.manifest()

    def test_manifest_hashes_unopened_bytes_and_scope(self):
        """Byte changes invalidate even with restored timestamps; exclusions are explicit."""
        workspace = self.workspace()
        before = workspace.manifest()
        stat = self.source.stat()
        original = self.source.read_bytes()
        self.source.write_bytes(original.replace(b"second", b"change"))
        os.utime(self.source, ns=(stat.st_atime_ns, stat.st_mtime_ns))
        self.assertNotEqual(workspace.manifest(), before)
        excluded = self.root / ".venv"
        excluded.mkdir()
        (excluded / "hidden.py").write_bytes(b"ignored")
        stable = workspace.manifest()
        (excluded / "hidden.py").write_bytes(b"different")
        self.assertEqual(workspace.manifest(), stable)
        (self.root / "new.py").write_bytes(b"pass\n")
        self.assertNotEqual(workspace.manifest(), stable)

    def test_limits_and_utf8_fail_visibly(self):
        """Oversized, overpopulated and non-UTF8 inputs do not become empty success."""
        workspace = self.workspace(limits={"file_bytes": 4})
        from gz_mcp_lsp.models import AdapterError

        with self.assertRaises(AdapterError) as caught:
            workspace.read(self.source.as_uri())
        self.assertEqual(caught.exception.code, "LIMIT_EXCEEDED")
        self.source.write_bytes(b"\xff")
        workspace = self.workspace()
        with self.assertRaises(AdapterError):
            workspace.read(self.source.as_uri())
        (self.root / "extra.py").write_bytes(b"pass")
        with self.assertRaises(AdapterError):
            self.workspace(limits={"workspace_files": 1}).manifest()

    def test_snapshot_is_exact_and_excluded_sources_are_denied(self):
        """Byte hashes/identity accompany the original input URI and version."""
        workspace = self.workspace()
        from gz_mcp_lsp.models import AdapterError

        snapshot = workspace.read(self.source.as_uri())
        self.assertEqual(snapshot.data, self.source.read_bytes())
        self.assertEqual(snapshot.sha256, hashlib.sha256(snapshot.data).hexdigest())
        self.assertEqual(snapshot.version, 1)
        excluded = self.root / ".git"
        excluded.mkdir()
        forbidden = excluded / "internal.py"
        forbidden.write_bytes(b"pass")
        with self.assertRaises(AdapterError):
            workspace.read(forbidden.as_uri())
