# Implementation handoff — 2026-11-01

T0–T9 are implemented. **Stop before T10.**
Resume one bounded stage per session; the remaining specification and plan
are approved. Do not restart design review or execute the whole remaining plan.

## Branch and verification

Use feat/reference-parity in its existing isolated implementation worktree.
The original checkout's pending planning documents remain preserved.
T9 starts from f08cdd77f4f9258d6e967a94a28947863ee6ea81. Implementation checkpoint
058be37da9d54e310202881ab38f433fb4a70a3e passed all three hosted lanes in
[CI 41353143416](https://github.com/tvproductions/gz-mcp-lsp/actions/runs/41353143416),
including installed startup recovery and real ty mutation tests on macOS arm64
and Linux x86_64. The follow-up updates stage progress and this handoff.
Obtain its exact SHA/CI result from the final sync response or the
[branch Actions runs](https://github.com/tvproductions/gz-mcp-lsp/actions?query=branch%3Afeat%2Freference-parity).
A checkpoint's CI does not substitute for the final commit's CI.

The full suite discovers 164 tests. Complete local Windows/native Linux gates,
C901 source ceiling 20 and scoped portability audit pass. Windows runs explicit
disabled/unsupported startup denials; 25 POSIX-only tests are not applicable.
POSIX lanes skip only the Windows-specific unsupported-startup control.
Pins remain CPython 3.14.10, uv 0.13.6, MCP SDK 2.3.0 and ty 0.0.95.
Ordinary feature-branch sync is authorized; no merge, force-push, tag or release.

## Delivered and next stage

The catalog is **definition, references, diagnostics, hover, rename_symbol,
edit_file**. T9 supplies strict preview/apply schemas, destructive annotations,
bounded immutable previews, production startup recovery admission, reader-draining
apply, cancellation ownership, durable receipt lookup and semantic invalidation.
See the [T9 receipt](evidence/2026-11-01-mutations.md) and
[request/configuration guide](configuration.md#mutation-requests).

Writes remain disabled by default. Enabled writes require bounded operator roots
and private same-filesystem recovery storage on Linux x86_64/macOS arm64.
Windows writes are rejected. A model-supplied approval flag is never authority.
The source-free durable receipt is result; semantic_state is separate. A committed
disk transaction must never be reported rolled back because later LSP sync failed.

T10 has not started. Start only on the user's next continuation. Read its
[brief](superpowers/plans/2026-10-28-reference-parity.md#t10-public-document-symbols-workspace-symbols-and-implementations),
the specification, acceptance matrix and current policies.
Add exactly document_symbols, workspace_symbols and implementations, reusing T5's
internal symbol normalization. Keep workspace search/resolve under the existing
generation lease without selecting a synthetic URI. Preserve hierarchy, duplicates
and full/selection range distinctions; never invent positions for URI-only symbols.

## Remaining acceptance gaps

- T10 semantic extensions; T11 final installed/native nine-tool and mutation approval
  acceptance; T12 deeper engineering; T13 fresh whole-branch review, acceptance and
  deliberate stop. No fresh whole-branch review is claimed at this stage.
- T4 Codex 0.166.0 programmatic accept/deny proof remains partial H1–H3 evidence,
  not GUI/human-click or full native mutation acceptance.
- Windows-host/Linux-adapter bridging and operator-enabled native mutation
  scenarios remain unverified.
- Final fixtures must include shared_runtime/run_shared_cli and three importing/
  calling packages with independently enumerated positions.
- Cognitive qualification remains UNKNOWN; complexipy is not a passing authority.
  Native discovery retains duplicate/global-scope FAIL. Keep Backplane disabled,
  preserve caches/defaults, and do not treat Git sync as acceptance.

Use the [execution record](evidence/2026-11-01-execution.md), per-stage receipts
and ignored .superpowers/sdd/2026-10-28-reference-parity/ ledger/rulings.
Local helpers are not sole project authority; fresh checkouts use tracked fixtures.
Never publish private source, journals or transcripts.
