# Project handoff — 2026-11-11

## Resume here: T12 cognitive closure; stop before T13

Resumed from `ee2e86e84af24559b288ece169fac728093c23c8` on **main in the primary
checkout**. T12 now has reviewed import contracts, correction of all five
pre-existing Lizard ceiling violations, full deeper measurements and fresh
actual Codex evidence on the November 11 runtime inputs. See the
[T12 engineering receipt](evidence/2026-11-11-engineering-acceptance.md) and
[structured evidence](evidence/2026-11-11-engineering-acceptance.json).
The final response supplies this save point's exact commit, Git/CI results and
remaining workspace state; do not create a receipt-only follow-up commit.

**G5/T12 is still incomplete.** The required independently qualified shared
cognitive engine is unavailable. Starter issue #1 remains OPEN/unscheduled.
Current gzkit source changed, but no separately versioned shared engine was
found at its inspected package boundary. Owner: project/starter maintainer;
external condition: gzkit delivers a versioned engine/API that can pass the
42 independent qualification fixtures and actual corpus gate at ceiling 15.
Complexipy remains a defect reproducer. No substitute scorer, whole-gzkit
lifecycle dependency or threshold waiver was introduced. **Do not begin T13.**

Concrete results:

- Four Import Linter contracts pass and reject injected violations: SDK boundary,
  semantic access through Session/Documents, filesystem isolation and planner
  isolation. No routine hook or dependency was added.
- Lizard passes all 20/20/20 ceilings on `src tests tools/engineering`: 648
  functions, maximum 20, weighted mean 3.1944444444444446; C901 also passes.
  The changes extract existing validation/initialization responsibilities and
  preserve errors, ordering and public behavior. Fresh bounded stage review
  reported no consequential defect; this is not T13's whole-milestone review.
- Deeper tools are measured and findings reviewed. Bandit retains nine LOWs;
  Interrogate records 41.9% presence, not an adopted default floor. Cohesion and
  Vulture candidates are reviewed. deptry and the 99-package hashed all-group
  vulnerability audit pass. Analyzer utility tests: 29 pass.
- Coverage: 87.1691% statements, 74.4444% branches, zero exclusions; parent
  process only, with installed/crash children functionally tested separately.
  Three new budget/Unicode/nonfinite-JSON tests close five survivor gaps;
  bounded product Cosmic Ray rerun kills 13/13 with source restored.
- Actual codex-cli 0.167.1 on macOS arm64 uses the installed runtime-only adapter,
  MCP 2.3.0 and ty 0.0.101. A model turn invokes/asserts all seven read tools;
  native disabled denials, rename/edit preview/decline/accept, exact complete
  byte maps and fresh post-edit declaration source pass. Native ty death,
  adapter death, 2-second host timeout and parent EOF preserve hashes/reap both
  observed PIDs. Decisions are supplied by the test client, not GUI/human clicks.
- The source/test suite now discovers 189 tests. POSIX skips one Windows-only
  rejection test; Windows excludes 26 narrowly POSIX-only tests. The final
  synchronization response is the authority for exact-commit hosted results.
  An earlier moving-input gate failed two installed mutation cases; both passed
  unchanged in focused and full coverage reruns. No cause is inferred from
  system load alone and no test/runtime deadline was weakened.

Keep Python **3.14.10**, MCP **2.3.0**, ty **0.0.101**, uv **>=0.13.6** (CI
**0.13.7**), uv_build **0.13.7**, starter **0.9.0**, Superpowers **7.0.2**,
gz-skills **0.10.1** and **disabled Backplane 0.2.0**. Lite remains selected;
native caches and unrelated defaults are preserved. The first unpublished
product remains **0.1.0** under ROADMAP.md. No release/tag is authorized.

Next work is bounded to obtaining/qualifying the shared cognitive candidate and
measuring the real corpus, then rechecking affected acceptance inputs. If upstream
is still unavailable, preserve UNKNOWN; do not repeat all completed T12 work just
to rediscover the same external condition. A changed engine/runtime requires
applicable fresh verification. Only after G5 closes may the authorized next
session proceed to T13 review/acceptance and deliberate stop.

## Retained implementation checkpoint — 2026-11-01

