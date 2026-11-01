# T9 mutation tools and startup recovery â€” 2026-11-01

User continuation authorized T9 only from
f08cdd77f4f9258d6e967a94a28947863ee6ea81. Stop before T10.
The official SDK now exposes all six parity tools; mutation tools always carry
readOnlyHint=false, destructiveHint=true and openWorldHint=false.

## Delivered contracts

Mutations owns bounded in-memory previews and composes Documents, Session and
Transactions. Preview never writes source or creates a transaction. Rename uses
exact URI/UTF-16 position, prepareRename when advertised and the actual ty
WorkspaceEdit. Explicit file edits require the saved SHA-256 hash. Complete
target sets, versions, ranges, aliases, annotations and resource-operation
rejections remain governed by the pure planner. Retained immutable previews are
bounded by configured count/TTL and generation. Apply never recomputes an edit.

Production lifespan completes authorized recovery before starting the semantic
session or admitting mutation calls. Disabled/unsupported startup performs no
source restoration. Corrupt, unreadable or conflicting recovery state becomes
persistent RECOVERY_REQUIRED admission lockout. Pending recovery cancellation
retains its IO owner until cleanup completes, including when that IO later fails.

Apply looks up durable receipts before session/preview/expiry checks. It then
drains readers, validates the retained generation without restarting ty and
shields only the admitted disk transaction plus semantic invalidation. Draining
remains cancellable and times out with zero writes. Semantic readers cannot
observe a partial commit or trigger a concurrent generation restart.

The durable receipt is nested in result; semantic_state is separate. Committed
disk changes remain committed when later synchronization fails, with
semantic_state=unavailable and old transport invalidation. Subsequent semantic
reads use a new generation or fail. Receipt retries never reapply. Preview
conservatively reserves the complete eventual receipt response budget.

## Evidence and decisions

- Eleven initial service assertions failed before mutations.py existed; six SDK
  admission/catalog tests failed before production wiring. Unit green preceded
  installed startup tests.
- Before-commit cancellation, cancelled recovery IO failure and receipt-budget
  negative controls each reproduced their defect before correction.
- Real SDK cancellation while a test transaction is held retains a durable
  receipt and retry invokes apply exactly once.
- Installed native Linux tests use an outside-checkout wheel, actual stdio and
  pinned ty. Multi-module rename verifies complete expected targets, same-name
  decoy exclusion, exact after-bytes and post-edit definition/references/hover/
  diagnostics. File edits cover insert/replace/delete/EOF with CRLF and mode
  preservation. Rejected/stale previews change no source.
- Disposable subprocesses seed partial/committed transactions. The installed CLI
  itself restores safe entries before preview, finalizes committed receipts,
  locks real preview/apply for corrupt or externally changed state, and preserves
  receipts across EOF cleanup/restart. A production-lifespan barrier separately
  proves pending recovery cancellation and safe restart without runtime test hooks.
- Windows runs disabled and unsupported-enabled startup denials; 25 POSIX-only
  tests are explicitly not applicable. POSIX lanes skip only the Windows-specific
  startup denial. Required POSIX capabilities never silently skip.
- Reuse the pure planner's target parser and existing owned-IO helper rather than
  duplicate WorkspaceEdit policy or release admission while a worker still runs.
- Advertise prepareRename and annotation parsing, but do not advertise authenticated
  confirmation handling. LSP's
  [rename capability](https://github.com/microsoft/language-server-protocol/blob/gh-pages/_specifications/lsp/3.18/language/rename.md)
  describes honoring confirmation; this adapter has no authenticated host consent
  signal. Returned labels/needs_confirmation remain preview-visible and digest-bound.
- Test provisioning remains before requests. No runtime installation, application
  environment settings, generic filesystem operations or second server was added.

Full local Windows/Linux gates pass on the implementation; the final SDK
cancellation control also passes on Windows. The suite discovers 164 tests.
Ruff, ty, C901 source ceiling 20 and scoped portability audit pass.
Hosted macOS arm64 and exact-commit three-platform CI remain required before
reporting T9 complete. The final bounded handoff will identify the completion
checkpoint without a CI receipt-only commit chain.

G2 software parity evidence does not waive native host H1-H3, T10 extensions,
T11 final fixtures/installed acceptance, T12 engineering gaps or T13 final review.
Cognitive qualification/native discovery remain unresolved. No release is accepted.
