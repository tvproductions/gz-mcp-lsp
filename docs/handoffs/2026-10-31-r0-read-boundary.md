# R0 complete; resume with T10 — 2026-10-31

The user approved the revised read-first plan in conversation with “looks good”.
**R0 is complete; stop this package before T10.** On a new instruction to resume,
the next bounded package is Task 10: document_symbols, workspace_symbols and
implementations. Do not resume T8/T9. Preserve inline execution, one writer and
one package per handoff under the [approved plan](../superpowers/plans/2026-10-31-read-first.md).

Active workspace is `~/.codex/worktrees/359d/gz-mcp-lsp`, branch
implementation/reference-parity. The local commit containing this handoff follows
base 2685a9c982fe35328608deab0e6188aa53b34fe7; resolve exact current SHA from Git.
R0 implementation commit is 7554bd07eade2a5b6934dfdb0f92d6043fcf8cbd.
The original main checkout is unchanged. At R0 completion no implementation push
or exact-commit CI had been performed. The user then requested this resumable
handoff and Git sync; that authorizes an ordinary push of this implementation
branch, without merging main, publishing a release or advancing T10.

## Git sync and durable local state

The sync checkpoint containing this update follows R0 commit 7554bd0. Fetch before
resuming and compare HEAD with origin/implementation/reference-parity; inspect
GitHub Actions for that exact SHA. Sync observation is recorded after the push in
Git-common storage at `handoffs/2026-10-31-r0-sync/sync-receipt.json` and in the final
handoff response. This source document does not predict a successful push or CI.
GitHub retains exact-commit checks even when the local receipt is unavailable.

The sync candidate has no runtime changes after the source-hashed R0 gate, whose
four commands all passed. Reuse that same-input gate for this handoff-only update
and run normal commit hooks with uv 0.13.6. Observe Linux CI on the exact pushed
candidate separately; CI success does not establish the deferred metadata policy,
actual Codex acceptance, cognitive qualification or full write-safety acceptance.

Git-common `handoffs/2026-10-31-r0-sync/` also holds a byte-verified copy of the three
T9 drafts, both plans' progress ledgers and a manifest. Those files and ignored
test logs are **local only**, not included in the pushed branch. A new clone must
not assume those drafts/ledgers exist; use committed plans/evidence for context and
transfer the local backup explicitly if continuing the drafts elsewhere. A normal
restart in this worktree needs no restore. Never overwrite newer files from backup.

First action on resume: read AGENTS.md and this handoff, verify Git/source/draft
hashes and sync receipt, then take the T10 brief from the approved plan. Expected
package result is seven actual read tools with real-ty evidence and a new bounded
handoff. Stop before host-acceptance or write-parity packages unless separately
instructed. Preserve standing plan approval; do not ask for it merely after restart.

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