**T0-T11 implemented, with actual installed/native host evidence. Stop before T12.**
T11 commit `05aa14b9885e511f04340e422298d784e8a74174` passed
[three-platform CI](https://github.com/tvproductions/gz-mcp-lsp/actions/runs/41358262222).
The user requested T11 completion and
instructed that accepted branches/worktrees be merged to main and removed.

## Workspace and verified checkpoints

Continue on **main in the primary checkout** from the maintenance checkpoint above.
Historically, T10 is `a71bcd445f47dac46a43812b9c996cb87b71bfd0`; T11 adds tests, distribution
checks, host examples and evidence without changing that runtime source tree.
The final response identifies the T11 commit, exact-commit three-platform CI,
local/remote SHA alignment and branch cleanup. No tag or release is authorized.

[T11 evidence](evidence/2026-11-01-codex-acceptance.md) and its
[sanitized native receipt](evidence/2026-11-01-codex-acceptance.json) record actual
observations. Raw host transcripts remain private and untracked. The
[consolidation record](evidence/2026-11-01-main-consolidation.md) preserves both
older histories, the independent read-first implementation and archived planning
files/ledgers. Do not restore superseded status over current evidence.

## Implemented contracts and seams

The catalog is exactly definition, references, diagnostics, hover, rename_symbol,
edit_file, document_symbols, workspace_symbols and implementations.

- Documents owns saved-file generation admission, reader/exclusive draining,
  final manifest validation and post-commit synchronization/invalidation.
- Navigation preserves exact identifier positions, hierarchy, duplicate symbols,
  full/selection ranges and honest unresolved URI-only symbols. Workspace search
  holds generation() through advertised resolution, normalization and final checks;
  it never opens a synthetic document. External targets are marked metadata.
- Diagnostics uses current pull reports and identity-bound caching. EditPlan
  values are immutable; complete WorkspaceEdits are validated without planner IO.
- Transactions owns private journals, same-filesystem staging, state locking,
  exact bytes/modes, safe rollback, durable receipts and conservative recovery.
- Mutations retains bounded previews and composes those services. Production
  startup finishes authorized recovery before mutation admission.

All successes use schema_version, operation, position_encoding, result,
workspace_generation, documents and complete. Preview metadata is under result:
result.plan_id, result.files and result.annotations. Apply result is the durable
disk receipt; semantic_state is separate. A semantic synchronization failure
cannot relabel committed disk writes as rolled back.

Writes default to disabled. Enabled writes require bounded operator roots and
private same-filesystem state on Linux x86_64/macOS arm64; Windows writes remain
unsupported. Plan identity is not authenticated human consent. Model approval
flags are rejected. Native host approval is separate from operator authority.
The adapter lock does not serialize independent writers; use a quiescent workspace.

## T11 verification and host proof

The suite discovers **186 tests**. Windows excludes **26 POSIX-only tests**;
POSIX excludes the one Windows-only unsupported-write test. Local Windows/Linux
four-hook gates, source-independent build, outside-source distribution verification
and scoped C901 pass. Hosted CI prints the complete platform skip inventory;
verify the exact final SHA's Linux x86_64/macOS arm64/Windows AMD64 results using
the immutable run link in the final response. Missing ty is never a passing skip.

Installed runtime-only tests assert exact import origin, no development masking,
all seven read outcomes, both disabled denials, and supported POSIX rename/edit
bytes followed by fresh semantics. The shared_runtime/run_shared_cli fixture has
three importing/calling packages with independent positions and a same-name decoy.

Actual codex-cli 0.166.0 on Windows launches the installed Linux adapter through
WSL Ubuntu-26.04 with native-local workspace/state. Fresh actual model turns
invoke all seven read tools and semantically assert results. Native mutation
preview/apply receives accept/decline/accept/accept/accept: declined apply leaves
recursive hashes unchanged and sends zero additional adapter tool calls. Both
accepted mutations have exact after-bytes and fresh post-edit declaration source.
These are real native protocol decisions supplied by the test client, **not GUI
or human-click evidence**. No direct SDK test is relabeled as native host proof.

Actual host timeout (2 seconds), ty death, adapter death and normal unsubscribe/
parent EOF leave hashes unchanged where appropriate and reap the adapter and ty.
All observed app-server exits are zero. Persistent host config, native caches,
Backplane and unrelated defaults remain unchanged. Isolated examples live under
docs/examples/; no engineering plugin registration was added.

Keep CPython **3.14.10**, MCP SDK **2.3.0** and ty **0.0.101**.
uv accepts **>=0.13.6**, with CI testing **0.13.7**; supported callers need not
match CI. Nested hooks must resolve the selected uv consistently. See the
[compatibility backport](evidence/2026-11-11-uv-compatibility.md). Required gate:

```text
uv sync --locked --all-groups
uv run --locked pre-commit run --all-files
uv build --no-sources
uv run --locked python tools/verify_distribution.py
```

The four hooks remain Ruff check, Ruff format, ty and unittest. No pytest,
application environment overrides, request-time installation, second server,
generic filesystem operations or unsolicited LSP applyEdit.

## Remaining acceptance

The current T12 receipt above supersedes the former T12 entry checklist. T0–T11
records below retain their historical runtime versions and limits; current T12
native behavior is separately observed. Required cognitive qualification remains
UNKNOWN and blocks G5/E3/E4 and terminal acceptance. T13 remains NOT RUN.

Use the [execution record](evidence/2026-11-01-execution.md),
[T12 receipt](evidence/2026-11-11-engineering-acceptance.md),
[acceptance matrix](discovery/acceptance-matrix.md) and
[request guide](configuration.md). Raw native transcripts, temporary probes and
the task ledger are private/ignored under
`.superpowers/sdd/2026-10-28-reference-parity`. Use gh for GitHub reads/writes
and git for repository synchronization. Never publish private paths or transcripts.
