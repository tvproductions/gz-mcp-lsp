"""Exercise distribution guard failures without depending on generated build output."""

import io
import sys
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path

from tools.verify_distribution import run, verify_archives


class DistributionGuardTests(unittest.TestCase):
    """Keep starter payloads and unintended runtime requirements out of the wheel."""

    def test_child_output_decoding_is_explicit_and_nonfatal(self):
        """Malformed UTF-8 diagnostics cannot break subprocess cleanup/reporting."""
        with tempfile.TemporaryDirectory() as temporary:
            result = run(
                sys.executable,
                "-c",
                "import sys; sys.stdout.buffer.write(bytes([255]))",
                cwd=Path(temporary),
            )
        self.assertEqual(result.stdout, "\ufffd")

    def test_console_entry_point_is_required(self):
        """A runtime distribution must provide its one approved stdio command."""
        with self.assertRaisesRegex(ValueError, "entry"):
            self.check_artifacts(entry_points="")

    def test_sdk_metadata_is_accepted(self):
        """The declared official SDK is the sole allowed runtime requirement."""
        try:
            self.check_artifacts(
                metadata="Name: gz-mcp-lsp\nVersion: 0.1.0\nRequires-Dist: mcp==2.3.0\n"
            )
        except ValueError as error:
            self.fail(f"Intended SDK metadata was rejected: {error}")

    def test_missing_sdk_is_rejected(self):
        """A runtime wheel must not silently omit the official MCP SDK."""
        with self.assertRaisesRegex(ValueError, "dependencies"):
            self.check_artifacts(metadata="Name: gz-mcp-lsp\nVersion: 0.1.0\n")

    def test_normalized_sdk_requirement_is_accepted(self):
        """Equivalent casing and whitespace retain the exact SDK requirement."""
        self.check_artifacts(
            metadata="Name: gz-mcp-lsp\nVersion: 0.1.0\nRequires-Dist: McP (== 2.3.0)\n"
        )

    def test_sdk_artifacts_are_accepted(self):
        """A correctly identified SDK-dependent package passes the archive guard."""
        self.check_artifacts()

    def test_wrong_identity_is_rejected(self):
        """A copied starter distribution cannot pass product verification."""
        with self.assertRaisesRegex(ValueError, "identity"):
            self.check_artifacts(metadata="Name: skills-first-starter\n")

    def test_undeclared_runtime_surface_is_rejected(self):
        """Unreviewed runtime requirements must not slip into a wheel."""
        with self.assertRaisesRegex(ValueError, "dependencies"):
            self.check_artifacts(
                metadata="Name: gz-mcp-lsp\nVersion: 0.1.0\nRequires-Dist: unexpected\n"
            )

    def test_sdk_requirement_must_be_exact_and_unique(self):
        """Reject changed versions, markers, extras and duplicate requirements."""
        for requirements in [
            "mcp>=2.3.0",
            "mcp==2.3.1",
            "mcp[cli]==2.3.0",
            "mcp==2.3.0; sys_platform == 'win32'",
            "mcp==2.3.0\nRequires-Dist: mcp==2.3.0",
            "mcp==2.3.0\nRequires-Dist: unexpected",
        ]:
            with (
                self.subTest(requirements=requirements),
                self.assertRaisesRegex(ValueError, "dependencies"),
            ):
                self.check_artifacts(
                    metadata="Name: gz-mcp-lsp\nVersion: 0.1.0\nRequires-Dist: "
                    + requirements
                    + "\n"
                )

    def test_starter_or_development_payload_is_rejected(self):
        """Inherited helper code and development files are not runtime payloads."""
        for name in ["skills_first_starter/cli.py", "tests/test_starter.py", "tools/probe.py"]:
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "development"):
                self.check_artifacts(extra_wheel_file=name)

    def test_source_environment_leakage_is_rejected(self):
        """Source archives must not expose the local development environment."""
        with self.assertRaisesRegex(ValueError, "environment"):
            self.check_artifacts(extra_source_file="gz_mcp_lsp-0.1.0/.venv/secret")

    def test_missing_runtime_module_or_typing_resource_is_rejected(self):
        for resource in ("gz_mcp_lsp/cli.py", "gz_mcp_lsp/py.typed"):
            with self.subTest(resource=resource), self.assertRaisesRegex(ValueError, "missing"):
                self.check_artifacts(omit=resource)

    def test_missing_license_notice_is_rejected(self):
        for resource in ("LICENSE", "NOTICE"):
            with self.subTest(resource=resource), self.assertRaisesRegex(ValueError, "missing"):
                self.check_artifacts(omit=resource)

    def test_source_license_notices_are_required(self):
        for resource in ("LICENSE", "NOTICE"):
            with self.subTest(resource=resource), self.assertRaisesRegex(ValueError, "missing"):
                self.check_artifacts(omit_source=resource)

    def check_artifacts(
        self,
        metadata="Name: gz-mcp-lsp\nVersion: 0.1.0\nRequires-Dist: mcp==2.3.0\n",
        extra_wheel_file=None,
        extra_source_file=None,
        entry_points="[console_scripts]\ngz-mcp-lsp = gz_mcp_lsp.cli:main\n",
        omit=None,
        omit_source=None,
    ):
        """Build invented archives to test acceptance and failure behavior."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            wheel, sdist = root / "product.whl", root / "product.tar.gz"
            with zipfile.ZipFile(wheel, "w") as archive:
                for name in ("gz_mcp_lsp/cli.py", "gz_mcp_lsp/py.typed"):
                    if name != omit:
                        archive.writestr(name, "")
                for name in ("LICENSE", "NOTICE"):
                    if name != omit:
                        archive.writestr(f"gz_mcp_lsp-0.1.0.dist-info/licenses/{name}", "notice")
                archive.writestr("gz_mcp_lsp-0.1.0.dist-info/METADATA", metadata)
                archive.writestr("gz_mcp_lsp-0.1.0.dist-info/entry_points.txt", entry_points)
                if extra_wheel_file:
                    archive.writestr(extra_wheel_file, "")
            with tarfile.open(sdist, "w:gz") as archive:
                names = ["gz_mcp_lsp-0.1.0/tests/README.md"]
                names.extend(
                    f"gz_mcp_lsp-0.1.0/{name}"
                    for name in ("LICENSE", "NOTICE")
                    if name != omit_source
                )
                if extra_source_file:
                    names.append(extra_source_file)
                for name in names:
                    archive.addfile(tarfile.TarInfo(name), io.BytesIO())
            verify_archives(wheel, sdist, "0.1.0")
