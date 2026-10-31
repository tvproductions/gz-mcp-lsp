"""Configuration must establish operator authority without ambient overrides."""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from gz_mcp_lsp.config import load_config
from gz_mcp_lsp.models import AdapterError


class ConfigurationTests(unittest.TestCase):
    """Malformed settings cannot grant writes or bypass resource bounds."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.settings = self.root / "settings.json"
        self.payload = {
            "schema_version": 1,
            "workspace_root": str(self.root),
            "ty_executable": "/usr/bin/true",
        }

    def load(self, **changes):
        self.settings.write_text(json.dumps(self.payload | changes))
        return load_config(self.settings)

    def test_mutations_default_disabled_and_env_ignored(self):
        with patch.dict(
            os.environ,
            {"GZ_MCP_LSP_MUTATIONS_ENABLED": "true", "GZ_MCP_LSP_WORKSPACE_ROOT": "/etc"},
        ):
            config = self.load()
        self.assertFalse(config.mutations_enabled)
        self.assertEqual(config.workspace_root, self.root)
        self.assertEqual(config.writable_roots, ())

    def test_reject_unknown_config_and_invalid_budgets(self):
        for changes in [
            {"unknown": 1},
            {"schema_version": True},
            {"limits": {"max_file_bytes": -1}},
            {"limits": {"unknown": 1}},
            {"request_timeout_seconds": False},
        ]:
            with self.subTest(changes=changes), self.assertRaises(AdapterError):
                self.load(**changes)

    def test_write_authority_requires_bounded_roots_and_external_state(self):
        for mutations in [{"enabled": True}, {"enabled": True, "writable_roots": ["/etc"]}]:
            with self.subTest(mutations=mutations), self.assertRaises(AdapterError):
                self.load(mutations=mutations)
        with self.assertRaises(AdapterError):
            self.load(
                mutations={"enabled": True, "writable_roots": [str(self.root)]},
                state_directory=str(self.root / "state"),
            )

    def test_nonabsolute_and_nonexistent_paths_denied(self):
        for changes in [
            {"workspace_root": "."},
            {"ty_executable": "/missing-ty"},
            {"workspace_root": str(self.root / "missing")},
        ]:
            with self.subTest(changes=changes), self.assertRaises(AdapterError):
                self.load(**changes)

    def test_duplicate_json_policy_is_rejected(self):
        self.settings.write_text(json.dumps(self.payload)[:-1] + ', "schema_version": 1}')
        with self.assertRaises(AdapterError):
            load_config(self.settings)
