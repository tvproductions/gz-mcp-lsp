# Implementation handoff — 2026-11-01

T0–T8 are implemented. **Stop before T9**, as requested by the user.
Resume one bounded stage per session; the specification and remaining scope
are approved. Do not restart design review or execute the whole remaining plan.

## Branch and verification

Use feat/reference-parity and its existing isolated implementation worktree.
The original checkout's pending planning documents remain preserved.
T8 started from 22fb1ddb9af949aba9a3a91d23cd4ef522ad7d0f; its adapter checkpoint
ea02dfabb4b31df7672e88d4016d10b25e644441 passed all three hosted lanes in
[CI 41333910261](https://github.com/tvproductions/gz-mcp-lsp/actions/runs/41333910261).
The final follow-up adds strict lockout-schema validation and explicit UTF-8
subprocess diagnostic decoding. Obtain its exact SHA/CI result from the final
sync response or the [branch's Actions runs](https://github.com/tvproductions/gz-mcp-lsp/actions?query=branch%3Afeat%2Freference-parity).
Do not substitute the checkpoint's CI for a later commit.

The final local suite discovers 131 tests. The complete Windows and native
Linux/WSL gates, C901 source ceiling 20 and scoped portability audit pass.
Windows runs zero-write denial and marks 16 POSIX-only tests not applicable.
Pins remain CPython 3.14.10, uv 0.13.6, MCP SDK 2.3.0 and ty 0.0.95.
Ordinary feature-branch sync is authorized; no merge, force-push, tag or release.

## Delivered and next stage

T0–T7 provide the official SDK boundary, JSON/workspace primitives, bounded
transport, one-ty lifecycle/CLI, saved generations/read/exclusive leases,
definition/references/diagnostics/hover and immutable edit plans.
T8 adds internal Transactions(config, workspace): recover(), apply(plan),
receipt(plan_id), private journal/state locking, all-target preflight,
descriptor-relative no-follow staging/replacement, verified rollback and
durable recovery/retry receipts. See the [T8 receipt](evidence/2026-11-01-transactions.md).
Writes are disabled by default and supported only on guarded local Linux
x86_64/macOS arm64 filesystems. Windows writes are rejected.

The public catalog remains **definition, references, diagnostics, hover**.
T9 has not started: production startup recovery, mutation admission and
rename/edit MCP wrappers are absent. Start only on the user's next continuation.
Read the [T9 brief](superpowers/plans/2026-10-28-reference-parity.md#t9-renameedit-mcp-tools-and-post-commit-semantics),
write-safety specification, acceptance matrix and current project policies.
Use Documents.exclusive() to drain readers before preflight, coordinate recovery
before mutation admission, shield commit/rollback, and invalidate semantic
generations after disk outcomes. A durable committed receipt must never be
reported as rolled back because later LSP synchronization fails.

## Remaining acceptance gaps

- T9 mutation/startup integration; T10 bounded semantic extensions; T11 installed
  nine-tool/native mutation approval; T12 deeper engineering; T13 fresh whole-branch
  review, acceptance and deliberate stop. No whole-branch review is claimed now.
- T4 Codex 0.166.0 programmatic accept/deny proof is partial H1–H3 evidence,
  not GUI/human-click or full mutation acceptance.
- Windows-host/Linux-adapter bridging and operator-enabled native mutation
  scenarios remain unverified.
- Final fixtures must include shared_runtime/run_shared_cli and three importing/
  calling packages with independently enumerated positions.
- Cognitive qualification remains UNKNOWN; complexipy is not a passing authority.
  Native discovery retains duplicate/global-scope FAIL. Keep Backplane disabled
  and preserve caches/defaults. Git sync does not waive these gaps.

Use the [execution record](evidence/2026-11-01-execution.md), per-stage receipts
and ignored .superpowers/sdd/2026-10-28-reference-parity/ ledger/rulings.
Local helpers are not sole project authority; fresh checkouts use tracked fixtures.
Private source, journals and transcripts must never enter this public repository.
