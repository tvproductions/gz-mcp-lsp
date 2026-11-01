# Approved plan execution â€” 2026-11-01

The user approved the revised implementation plan after its reviews: **"plan is
approved, proceed"**. This authorizes T0â€“T13 within the linked specification:
behavioral URI/position schemas, conservative saved-file consistency, disabled-by-
default guarded preview/apply, recoverable multi-file changes and initial POSIX
write scope. Required runtime, host and engineering evidence is not waived.
No merge, push, tag or release publication is authorized by execution approval.

Earlier planning/audit receipts retain their dated conclusions and hashes.
Current sources: [specification](../superpowers/specs/2026-10-28-semantic-navigation-design.md),
[plan](../superpowers/plans/2026-10-28-reference-parity.md),
[acceptance matrix](../discovery/acceptance-matrix.md).

Execution is isolated on branch feat/reference-parity from product base
922bd622e5d0d21f833eba70550c01fe07616a90. Approved pending planning changes were
carried into that worktree; the original checkout's pending documents were preserved.
Inline execution uses test-first task boundaries and a plan-specific local ledger.

## Current state

T0 runtime-input work is complete with native/cognitive gaps retained; T1 is complete; T2 is complete; T3 is complete; T4 implementation and its early Codex checkpoint are verified; T5 is next.
Partial production hover evidence exists; the complete runtime milestone is unaccepted.
See [runtime-input evidence](2026-11-01-runtime-inputs.md) for negative control,
SDK/dependency adoption, actual compatibility checks and native discovery failure. Baseline locked sync and the four
hooks passed on managed CPython 3.14.10 / uv 0.13.6 in the isolated worktree.

Selected SDK tag v2.3.0 resolves 2118f14f8a19bc158d8a1cf90af58d85d187f849.
Selected ty 0.0.95 resolves 48c5ea1baf6144dc9918ae60040aaa4198b251ce.
Official SDK metadata declares Python >=3.10, including 3.14 classification,
MIT licensing and Python-3.14-specific dependency markers. Actual compatibility
is being tested rather than inferred from metadata.

The upstream [cognitive-engine issue](https://github.com/tvproductions/gz-skills-first-starter/issues/1)
was rechecked OPEN. No qualified shared engine is available in its recorded
workflow; complexipy remains a defect reproducer. This remains an explicit
T0/T12 strict-acceptance blocker, not a substitute implementation task or waiver.

T1: [configuration/workspace evidence](2026-11-01-workspace-config.md) records
15 passing behavior tests and exact URI/byte/UTF-16 boundaries; no semantic or write
acceptance follows. The portability regression brings the total suite to 28 tests.

T2: [transport evidence](2026-11-01-transport.md) records eleven passing byte-stream
tests; the full suite now has 39 passing tests. Real ty/MCP interoperability is
not yet accepted.

T3: [lifecycle/CLI evidence](2026-11-01-session-cli.md) records 54 passing tests,
actual pinned-ty initialization/reaping, real MCP stdio startup/EOF and clean
installed CLI behavior. G1 still requires T4's production hover and generations.

T4: [documents/hover receipt](2026-11-01-documents-hover.md) records saved-byte
leases, stale-result controls, actual installed hover/dependency visibility and
full local Windows/Linux gates. The [native host checkpoint](2026-11-01-codex-feasibility.md)
observes programmatic native allow/deny with zero denied adapter calls and
supported Linux host access. Full H1-H3, macOS and new-branch hosted CI remain
unverified. T5 continues on this same production path.
