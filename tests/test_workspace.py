"""Workspace reads and UTF-16 coordinates must describe the same exact bytes."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import cast

from gz_mcp_lsp.config import load_config
from gz_mcp_lsp.models import AdapterError, Position
from gz_mcp_lsp.workspace import Workspace


class WorkspaceTests(unittest.TestCase):
    """Catch boundary escapes, stale snapshots and Unicode offset corruption."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.source = self.root / "space 😀.py"
        self.source.write_bytes("a😀b\r\nnext\n".encode())
        self.settings = self.root / "settings.json"
        self.settings.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "workspace_root": str(self.root),
                    "ty_executable": "/usr/bin/true",
                }
            )
        )
        self.workspace = Workspace(load_config(self.settings))

    def test_utf16_offsets(self):
        snapshot = self.workspace.read(self.source.as_uri())
        self.assertEqual(self.workspace.offset(snapshot, Position(0, 3)), 5)
        self.assertEqual(self.workspace.offset(snapshot, Position(1, 0)), 8)
        self.assertEqual(self.workspace.offset(snapshot, Position(2, 0)), 13)
        for position in [Position(0, 2), Position(0, 5), Position(3, 0)]:
            with self.subTest(position=position), self.assertRaises(AdapterError):
                self.workspace.offset(snapshot, position)

    def test_uri_containment_aliases(self):
        uri = self.source.as_uri()
        self.assertEqual(
            self.workspace.read(uri.replace("%20", " ")).sha256, self.workspace.read(uri).sha256
        )
        for denied in [
            "file:///etc/passwd",
            uri + "?x=1",
            uri + "#part",
            "file://remote/etc/a",
            self.root.as_uri() + "/%2e%2e/escape.py",
            self.root.as_uri() + "/%ZZ.py",
        ]:
            with self.subTest(uri=denied), self.assertRaises(AdapterError):
                self.workspace.read(denied)

    def test_symlink_denied(self):
        link = self.root / "alias.py"
        link.symlink_to(self.source)
        with self.assertRaises(AdapterError):
            self.workspace.read(link.as_uri())

    def test_manifest_hashes_bytes_not_mtime(self):
        before = self.workspace.manifest()
        stamp = self.source.stat()
        self.source.write_bytes("x😀b\r\nnext\n".encode())
        os.utime(self.source, ns=(stamp.st_atime_ns, stamp.st_mtime_ns))
        self.assertNotEqual(self.workspace.manifest(), before)
        extra = self.root / "new.py"
        extra.write_text("pass\n")
        created = self.workspace.manifest()
        extra.unlink()
        self.assertNotEqual(self.workspace.manifest(), created)

    def test_nontext_file_and_missing_file_denied(self):
        self.source.write_bytes(b"\x00binary")
        with self.assertRaises(AdapterError):
            self.workspace.read(self.source.as_uri())
        with self.assertRaises(AdapterError):
            self.workspace.read((self.root / "missing.py").as_uri())

    def test_invalid_integer_positions(self):
        for line, character in [(True, 0), (0, False), (-1, 0), (0, 0.5)]:
            with self.subTest(position=(line, character)), self.assertRaises(AdapterError):
                Position(line, cast(int, character))

    def test_explicit_scope_exclusion_denies_direct_read(self):
        payload = json.loads(self.settings.read_text())
        payload["exclusions"] = [self.source.name]
        self.settings.write_text(json.dumps(payload))
        workspace = Workspace(load_config(self.settings))
        with self.assertRaises(AdapterError):
            workspace.read(self.source.as_uri())

    def test_fifo_is_rejected_without_waiting_for_a_writer(self):
        fifo = self.root / "pipe.py"
        os.mkfifo(fifo)
        code = (
            "import sys; from pathlib import Path; "
            "from gz_mcp_lsp.config import load_config; "
            "from gz_mcp_lsp.workspace import Workspace; "
            "from gz_mcp_lsp.models import AdapterError; "
            "w=Workspace(load_config(Path(sys.argv[1]))); "
            "\ntry: w.read(sys.argv[2])"
            "\nexcept AdapterError as e: print(e.code)"
        )
        result = subprocess.run(
            [sys.executable, "-c", code, str(self.settings), fifo.as_uri()],
            timeout=2,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
            check=True,
        )
        self.assertEqual(result.stdout.strip(), "INVALID_INPUT")

    def test_file_and_manifest_limits_fail_visibly(self):
        payload = json.loads(self.settings.read_text())
        payload["limits"] = {"max_file_bytes": 2}
        self.settings.write_text(json.dumps(payload))
        limited = Workspace(load_config(self.settings))
        with self.assertRaises(AdapterError) as failure:
            limited.read(self.source.as_uri())
        self.assertEqual(failure.exception.code, "LIMIT_EXCEEDED")
        payload["limits"] = {"max_files": 1}
        self.settings.write_text(json.dumps(payload))
        (self.root / "another.py").write_bytes(b"pass\n")
        with self.assertRaises(AdapterError) as failure:
            Workspace(load_config(self.settings)).manifest()
        self.assertEqual(failure.exception.code, "LIMIT_EXCEEDED")
