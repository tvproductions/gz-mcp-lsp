"""Verify project-owned JSON settings without environment overrides."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


class ConfigTests(unittest.TestCase):
    """Reject ambiguous settings and preserve disabled-by-default authority."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name).resolve()
        self.root = self.directory / "workspace"
        self.root.mkdir()
        self.settings = self.directory / "settings.json"

    def load(self, **changes):
        """Load an invented workspace and preinstalled executable."""
        from gz_mcp_lsp.config import load_config

        data = {
            "schema_version": 1,
            "workspace_root": str(self.root),
            "ty_executable": sys.executable,
        }
        data.update(changes)
        self.settings.write_text(json.dumps(data), encoding="utf-8")
        return load_config(self.settings)

    def test_mutations_default_disabled(self):
        """Read-only startup requires no implicit writable roots or state writes."""
        config = self.load()
        self.assertFalse(config.mutations_enabled)
        self.assertEqual(config.writable_roots, ())
        self.assertIsNone(config.state_directory)
        self.assertEqual(config.request_timeout_seconds, 20)
        self.assertEqual(config.limits.file_bytes, 2 * 1024 * 1024)
        self.assertEqual(config.limits.workspace_files, 10_000)

    def test_reject_unknown_config_and_env_override(self):
        """Only explicit JSON keys control the application."""
        from gz_mcp_lsp.models import AdapterError

        for changes in [
            {"unknown": 1},
            {"mutations": {"approved": True}},
            {"limits": {"unknown": 1}},
            {"schema_version": True},
            {"request_timeout_seconds": True},
        ]:
            with self.subTest(changes=changes), self.assertRaises(AdapterError):
                self.load(**changes)
        with patch.dict(os.environ, {"GZ_MCP_LSP_WORKSPACE_ROOT": "/unrelated"}):
            self.assertEqual(self.load().workspace_root, self.root.resolve())

    def test_duplicate_keys_and_nonfinite_json_are_rejected(self):
        """Duplicate policy keys and NaN cannot select ambiguous authority."""
        from gz_mcp_lsp.config import load_config
        from gz_mcp_lsp.models import AdapterError

        for text in ['{"schema_version":1,"schema_version":1}', '{"schema_version":NaN}']:
            self.settings.write_text(text, encoding="utf-8")
            with self.subTest(text=text), self.assertRaises(AdapterError):
                load_config(self.settings)

    def test_limits_require_positive_integers(self):
        """Bool, float and nonpositive resource caps are invalid."""
        from gz_mcp_lsp.models import AdapterError

        for value in [True, 1.5, 0, -1, "10"]:
            with self.subTest(value=value), self.assertRaises(AdapterError):
                self.load(limits={"file_bytes": value})
        self.assertEqual(self.load(limits={"file_bytes": 64}).limits.file_bytes, 64)

    def test_authority_paths_are_explicit_and_bounded(self):
        """Enabling writes requires roots plus private state outside source."""
        from gz_mcp_lsp.models import AdapterError

        for changes in [
            {"workspace_root": "relative"},
            {"ty_executable": "ty"},
            {"mutations": {"enabled": True}},
            {
                "mutations": {"enabled": True, "writable_roots": [str(self.directory)]},
                "state_directory": str(self.directory / "state"),
            },
            {
                "mutations": {"enabled": True, "writable_roots": [str(self.root)]},
                "state_directory": str(self.root / "state"),
            },
        ]:
            with self.subTest(changes=changes), self.assertRaises(AdapterError):
                self.load(**changes)
        if sys.platform == "win32":
            with self.assertRaises(AdapterError) as caught:
                self.load(
                    mutations={"enabled": True, "writable_roots": [str(self.root)]},
                    state_directory=str(self.directory / "state"),
                )
            self.assertEqual(caught.exception.code, "UNSUPPORTED")

    def test_invalid_state_directory_and_overflow_timeout_fail_as_domain_errors(self):
        """State must be a directory and enormous timeout values fail deliberately."""
        from gz_mcp_lsp.models import AdapterError

        state = self.directory / "not-a-directory"
        state.write_bytes(b"occupied")
        for changes in [
            {"state_directory": str(state)},
            {"request_timeout_seconds": 10**400},
        ]:
            with self.subTest(changes=changes), self.assertRaises(AdapterError):
                self.load(**changes)

    def test_scope_paths_cannot_escape(self):
        """Exclusions/config inputs are literal contained relative paths."""
        from gz_mcp_lsp.models import AdapterError

        for changes in [
            {"exclusions": ["../outside"]},
            {"exclusions": ["*.py"]},
            {"project_config_files": ["../settings.toml"]},
        ]:
            with self.subTest(changes=changes), self.assertRaises(AdapterError):
                self.load(**changes)
