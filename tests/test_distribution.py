"""Exercise distribution guard failures without depending on generated build output."""

import io
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path

from tools.verify_distribution import verify_archives


class DistributionGuardTests(unittest.TestCase):
    """Keep starter payloads and unintended runtime requirements out of the wheel."""

    def test_design_stage_artifacts_are_accepted(self):
        """A correctly identified minimal package passes the archive guard."""
        self.check_artifacts()

    def test_wrong_identity_is_rejected(self):
        """A copied starter distribution cannot pass product verification."""
        with self.assertRaisesRegex(ValueError, "identity"):
            self.check_artifacts(metadata="Name: skills-first-starter\n")

    def test_undeclared_runtime_surface_is_rejected(self):
        """A scaffold must not accidentally ship runtime dependency requirements."""
        with self.assertRaisesRegex(ValueError, "dependencies"):
            self.check_artifacts(metadata="Name: gz-mcp-lsp\nRequires-Dist: unexpected\n")

    def test_starter_or_development_payload_is_rejected(self):
        """Inherited helper code and development files are not runtime payloads."""
        for name in ["skills_first_starter/cli.py", "tests/test_starter.py", "tools/probe.py"]:
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "development"):
                self.check_artifacts(extra_wheel_file=name)

    def test_source_environment_leakage_is_rejected(self):
        """Source archives must not expose the local development environment."""
        with self.assertRaisesRegex(ValueError, "environment"):
            self.check_artifacts(extra_source_file="gz_mcp_lsp-0.0.0/.venv/secret")

    def check_artifacts(
        self,
        metadata="Name: gz-mcp-lsp\nVersion: 0.0.0\n",
        extra_wheel_file=None,
        extra_source_file=None,
    ):
        """Build invented archives to test acceptance and failure behavior."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            wheel, sdist = root / "product.whl", root / "product.tar.gz"
            with zipfile.ZipFile(wheel, "w") as archive:
                archive.writestr("gz_mcp_lsp/py.typed", "")
                archive.writestr("gz_mcp_lsp-0.0.0.dist-info/METADATA", metadata)
                if extra_wheel_file:
                    archive.writestr(extra_wheel_file, "")
            with tarfile.open(sdist, "w:gz") as archive:
                names = ["gz_mcp_lsp-0.0.0/tests/README.md"]
                if extra_source_file:
                    names.append(extra_source_file)
                for name in names:
                    archive.addfile(tarfile.TarInfo(name), io.BytesIO())
            verify_archives(wheel, sdist, "0.0.0")
