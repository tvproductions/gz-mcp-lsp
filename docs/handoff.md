# Implementation handoff — 2026-11-01

Resume **one bounded stage per session**. T0–T7 are complete; **T8 has not started**.
The specification and remaining implementation scope are approved. Do not
restart design review or run the entire remaining plan in one continuous session.

## Branch and verification

Use feat/reference-parity. The implementation checkpoint before this handoff is
a976991782594f145558719bdd24c75121bf41da, based on
922bd622e5d0d21f833eba70550c01fe07616a90. Implementation used an isolated managed
worktree; the original checkout's pending planning documents remain preserved.

The user now authorizes this handoff and ordinary synchronization of the feature
branch. No main merge, force-push, tag/release or T8 execution follows. Verify the
exact pushed commit's [Actions run](https://github.com/tvproductions/gz-mcp-lsp/actions?query=branch%3Afeat%2Freference-parity).
The final sync response records SHA/CI outcome without receipt-only commit chains.

Latest local verification: **114 tests**, complete Windows and native Linux/WSL
gates, C901 src and scoped portability checks pass. Pins: managed CPython 3.14.10,
uv 0.13.6, MCP SDK 2.3.0, ty 0.0.95. Hosted platform conclusions must come from
the exact-commit CI result; they are separate from local receipts.

## Delivered

T0–T3: official SDK, JSON/workspace primitives, bounded byte transport, supervised
one-ty lifecycle and installed stdio CLI. T4: saved-document/generation/read/
exclusive leases and early actual Codex hover/approval feasibility. T5: exact
navigation and complete authorized source. T6: current pull diagnostics and
identity-bound caching. T7: immutable zero-IO edit plans.

The public catalog is **definition, references, diagnostics, hover**. Filesystem
transactions, recovery, mutation tools and semantic extensions remain absent.
Writes remain disabled by default; initial write platforms are Linux x86_64 and
macOS arm64, never Windows. No final release or whole-branch review is claimed.

## Next bounded session: T8 only

Read the [T8 brief](superpowers/plans/2026-10-28-reference-parity.md#t8-guarded-posix-filesystem-transactions-and-durable-recovery),
[write-safety specification](superpowers/specs/2026-10-28-semantic-navigation-design.md),
[acceptance matrix](discovery/acceptance-matrix.md), AGENTS.md and adopted policies.

Implement Transactions(config, workspace): recover(), apply(plan), receipt(plan_id).
Own private journal/state locking, all-target preflight, directory-relative
no-follow operations, verified before/after staging, durable receipts, safe
rollback and crash recovery. Import no SDK/LSP modules. Preserve modes, reject
unsafe paths/links/resource operations and never overwrite a newer external writer.

Write T8's named failing tests first: replacement failures, external rollback
conflicts, replay/lost responses, quota/corrupt journals and subprocess crashes.
Windows must explicitly reject writes with unchanged source. Separate Linux/macOS
safety evidence is required. Finish T8's reviewed commit and hand back before T9.

T7 seam: frozen EditPlan(plan_id, generation, tuple files, expires_at, tuple
annotations); PlannedFile(uri, before Snapshot, after bytes, tuple edits); frozen
PlannedEdit and ChangeAnnotation. plan_edits/plan_workspace_edit take keyword-only
limits; the latter supports explicit expiry. plan_payload/plan_digest bind actual
and claimed before hashes, after hashes, identity/mode/version, edits, expiry and
annotations. Staging counts before plus after bytes. Digest is not consent/authority.

Generation combines scan digest and transport epoch; semantic inputs must be
tracked. Documents.exclusive() drains readers before preflight; its drain timeout
ends before the transaction body. T9 later owns startup recovery/admission and
commit/rollback shielding. Do not implement later stages incidentally during T8.

## Remaining gates and continuation aids

- T9: mutation tools/startup recovery; T10: three semantic extensions; T11: full
  installed/native nine-tool and mutation approval evidence; T12: deeper engineering;
  T13: fresh whole-branch review, acceptance and deliberate stop.
- T4 used actual Codex 0.166.0 model-driven approval with a programmatic client:
  accept returned int; decline sent zero adapter calls. This is neither GUI/human
  click evidence nor full H1–H3 mutation acceptance.
- Native Linux WSL access exists. Windows-host/Linux-adapter bridging and actual
  operator-enabled mutation scenarios remain unverified.
- T5's three root-module consumers are development evidence. Final fixtures must
  also include shared_runtime/run_shared_cli and three importing/calling packages
  with independently enumerated call/import positions.
- Cognitive qualification remains UNKNOWN; complexipy is not a passing authority.
  Native discovery has duplicate/global-scope FAIL. Keep Backplane disabled and
  preserve caches/defaults. Git sync does not resolve these acceptance gaps.

Use the [execution record](evidence/2026-11-01-execution.md) and per-stage receipts.
Their hashes identify dated inputs; later commits do not inherit earlier receipts.
The existing worktree's ignored .superpowers/sdd/2026-10-28-reference-parity/ holds
the complete task ledger/rulings, local handoff, native probe and Linux gate helper.
These are local aids, not sole project authority. Fresh checkouts provision tools/
fixtures from tracked sources. Never publish private transcripts or local paths.
