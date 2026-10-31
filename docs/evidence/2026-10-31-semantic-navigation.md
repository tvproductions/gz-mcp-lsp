# First semantic navigation evidence — 2026-10-31

Approved Tasks 3–5 joint interoperability gate, macOS arm64, managed CPython
3.14.10 and locked ty 0.0.93 / MCP SDK 2.3.0. Independent Python implementation;
only synthetic public fixture sources in tests/fixtures/semantic_workspace.

Actual stdio SDK client negotiates MCP with the Python executable, lists implemented
tools, invokes definition/references/hover, and receives structured JSON identical
to text content. Actual ty child handles all semantic requests. Definition includes
complete authorized declaration source; hover retains type/signature text.

The fixture definition is sample/runtime.py, zero-based line 3, character 4.
Adapter references and a direct ty identifier query agree exactly:

| Consumer | Zero-based line | UTF-16 character |
| --- | --- | --- |
| sample/inventory.py | 2 | 9 |
| sample/registration.py | 2 | 9 |
| sample/rotation.py | 2 | 9 |

The sample/decoy.py function and its caller are absent. include_declaration=true
includes runtime.py. Direct keyword control at character 0 returns null (empty
semantic result), while the identifier returns three callers. No +4 adjustment,
workspace-symbol-derived position or private source is used.

Actual ty restart tests observe unopened dependency source changes, creation,
rename/deletion and configuration changes. Before/after scope hashes and process
reaping are asserted; references reflect the created/changed consumer. No readiness
sleep, mocked result or tool registration is used as semantic success evidence.

Unit checks additionally cover full/selection LocationLink separation, decorated
nested async source, constants after astral Unicode, AST UTF-8 columns versus
UTF-16, external metadata-only source, null/markup hover forms, numeric location
ordering, result-cap rejection, generation races, open-once/eviction and negotiated
full/incremental didChange forms. Artifact verification now installs the wheel in a
clean outside-checkout environment and invokes actual semantic hover through MCP
and configured ty, with no source-path injection or dev dependency masking.

SDK qualification demonstrated coercion of Boolean/float/string coordinates by
its default dataclass input validation. pydantic 2.14.2 (already SDK-transitive,
MIT) is now an explicit pinned boundary-only dependency for strict input fields;
there is no new dependency resolution or domain coupling. Strict rejection is
verified via SDK call_tool, rather than trusting JSON schema declarations.

Ruff check/format, ty, unittest, archive/install checks and separately run C901 and
Lizard pass for this increment. Protocol stubs use documented multiline bodies so
Lizard discovers the same functions as CPython AST; checker/ceilings unchanged.
Cognitive qualification remains UNKNOWN and blocks strict acceptance. Diagnostics,
write operations, three extension tools, crash recovery and actual Codex host proof
are not yet accepted. This is a bounded capability receipt, not milestone completion.
