# R0 complete; resume with T10 — 2026-10-31

The user approved the revised read-first plan in conversation with “looks good”.
**R0 is complete; stop this package before T10.** On a new instruction to resume,
the next bounded package is Task 10: document_symbols, workspace_symbols and
implementations. Do not resume T8/T9. Preserve inline execution, one writer and
one package per handoff under the [approved plan](../superpowers/plans/2026-10-31-read-first.md).

Active workspace is `~/.codex/worktrees/359d/gz-mcp-lsp`, branch
implementation/reference-parity. The local commit containing this handoff follows
base 2685a9c982fe35328608deab0e6188aa53b34fe7; resolve exact current SHA from Git.
The original main checkout is unchanged. No implementation push or exact-commit CI
was performed; do not infer remote backup, release or complete milestone acceptance.

Read [R0 evidence](../evidence/2026-10-31-r0-read-boundary.md) and its
[source-hashed receipt](../evidence/2026-10-31-r0-read-boundary.json), then the
[design](../superpowers/specs/2026-10-31-read-first-milestones-design.md) and plan.
The read-first ledger is `.superpowers/sdd/2026-10-31-read-first/progress.md`.
Historical T0–T8 records remain in the older plan's workspace; do not redo completed
tasks or claim the paused write work is accepted.

## Delivered and verified

Enabled-write JSON is rejected with UNSUPPORTED before ty launch/state access;
programmatic write-enabled MCP composition is also rejected. The source parser's
unreachable former write-authority branch was removed to retain the Lizard ceiling.
The four existing reads still work through actual ty without transaction startup,
source changes or recovery storage. Mutation previews remain unregistered.

Configuration 7/7 and MCP API 6/6 passed. Exact candidate gate exits 0/0/0/0;
outside-source installed actual-ty hover passed. Separate C901 and full runtime
Lizard passed, maximum 19. These checks are not actual Codex or seven-tool acceptance.

## Preserve and keep open

The three T9 drafts remain at src/gz_mcp_lsp/mutations.py, tests/test_mutations.py
and tests/integration/test_mutations.py, restored after candidate verification.
Their hashes still match the Git-common backup manifest at
handoffs/2026-10-31-t8-only/t9-drafts/manifest.json. Preserve them unchanged; use
the approved plan's explicit candidate isolation for future full gates. Do not
report the combined draft tree as the passing candidate or suppress its failures.

T8 remains incomplete: metadata loss, inherited-ACL/private-storage concerns and
unobserved Linux write/recovery require later write-parity work. No metadata policy
was approved. The earlier metadata question is deferred with writes, not blocking T10.
Linux read candidate execution, actual Codex dogfooding, qualified cognitive scoring
and whole-branch independent review remain separate outstanding evidence.

Dogfood this repository's real Python code through an externally installed adapter
at the later host-acceptance step. Use a disposable copy for change/failure tests;
retain synthetic fixtures as exact edge-case controls. No active host configuration
has been changed. T10 must leave seven read tools; full parity later requires nine.
