"""Pure preview planning: exact bytes, whole-set rejection and content identity."""

import unittest
from dataclasses import FrozenInstanceError, replace

from test_source_text import snapshot

from gz_mcp_lsp.edit_plan import plan_edits, plan_workspace_edit
from gz_mcp_lsp.models import AdapterError, Position, Range, TextEdit


def span(start, end):
    return {"start": {"line": 0, "character": start}, "end": {"line": 0, "character": end}}


class EditPlanTests(unittest.TestCase):
    """Every replacement refers to the same original immutable preimage."""

    def test_utf16_crlf_eof_and_original_snapshot(self):
        source = snapshot("a😀b\r\n")
        edited = plan_edits(source, [TextEdit(Range(Position(0, 1), Position(0, 3)), "x")])
        self.assertEqual(edited, b"axb\r\n")
        edits = [
            TextEdit(Range(Position(0, 0), Position(0, 1)), "long"),
            TextEdit(Range(Position(0, 3), Position(0, 4)), "tail"),
            TextEdit(Range(Position(1, 0), Position(1, 0)), "EOF"),
        ]
        self.assertEqual(plan_edits(source, edits), "long😀tail\r\nEOF".encode())
        self.assertEqual(source.data, "a😀b\r\n".encode())

    def test_adjacent_legal_overlap_and_coincident_inserts_rejected(self):
        source = snapshot("abcd\n")
        self.assertEqual(
            plan_edits(
                source,
                [
                    TextEdit(Range(Position(0, 0), Position(0, 2)), "x"),
                    TextEdit(Range(Position(0, 2), Position(0, 4)), "y"),
                ],
            ),
            b"xy\n",
        )
        for edits in [
            [
                TextEdit(Range(Position(0, 0), Position(0, 3)), "x"),
                TextEdit(Range(Position(0, 2), Position(0, 4)), "y"),
            ],
            [
                TextEdit(Range(Position(0, 2), Position(0, 2)), "x"),
                TextEdit(Range(Position(0, 2), Position(0, 2)), "y"),
            ],
        ]:
            with self.assertRaises(AdapterError) as failure:
                plan_edits(source, edits)
            self.assertEqual(failure.exception.code, "CONFLICT")

    def test_both_workspace_edit_forms_and_versions(self):
        source = snapshot("abc\n")
        changes = {"changes": {source.uri: [{"range": span(0, 1), "newText": "x"}]}}
        documents = {
            "documentChanges": [
                {
                    "textDocument": {"uri": source.uri, "version": 1},
                    "edits": [{"range": span(0, 1), "newText": "x"}],
                }
            ]
        }
        for value in (changes, documents):
            plan = plan_workspace_edit(value, {source.uri: source}, "generation")
            self.assertEqual(plan.after, (b"xbc\n",))
            self.assertEqual(plan.bases, (source,))
            for field in ("generation", "plan_id"):
                with self.assertRaises(FrozenInstanceError):
                    setattr(plan, field, "changed")
        documents["documentChanges"][0]["textDocument"]["version"] = 2
        with self.assertRaises(AdapterError) as failure:
            plan_workspace_edit(documents, {source.uri: source}, "generation")
        self.assertEqual(failure.exception.code, "CONFLICT")

    def test_resource_ops_duplicates_and_contradictory_forms_reject_whole_set(self):
        source = snapshot("abc\n")
        values = [
            {"documentChanges": [{"kind": "delete", "uri": source.uri}]},
            {"changes": {source.uri: []}, "documentChanges": []},
            {"changes": {source.uri: [], "file:///%73ample.py": []}},
        ]
        for value in values:
            with self.subTest(value=value), self.assertRaises(AdapterError):
                plan_workspace_edit(value, {source.uri: source}, "generation")
        self.assertEqual(source.data, b"abc\n")

    def test_annotations_and_base_identity_bound_to_digest(self):
        source = snapshot("abc\n")
        edit = {
            "changes": {source.uri: [{"range": span(0, 1), "newText": "x", "annotationId": "a"}]},
            "changeAnnotations": {"a": {"label": "rename", "needsConfirmation": True}},
        }
        first = plan_workspace_edit(edit, {source.uri: source}, "generation")
        edit["changeAnnotations"]["a"]["label"] = "different"
        second = plan_workspace_edit(edit, {source.uri: source}, "generation")
        self.assertNotEqual(first.plan_id, second.plan_id)
        moved = replace(source, identity=replace(source.identity, inode=99))
        third = plan_workspace_edit(edit, {source.uri: moved}, "generation")
        self.assertNotEqual(second.plan_id, third.plan_id)

    def test_limits_and_surrogate_split_are_errors(self):
        from gz_mcp_lsp.config import Limits

        source = snapshot("a😀b\n")
        with self.assertRaises(AdapterError):
            plan_edits(source, [TextEdit(Range(Position(0, 2), Position(0, 3)), "x")])
        edit = {"changes": {source.uri: [{"range": span(0, 1), "newText": "too large"}]}}
        with self.assertRaises(AdapterError) as failure:
            plan_workspace_edit(
                edit,
                {source.uri: source},
                "generation",
                limits=replace(Limits(), max_staged_bytes=1),
            )
        self.assertEqual(failure.exception.code, "LIMIT_EXCEEDED")

    def test_low_level_plan_has_an_allocation_bound(self):
        source = snapshot("a")
        edits = [
            TextEdit(Range(Position(0, 0), Position(0, 1)), "x" * 1048576),
            TextEdit(Range(Position(0, 1), Position(0, 1)), "y" * 1048577),
        ]
        with self.assertRaises(AdapterError) as failure:
            plan_edits(source, edits)
        self.assertEqual(failure.exception.code, "LIMIT_EXCEEDED")

    def test_lone_cr_and_mixed_lsp_newlines(self):
        source = snapshot("ab\rcd\r\n")
        result = plan_edits(source, [TextEdit(Range(Position(1, 0), Position(1, 1)), "X")])
        self.assertEqual(result, b"ab\rXd\r\n")

    def test_public_table_and_zero_filesystem_effects(self):
        import json
        from pathlib import Path
        from unittest.mock import patch

        cases = json.loads((Path(__file__).parent / "fixtures" / "edit_cases.json").read_text())
        for case in cases:
            source = snapshot(case["source"])
            edit = TextEdit(
                Range(Position(*case["start"]), Position(*case["end"])), case["new_text"]
            )
            with (
                patch("builtins.open", side_effect=AssertionError("planner attempted IO")),
                patch("os.open", side_effect=AssertionError("planner attempted IO")),
                patch("os.replace", side_effect=AssertionError("planner attempted mutation")),
            ):
                self.assertEqual(plan_edits(source, [edit]), case["expected"].encode())
