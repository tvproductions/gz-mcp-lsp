"""Installed six-tool parity through real stdio and the pinned ty executable."""

import hashlib
import os
import unittest

from tests.integration.mutation_support import InstalledMutationCase


def edit_range(start_line, start_character, end_line, end_character, text):
    return {
        "range": {
            "start": {"line": start_line, "character": start_character},
            "end": {"line": end_line, "character": end_character},
        },
        "new_text": text,
    }


@unittest.skipIf(os.name == "nt", "POSIX mutation integration; Windows denial runs separately")
class ActualMutationTests(InstalledMutationCase):
    async def test_real_multimodule_rename_retry_restart_and_semantics(self):
        module = self.root / "module.py"
        consumer = self.root / "consumer.py"
        decoy = self.root / "decoy.py"
        module.write_bytes(b"def shared(value: int) -> int:\n    return value + 1\n")
        consumer.write_bytes(b"from module import shared\nresult = shared(1)\n")
        decoy.write_bytes(b"def shared() -> str:\n    return 'decoy'\n")
        before = self.images()
        async with self.client() as client:
            preview = await self.call(
                client,
                "rename_symbol",
                {
                    "action": "preview",
                    "uri": module.as_uri(),
                    "position": {"line": 0, "character": 4},
                    "new_name": "renamed",
                },
            )
            self.assertEqual(
                {f["uri"] for f in preview["files"]}, {module.as_uri(), consumer.as_uri()}
            )
            self.assertEqual(before, self.images())
            committed = await self.apply(client, preview["plan_id"], "rename_symbol")
            self.assertEqual(committed["result"]["status"], "committed")
            inode = module.stat().st_ino
            retry = await self.apply(client, preview["plan_id"], "rename_symbol")
            self.assertEqual(retry["result"], committed["result"])
            self.assertEqual(module.stat().st_ino, inode)
            self.assertEqual(
                module.read_bytes(), b"def renamed(value: int) -> int:\n    return value + 1\n"
            )
            self.assertEqual(
                consumer.read_bytes(), b"from module import renamed\nresult = renamed(1)\n"
            )
            self.assertEqual(decoy.read_bytes(), before["decoy.py"][0])
            definition = await self.call(
                client,
                "definition",
                {"uri": consumer.as_uri(), "position": {"line": 1, "character": 9}},
            )
            self.assertEqual(definition["result"]["locations"][0]["uri"], module.as_uri())
            self.assertEqual(
                definition["result"]["locations"][0]["selection_range"]["start"],
                {"line": 0, "character": 4},
            )
            references = await self.call(
                client,
                "references",
                {
                    "uri": module.as_uri(),
                    "position": {"line": 0, "character": 4},
                    "include_declaration": True,
                },
            )
            self.assertEqual(len(references["result"]["locations"]), 3)
            diagnostic = await self.call(client, "diagnostics", {"uri": consumer.as_uri()})
            self.assertEqual(diagnostic["result"]["items"], [])
            hover = await self.call(
                client, "hover", {"uri": consumer.as_uri(), "position": {"line": 1, "character": 9}}
            )
            self.assertIn("renamed", str(hover["result"]["contents"]))
        async with self.client() as client:
            retry = await self.apply(client, preview["plan_id"], "rename_symbol")
            self.assertEqual(retry["result"], committed["result"])
            self.assertEqual(module.stat().st_ino, inode)

    async def test_insert_replace_delete_eof_exact_bytes_and_post_edit_queries(self):
        source = self.root / "a.py"
        source.write_bytes(b"value = 1\r\n")
        source.chmod(0o640)
        async with self.client() as client:
            preview = await self.edit(
                client,
                source,
                [
                    edit_range(0, 0, 0, 0, "# inserted\r\n"),
                    edit_range(0, 8, 0, 9, "2"),
                    edit_range(1, 0, 1, 0, "added = value\r\n"),
                ],
            )
            applied = await self.apply(client, preview["plan_id"])
            self.assertEqual(applied["result"]["status"], "committed")
            self.assertEqual(source.read_bytes(), b"# inserted\r\nvalue = 2\r\nadded = value\r\n")
            hover = await self.call(
                client, "hover", {"uri": source.as_uri(), "position": {"line": 2, "character": 8}}
            )
            self.assertIn("2", str(hover["result"]["contents"]))
            definition = await self.call(
                client,
                "definition",
                {"uri": source.as_uri(), "position": {"line": 2, "character": 8}},
            )
            self.assertEqual(
                definition["result"]["locations"][0]["selection_range"]["start"],
                {"line": 1, "character": 0},
            )
            deletion = await self.edit(client, source, [edit_range(2, 0, 3, 0, "")])
            await self.apply(client, deletion["plan_id"])
            self.assertEqual(source.read_bytes(), b"# inserted\r\nvalue = 2\r\n")
            diagnostic = await self.call(client, "diagnostics", {"uri": source.as_uri()})
            self.assertEqual(diagnostic["result"]["items"], [])

    async def test_rejected_set_and_stale_apply_change_zero_files(self):
        source = self.root / "a.py"
        source.write_bytes(b"value = 1\n")
        before = self.images()
        async with self.client() as client:
            base = {
                "action": "preview",
                "uri": source.as_uri(),
                "expected_hash": hashlib.sha256(source.read_bytes()).hexdigest(),
                "edits": [edit_range(0, 8, 0, 9, "2")],
            }
            outside = self.base / "outside.py"
            outside.write_bytes(b"private = True\n")
            rejected = [
                base | {"approved": True},
                base | {"expected_hash": "0" * 64},
                base | {"edits": [edit_range(0, 8, 0, 9, "2")] * 2},
                base | {"uri": outside.as_uri()},
                base | {"edits": [edit_range(0, True, 0, 1, "x")]},
                base | {"edits": [edit_range(99, 0, 99, 0, "x")]},
            ]
            for arguments in rejected:
                result = await client.call_tool("edit_file", arguments)
                self.assertTrue(result.is_error, result.content)
                self.assertEqual(before, self.images())
            preview = await self.edit(client, source, [edit_range(0, 8, 0, 9, "2")])
            source.write_bytes(b"value = 99\n")
            changed = self.images()
            result = await client.call_tool(
                "edit_file", {"action": "apply", "plan_id": preview["plan_id"]}
            )
            self.assertTrue(result.is_error)
            self.assertEqual(result.structured_content["error"]["code"], "STALE_DOCUMENT")
            self.assertEqual(changed, self.images())
            self.assertEqual(outside.read_bytes(), b"private = True\n")

    async def test_restart_expires_preview_and_noop_does_not_replace(self):
        source = self.root / "a.py"
        source.write_bytes(b"value = 1\n")
        async with self.client() as client:
            preview = await self.edit(client, source, [edit_range(0, 8, 0, 9, "2")])
        async with self.client() as client:
            stale = await client.call_tool(
                "edit_file", {"action": "apply", "plan_id": preview["plan_id"]}
            )
            self.assertEqual(stale.structured_content["error"]["code"], "PLAN_EXPIRED")
            noop = await self.edit(client, source, [])
            inode = source.stat().st_ino
            applied = await self.apply(client, noop["plan_id"])
            self.assertEqual(applied["result"]["status"], "no_op")
            self.assertEqual(source.stat().st_ino, inode)
            self.assertEqual(source.read_bytes(), b"value = 1\n")
