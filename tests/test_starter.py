import json
import os
import subprocess
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest import mock

from skills_first_starter import cli as starter

MODULE = Path(__file__).parents[1] / "starter.py"
REF = "a" * 40


class AdoptionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.addCleanup(self.temp.cleanup)

    def configure(self, apply=False):
        return starter.configure(self.root, REF, apply=apply)

    def test_preview_never_writes(self):
        result = self.configure()
        self.assertEqual(list(self.root.iterdir()), [])
        self.assertEqual(result["status"], "preview")
        self.assertIn(".codex/config.toml", result["writes"])

    def test_wheel_resources_match_authoritative_checkout(self):
        result = subprocess.run(
            [
                str(Path(starter.sys.executable)),
                str(MODULE.parent / "tools/package_resources.py"),
                "--check",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_second_adoption_is_noop(self):
        self.configure(True)
        before = {
            p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()
        }
        result = self.configure(True)
        after = {
            p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()
        }
        self.assertEqual(before, after)
        self.assertEqual(result["writes"], [])

    def test_preserves_existing_instructions_and_config(self):
        (self.root / "AGENTS.md").write_text("Existing project authority.\n")
        (self.root / ".codex").mkdir()
        config = self.root / ".codex/config.toml"
        config.write_text('model = "example"\n# Keep this comment.\n')
        self.configure(True)
        self.assertEqual((self.root / "AGENTS.md").read_text(), "Existing project authority.\n")
        self.assertTrue(config.read_text().startswith('model = "example"\n# Keep this comment.\n'))
        self.assertIn("AGENTS.skills-first.md", starter.configure(self.root, REF)["present"])

    def test_preserves_extended_project_dependencies_and_settings(self):
        dependencies = ",\n".join(f'  "fixture-adapter-{n}>=1,<3"' for n in range(60))
        project = (
            '# Project-owned metadata and comments.\n[project]\nname = "fixture-app"\n'
            f'version = "0.1.0"\ndependencies = [\n{dependencies}\n]\n'
            '[project.optional-dependencies]\nexport = ["fixture-export>=2"]\n'
            '[dependency-groups]\ndev = ["fixture-tool==3.0"]\n'
            '[tool.uv]\noverride-dependencies = ["fixture-shared==2.0"]\n'
            '[tool.uv.sources]\nfixture-export = { path = "adapters/export" }\n'
            '[tool.fixture_app]\noutput_directory = "products"\n'
        )
        settings = {
            "schema_version": 1,
            "extensions": {"enabled": ["summary_export"]},
            "overrides": {"output_directory": "custom_products"},
        }
        fixtures = {
            "pyproject.toml": project.encode(),
            "settings.json": (json.dumps(settings, indent=2) + "\n").encode(),
            # Preservation-only fixture; not a claim to be a resolved uv lock.
            "uv.lock": b"# Existing project lock fixture.\nversion = 1\n",
        }
        for name, payload in fixtures.items():
            (self.root / name).write_bytes(payload)
        self.assertEqual(len(tomllib.loads(project)["project"]["dependencies"]), 60)
        for apply in (False, True, True):
            with self.subTest(apply=apply):
                result = self.configure(apply)
                self.assertFalse(set(fixtures) & set(result["writes"]))
                for name, payload in fixtures.items():
                    self.assertEqual((self.root / name).read_bytes(), payload)

    def test_adoption_uses_utf8_and_preserves_host_config_bytes(self):
        (self.root / ".codex").mkdir()
        config = self.root / ".codex/config.toml"
        original = '# Project: café, “示例”\r\nmodel = "example"\r\n'.encode()
        config.write_bytes(original)
        read_text = Path.read_text

        def legacy_locale_read(path, *args, **kwargs):
            kwargs.setdefault("encoding", "cp1252")
            return read_text(path, *args, **kwargs)

        with mock.patch.object(Path, "read_text", autospec=True, side_effect=legacy_locale_read):
            self.configure(True)
            after = config.read_bytes()
            self.assertTrue(after.startswith(original))
            self.assertEqual(self.configure(True)["writes"], [])
            self.assertEqual(config.read_bytes(), after)

    def test_conflict_blocks_all_writes(self):
        (self.root / ".codex").mkdir()
        p = self.root / ".codex/config.toml"
        p.write_text('[plugins."gz-skills@skills-first-starter"]\nenabled = false\n')
        with self.assertRaises(starter.AdoptionError):
            self.configure(True)
        self.assertFalse((self.root / ".skills-first").exists())
        self.assertFalse((self.root / "AGENTS.md").exists())
        self.assertIn("false", p.read_text())

    def test_failed_replacement_preserves_existing_config_and_cleans_temporary_file(self):
        folder = self.root / ".codex"
        folder.mkdir()
        config = folder / "config.toml"
        original = b'model = "fixture"\r\n'
        config.write_bytes(original)
        with (
            mock.patch.object(starter.os, "replace", side_effect=OSError("fixture failure")),
            self.assertRaisesRegex(OSError, "fixture failure"),
        ):
            self.configure(True)
        self.assertEqual(config.read_bytes(), original)
        self.assertEqual(list(folder.iterdir()), [config])
        self.assertFalse((self.root / ".skills-first").exists())

    def test_later_write_failure_rolls_back_created_and_replaced_files(self):
        for existing in (False, True):
            with self.subTest(existing=existing), tempfile.TemporaryDirectory() as directory:
                root = Path(directory).resolve()
                config = root / ".codex/config.toml"
                original = b'model = "fixture"\r\n'
                if existing:
                    config.parent.mkdir()
                    config.write_bytes(original)
                open_path = Path.open

                def fail_lock(path, *args, root=root, open_path=open_path, **kwargs):
                    if path == root / ".skills-first/bundle.lock.json" and args == ("xb",):
                        raise OSError("fixture lock failure")
                    return open_path(path, *args, **kwargs)

                with (
                    mock.patch.object(Path, "open", autospec=True, side_effect=fail_lock),
                    self.assertRaisesRegex(OSError, "fixture lock failure"),
                ):
                    starter.configure(root, REF, apply=True)
                files = [path for path in root.rglob("*") if path.is_file()]
                self.assertEqual(files, [config] if existing else [])
                if existing:
                    self.assertEqual(config.read_bytes(), original)

    def test_concurrent_later_file_is_preserved_while_prior_write_rolls_back(self):
        config = self.root / ".codex/config.toml"
        config.parent.mkdir()
        original = b'model = "fixture"\r\n'
        config.write_bytes(original)
        lock = self.root / ".skills-first/bundle.lock.json"
        concurrent = b"Concurrent fixture record.\n"
        replace_file = os.replace

        def replace_with_concurrent_writer(source, destination):
            lock.parent.mkdir()
            lock.write_bytes(concurrent)
            replace_file(source, destination)

        with (
            mock.patch.object(starter.os, "replace", side_effect=replace_with_concurrent_writer),
            self.assertRaisesRegex(starter.AdoptionError, "changed during preview"),
        ):
            self.configure(True)
        self.assertEqual(config.read_bytes(), original)
        self.assertEqual(lock.read_bytes(), concurrent)
        self.assertFalse((self.root / "AGENTS.skills-first.md").exists())

    def test_disabled_alternative_plugin_source_is_preserved(self):
        config = self.root / ".codex/config.toml"
        config.parent.mkdir()
        original = b'[plugins."superpowers@fixture-other"]\nenabled = false\n'
        config.write_bytes(original)
        self.configure(True)
        self.assertTrue(config.read_bytes().startswith(original))
        self.assertEqual(self.configure(True)["writes"], [])

    def test_gzkit_is_not_reconfigured(self):
        (self.root / ".gzkit").mkdir()
        with self.assertRaises(starter.AdoptionError):
            self.configure(True)
        self.assertEqual([p.name for p in self.root.iterdir()], [".gzkit"])

    def test_symlink_destination_is_rejected(self):
        external = self.root / "outside"
        external.mkdir()
        (self.root / ".codex").symlink_to(external, target_is_directory=True)
        with self.assertRaises(starter.AdoptionError):
            self.configure(True)
        self.assertEqual(list(external.iterdir()), [])

    def test_existing_legacy_skill_copy_blocks_duplicate_discovery(self):
        p = self.root / ".agents/skills/gzs-router"
        p.mkdir(parents=True)
        (p / "SKILL.md").write_text("Legacy skill copy")
        with self.assertRaises(starter.AdoptionError):
            self.configure(True)
        self.assertFalse((self.root / ".codex").exists())

    def test_existing_other_marketplace_plugin_blocks_duplicate(self):
        (self.root / ".codex").mkdir()
        (self.root / ".codex/config.toml").write_text(
            '[plugins."superpowers@other"]\nenabled = true\n'
        )
        with self.assertRaises(starter.AdoptionError):
            self.configure(True)

    def test_pending_profile_is_not_a_readiness_claim(self):
        self.configure(True)
        self.assertFalse((self.root / ".gz-skills/settings.json").exists())
        self.assertEqual(starter.status(self.root)["runtime_readiness"], "unverified")

    def test_existing_profile_and_rules_are_preserved(self):
        (self.root / ".gz-skills").mkdir()
        p = self.root / ".gz-skills/settings.json"
        p.write_text('{"schema_version": 1, "profile": "lite"}\n')
        self.configure(True)
        self.assertEqual(p.read_text(), '{"schema_version": 1, "profile": "lite"}\n')

    def test_malformed_settings_do_not_get_overwritten(self):
        (self.root / ".gz-skills").mkdir()
        (self.root / ".gz-skills/settings.json").write_text("{}")
        with self.assertRaises(starter.AdoptionError):
            self.configure(True)

    def test_backplane_is_pinned_but_disabled(self):
        self.configure(True)
        data = tomllib.loads((self.root / ".codex/config.toml").read_text())
        self.assertIs(
            data["plugins"]["superpowers-backplane@skills-first-starter"]["enabled"], False
        )
        self.assertIs(data["plugins"]["superpowers@skills-first-starter"]["enabled"], True)
        self.assertIs(data["plugins"]["gz-skills@skills-first-starter"]["enabled"], True)

    def test_active_backplane_is_not_silently_disabled(self):
        (self.root / ".codex").mkdir()
        p = self.root / ".codex/config.toml"
        original = '[plugins."superpowers-backplane@skills-first-starter"]\nenabled = true\n'
        p.write_text(original)
        with self.assertRaises(starter.AdoptionError):
            self.configure(True)
        self.assertEqual(p.read_text(), original)
        self.assertFalse((self.root / ".skills-first").exists())

    def test_adoption_seeds_only_the_canonical_template_update_skill(self):
        result = self.configure(True)
        self.assertEqual(
            set(result["writes"]),
            {
                ".codex/config.toml",
                ".skills-first/bundle.lock.json",
                "AGENTS.skills-first.md",
                "AGENTS.md",
                starter.UPDATE_SKILL_DESTINATION,
            },
        )
        skill = self.root / starter.UPDATE_SKILL_DESTINATION
        self.assertEqual(list(self.root.rglob("SKILL.md")), [skill])
        self.assertEqual(
            skill.read_bytes(), (MODULE.parent / starter.UPDATE_SKILL_SOURCE).read_bytes()
        )
        self.assertEqual(starter.status(self.root)["status"], "configured")

    def test_modified_update_skill_blocks_all_writes_and_is_preserved(self):
        skill = self.root / starter.UPDATE_SKILL_DESTINATION
        skill.parent.mkdir(parents=True)
        original = b"Project-edited update guidance.\n"
        skill.write_bytes(original)
        for apply in (False, True):
            with self.subTest(apply=apply), self.assertRaises(starter.AdoptionError):
                self.configure(apply)
            self.assertEqual(skill.read_bytes(), original)
            self.assertEqual([p for p in self.root.rglob("*") if p.is_file()], [skill])

    def test_update_skill_symlink_cannot_write_outside_project(self):
        with tempfile.TemporaryDirectory() as directory:
            external = Path(directory).resolve()
            target = self.root / starter.UPDATE_SKILL_DESTINATION
            target.parent.mkdir(parents=True)
            target.symlink_to(external / "SKILL.md")
            with self.assertRaises(starter.AdoptionError):
                self.configure(True)
            self.assertEqual(list(external.iterdir()), [])
        self.assertFalse((self.root / ".codex").exists())

    def test_alternate_surface_update_skill_requires_reconciliation(self):
        for surface in (".codex/skills", ".claude/skills", ".github/skills"):
            with self.subTest(surface=surface), tempfile.TemporaryDirectory() as directory:
                root = Path(directory).resolve()
                skill = root / surface / starter.UPDATE_SKILL / "SKILL.md"
                skill.parent.mkdir(parents=True)
                skill.write_text("Existing alternative installation.\n")
                with self.assertRaises(starter.AdoptionError):
                    starter.configure(root, REF, apply=True)
                self.assertEqual([p for p in root.rglob("*") if p.is_file()], [skill])

    def test_update_skill_write_failure_rolls_back_prior_managed_outputs(self):
        target = self.root / starter.UPDATE_SKILL_DESTINATION
        open_path = Path.open

        def fail_skill(path, *args, **kwargs):
            if path == target and args == ("xb",):
                raise OSError("fixture skill failure")
            return open_path(path, *args, **kwargs)

        with (
            mock.patch.object(Path, "open", autospec=True, side_effect=fail_skill),
            self.assertRaisesRegex(OSError, "fixture skill failure"),
        ):
            self.configure(True)
        self.assertEqual([p for p in self.root.rglob("*") if p.is_file()], [])

    def test_modified_project_guidance_is_preserved(self):
        self.configure(True)
        guidance = self.root / "AGENTS.skills-first.md"
        guidance.write_text("Project-specific routing")
        with self.assertRaises(starter.AdoptionError):
            self.configure(True)
        self.assertEqual(guidance.read_text(), "Project-specific routing")

    def test_project_owned_skills_are_preserved(self):
        skill = self.root / ".agents/skills/fixture-operation/SKILL.md"
        skill.parent.mkdir(parents=True)
        original = b"Project-owned operational instructions.\n"
        skill.write_bytes(original)
        expected = {skill}
        for apply in (False, True, True):
            with self.subTest(apply=apply):
                self.configure(apply)
                if apply:
                    expected.add(self.root / starter.UPDATE_SKILL_DESTINATION)
                self.assertEqual(skill.read_bytes(), original)
                self.assertEqual(set(self.root.rglob("SKILL.md")), expected)

    def test_backport_assessment_preserves_records_and_does_not_follow_links(self):
        (self.root / "records").mkdir()
        record = self.root / "records/private.txt"
        record.write_text("private fixture content")
        (self.root / "alias").symlink_to(self.root / "records", target_is_directory=True)
        before = record.read_bytes()
        result = starter.backport(self.root)
        self.assertEqual(result["writes"], [])
        self.assertEqual(result["backplane"], "deferred")
        self.assertNotIn("private fixture content", json.dumps(result))
        self.assertNotIn("private.txt", json.dumps(result))
        self.assertEqual(record.read_bytes(), before)
        self.assertEqual({x.name for x in self.root.iterdir()}, {"records", "alias"})
        self.assertEqual(
            next(e for e in result["inventory"] if e["path"] == "alias")["kind"], "symlink"
        )

    def test_legacy_starter_skills_require_review_before_any_writes(self):
        for surface in (".agents/skills", ".codex/skills", ".claude/skills", ".github/skills"):
            for name in ("skills-first-start", "adopt-skills-stack", "python-engineering"):
                with (
                    self.subTest(surface=surface, name=name),
                    tempfile.TemporaryDirectory() as directory,
                ):
                    root = Path(directory)
                    skill = root / surface / name / "SKILL.md"
                    skill.parent.mkdir(parents=True)
                    original = b"Retained starter skill with project edits.\n"
                    skill.write_bytes(original)
                    for apply in (False, True):
                        with self.assertRaisesRegex(starter.AdoptionError, "migration-0.3"):
                            starter.configure(root, REF, apply=apply)
                        self.assertEqual(skill.read_bytes(), original)
                        self.assertEqual([p for p in root.rglob("*") if p.is_file()], [skill])

    def test_template_contains_only_the_approved_update_skill_and_wheel_copy(self):
        self.assertFalse((MODULE.parent / "skills").exists())
        tracked = starter.subprocess.run(
            [
                "git",
                "-C",
                str(MODULE.parent),
                "ls-files",
                "--cached",
                "--others",
                "--exclude-standard",
            ],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
        ).stdout.splitlines()
        self.assertEqual(
            {
                name
                for name in tracked
                if Path(name).name == "SKILL.md" and (MODULE.parent / name).exists()
            },
            {
                starter.UPDATE_SKILL_SOURCE,
                f"src/skills_first_starter/resources/{starter.UPDATE_SKILL_SOURCE}",
            },
        )

    def test_backport_inventory_is_bounded(self):
        for n in range(205):
            (self.root / f"entry-{n}").touch()
        result = starter.backport(self.root)
        self.assertEqual(len(result["inventory"]), 200)
        self.assertTrue(result["inventory_truncated"])

    def test_pins_are_immutable_and_marketplace_matches(self):
        starter.validate_bundle()
        catalog = json.loads((MODULE.parent / ".agents/plugins/marketplace.json").read_text())
        self.assertEqual(
            {p["name"]: p["source"]["ref"] for p in catalog["plugins"]},
            {p["name"]: p["revision"] for p in starter.bundle()["components"]},
        )
        claude = json.loads((MODULE.parent / ".claude-plugin/marketplace.json").read_text())
        for plugin in claude["plugins"]:
            self.assertNotIn("ref", plugin["source"])
        self.assertEqual(
            {p["name"]: p["source"]["sha"] for p in claude["plugins"]},
            {p["name"]: p["revision"] for p in starter.bundle()["components"]},
        )

    def test_source_revision_recognizes_legacy_and_canonical_starter_origins(self):
        origins = (
            "https://github.com/tvproductions/skills-first-starter.git",
            "https://github.com/tvproductions/skills-first-starter",
            "https://github.com/tvproductions/gz-skills-first-starter.git",
            "https://github.com/tvproductions/gz-skills-first-starter",
        )
        for origin in origins:
            with self.subTest(origin=origin):
                outputs = {
                    ("rev-parse", "--show-toplevel"): str(self.root),
                    ("remote", "get-url", "origin"): origin,
                    ("status", "--porcelain"): "",
                    ("rev-parse", "HEAD"): REF,
                }

                def run_git(args, outputs=outputs, **kwargs):
                    return subprocess.CompletedProcess(args, 0, stdout=outputs[tuple(args[3:])])

                with (
                    mock.patch.object(starter, "HERE", self.root),
                    mock.patch.object(starter.subprocess, "run", side_effect=run_git),
                ):
                    try:
                        revision = starter.source_revision()
                    except starter.AdoptionError as error:
                        self.fail(f"recognized starter origin was rejected: {error}")
                    self.assertEqual(revision, REF)
                    outputs[("remote", "get-url", "origin")] = (
                        "https://github.com/example/fixture-adopter.git"
                    )
                    with self.assertRaisesRegex(starter.AdoptionError, "adopting repo"):
                        starter.source_revision()

    def test_adoption_records_canonical_starter_repository(self):
        self.configure(True)
        config = tomllib.loads((self.root / ".codex/config.toml").read_text())
        lock = json.loads((self.root / ".skills-first/bundle.lock.json").read_bytes())
        canonical = "https://github.com/tvproductions/gz-skills-first-starter.git"
        self.assertEqual(config["marketplaces"]["skills-first-starter"]["source"], canonical)
        self.assertEqual(lock["starter"]["repository"], canonical)

    def test_adoption_records_template_version_and_exact_revision(self):
        metadata = tomllib.loads((MODULE.parent / "pyproject.toml").read_text(encoding="utf-8"))
        app_metadata = b'[project]\nname = "fixture-app"\nversion = "7.3.2"\n'
        (self.root / "pyproject.toml").write_bytes(app_metadata)
        result = self.configure(True)
        lock = json.loads((self.root / ".skills-first/bundle.lock.json").read_bytes())
        self.assertEqual(lock["starter"]["version"], starter.bundle()["template_version"])
        self.assertEqual(lock["starter"]["version"], metadata["project"]["version"])
        self.assertEqual(lock["starter"]["revision"], REF)
        self.assertEqual(result["starter"], lock["starter"])
        self.assertEqual(starter.status(self.root)["starter"], lock["starter"])
        self.assertEqual(self.configure(True)["writes"], [])
        self.assertEqual((self.root / "pyproject.toml").read_bytes(), app_metadata)

    def test_invalid_template_version_blocks_adoption_before_writes(self):
        for version in (None, "latest", "v0.1.0", "01.1.0", 1):
            with self.subTest(version=version):
                data = starter.bundle()
                data["template_version"] = version
                with (
                    mock.patch.object(starter, "bundle", return_value=data),
                    self.assertRaises(starter.AdoptionError),
                ):
                    self.configure(True)
                self.assertEqual(list(self.root.iterdir()), [])

    def test_legacy_unversioned_lock_requires_review_and_is_preserved(self):
        self.configure(True)
        path = self.root / ".skills-first/bundle.lock.json"
        lock = json.loads(path.read_bytes())
        del lock["starter"]["version"]
        original = (json.dumps(lock, indent=2) + "\n").encode("utf-8")
        path.write_bytes(original)
        for action in (
            self.configure,
            lambda: self.configure(True),
            lambda: starter.status(self.root),
        ):
            with self.subTest(action=action):
                with self.assertRaises(starter.AdoptionError):
                    action()
                self.assertEqual(path.read_bytes(), original)

    def test_version_command_reports_manifest_version(self):
        with mock.patch("builtins.print") as output:
            self.assertEqual(starter.main(["version"]), 0)
        self.assertEqual(
            json.loads(output.call_args.args[0]),
            {"template_version": starter.bundle()["template_version"]},
        )

    def test_moving_starter_ref_is_rejected(self):
        with self.assertRaises(starter.AdoptionError):
            starter.configure(self.root, "main", apply=True)


if __name__ == "__main__":
    unittest.main()
