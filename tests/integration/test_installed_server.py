"""Full installed CLI contract over real ty using a three-package synthetic fixture."""

import json
import os
import shutil
import subprocess
from pathlib import Path

from tests.integration.mutation_support import InstalledMutationCase
from tests.integration.test_mutations import edit_range


class InstalledServerTests(InstalledMutationCase):
    def images(self):
        return {
            path.relative_to(self.root).as_posix(): path.read_bytes()
            for path in self.root.rglob("*")
            if path.is_file()
        }

    async def asyncSetUp(self):
        await super().asyncSetUp()
        shutil.copytree(
            self.checkout / "tests/fixtures/acceptance_workspace", self.root, dirs_exist_ok=True
        )
        shutil.copyfile(
            self.checkout / "tests/fixtures/semantic_workspace/hierarchy.py",
            self.root / "hierarchy.py",
        )
        self.expected = json.loads((self.root / "expected.json").read_text(encoding="utf-8"))
        self.module = self.root / "shared_runtime/__init__.py"
        self.caller = self.root / "package_a/__init__.py"

    def sites(self, locations):
        return sorted(
            (item["uri"], item["range"]["start"]["line"], item["range"]["start"]["character"])
            for item in locations
        )

    async def test_runtime_only_origin_and_full_read_contract_with_disabled_mutations(self):
        origin = subprocess.run(
            [
                str(self.python),
                "-I",
                "-c",
                "import gz_mcp_lsp,importlib.util,json,sys; "
                "print(json.dumps({'origin':gz_mcp_lsp.__file__,'prefix':sys.prefix,"
                "'development':[n for n in ('ruff','pre_commit','coverage','tests') if importlib.util.find_spec(n)]}))",
            ],
            cwd=self.outside,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
            timeout=20,
        )
        installed = json.loads(origin.stdout)
        self.assertEqual(installed["development"], [])
        installed_origin_root = (
            Path(installed["origin"]).resolve().parents[3 if os.name == "nt" else 4]
        )
        clean_environment_root = Path(installed["prefix"]).resolve()
        self.assertTrue(Path(installed["origin"]).resolve().is_relative_to(clean_environment_root))
        self.assertFalse(Path(installed["origin"]).resolve().is_relative_to(self.checkout))
        self.assertEqual(installed_origin_root, clean_environment_root)
        self.configure(enabled=False)
        before = self.images()
        async with self.client() as client:
            self.assertEqual(
                {tool.name for tool in (await client.list_tools()).tools},
                {
                    "definition",
                    "references",
                    "diagnostics",
                    "hover",
                    "rename_symbol",
                    "edit_file",
                    "document_symbols",
                    "workspace_symbols",
                    "implementations",
                },
            )
            query = {"uri": self.caller.as_uri(), "position": {"line": 2, "character": 9}}
            definition = await self.call(client, "definition", query)
            target = definition["result"]["locations"][0]
            self.assertEqual(target["uri"], self.module.as_uri())
            self.assertEqual(target["selection_range"]["start"], {"line": 0, "character": 4})
            self.assertEqual(
                target["source"]["text"],
                "def run_shared_cli(value: int) -> int:\n    return value + 1",
            )
            for include in (False, True):
                references = await self.call(
                    client,
                    "references",
                    {
                        "uri": self.module.as_uri(),
                        "position": {"line": 0, "character": 4},
                        "include_declaration": include,
                    },
                )
                expected = [
                    ((self.root / item["file"]).as_uri(), item["line"], item["character"])
                    for item in self.expected["calls"]
                ]
                if include:
                    expected += [
                        ((self.root / item["file"]).as_uri(), item["line"], item["character"])
                        for item in self.expected["imports"]
                    ]
                    expected += [(self.module.as_uri(), 0, 4)]
                self.assertEqual(self.sites(references["result"]["locations"]), sorted(expected))
            hover = await self.call(client, "hover", query)
            self.assertIn("run_shared_cli", str(hover["result"]["contents"]))
            diagnostics = await self.call(client, "diagnostics", {"uri": self.caller.as_uri()})
            self.assertEqual(diagnostics["result"]["items"], [])
            symbols = await self.call(client, "document_symbols", {"uri": self.module.as_uri()})
            self.assertEqual(symbols["result"]["symbols"][0]["name"], "run_shared_cli")
            search = await self.call(client, "workspace_symbols", {"query": "run_shared_cli"})
            self.assertEqual(
                {item["uri"] for item in search["result"]["symbols"]},
                {self.module.as_uri(), (self.root / "decoy.py").as_uri()},
            )
            implementations = await self.call(
                client,
                "implementations",
                {
                    "uri": (self.root / "hierarchy.py").as_uri(),
                    "position": {"line": 4, "character": 8},
                },
            )
            self.assertEqual(
                [item["range"]["start"]["line"] for item in implementations["result"]["locations"]],
                [4, 9, 14],
            )
            for name in ("edit_file", "rename_symbol"):
                response = await client.call_tool(name, {"action": "apply", "plan_id": "0" * 64})
                self.assertTrue(response.is_error)
                self.assertEqual(response.structured_content["error"]["code"], "MUTATIONS_DISABLED")
        self.assertEqual(before, self.images())

    async def test_both_mutations_change_only_expected_package_bytes(self):
        if os.name == "nt":
            self.skipTest(
                "POSIX installed writes; Windows disabled/unsupported denials run separately"
            )
        before = {
            p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*.py")
        }
        async with self.client() as client:
            preview = await self.call(
                client,
                "rename_symbol",
                {
                    "action": "preview",
                    "uri": self.module.as_uri(),
                    "position": {"line": 0, "character": 4},
                    "new_name": "renamed_cli",
                },
            )
            self.assertEqual(
                {item["uri"] for item in preview["result"]["files"]},
                {
                    self.module.as_uri(),
                    *((self.root / item["file"]).as_uri() for item in self.expected["calls"]),
                },
            )
            self.assertEqual(
                before,
                {
                    p.relative_to(self.root).as_posix(): p.read_bytes()
                    for p in self.root.rglob("*.py")
                },
            )
            applied = await self.apply(client, preview["result"]["plan_id"], "rename_symbol")
            self.assertEqual(applied["result"]["status"], "committed")
            for name, content in before.items():
                expected = (
                    content
                    if name in ("decoy.py", "hierarchy.py")
                    else content.replace(b"run_shared_cli", b"renamed_cli")
                )
                self.assertEqual((self.root / name).read_bytes(), expected)
            edited = await self.edit(client, self.module, [edit_range(1, 19, 1, 20, "2")])
            self.assertEqual(
                (await self.apply(client, edited["result"]["plan_id"]))["result"]["status"],
                "committed",
            )
            self.assertEqual(
                self.module.read_bytes(),
                b"def renamed_cli(value: int) -> int:\n    return value + 2\n",
            )
            after = await self.call(
                client,
                "definition",
                {"uri": self.caller.as_uri(), "position": {"line": 2, "character": 9}},
            )
            self.assertIn("return value + 2", after["result"]["locations"][0]["source"]["text"])
