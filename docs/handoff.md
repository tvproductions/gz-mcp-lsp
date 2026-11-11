# Project handoff — 2026-11-11

## Resume here: T12 after dependency maintenance

The latest user request is to **write the handoff and Git-sync it** after
dependency maintenance and identifying T12 as the next backlog item. Work is
on **main in the primary checkout**, based on maintenance commit
`1f8b16e28c452e1367e666e02963b750a6a4ec81`. This save point changes documentation
and evidence only; it does not execute T12 or authorize T13.

The preceding user-authorized full update started at `397d48d`. The full
[maintenance receipt](evidence/2026-11-11-dependency-update.md) and
[version/source inventory](evidence/2026-11-11-dependency-update.json) record
selected inputs, checks, rollback and remaining engineering findings.
Maintenance commit `1f8b16e` passed
[exact-commit Linux/macOS/Windows CI](https://github.com/tvproductions/gz-mcp-lsp/actions/runs/43035668745).
Each platform discovered 186 tests; Linux/macOS skipped the one Windows-only
test, and Windows skipped 26 POSIX-only tests. Local gates, normal commit hooks,
source-independent build and outside-source distribution verification passed.
The final response supplies this handoff commit's own Git/CI results; do not
create a follow-up commit solely to record that response.

Current selections: starter **0.9.0**, Superpowers **7.0.2**, gz-skills **0.10.1**,
and **disabled Backplane 0.2.0**. The lite profile, product-owned marketplace,
standalone-source exclusion and user defaults are preserved. Complete cached
source trees match the three published target revisions. The native manager's
scoped marketplace refresh completed without errors; installed source refs now
match all three project selections. Fresh discovery finds 20 project gz-skills
entries from starter 0.10.1, zero duplicate names and zero errors. Outside-project
discovery remains 20 standalone 0.8.3 entries. User configuration is byte-unchanged.
Source reconciliation is closed for this observed Codex host; it does not prove
fresh model/approval behavior on the changed runtime set.

Managed Python remains **3.14.10** and runtime MCP remains **2.3.0**. The project
accepts uv **>=0.13.6** and tests **0.13.7**; uv_build is **0.13.7**. Ruff is
**0.17.4**, ty **0.0.101**, Coverage **7.17.2**, Import Linter **2.16**, Cosmic Ray
**8.9.0** and Lizard **1.26.0**. The full uv lock was regenerated. A late PyPI ty
release superseded the initial 0.0.100 candidate during verification.

The Lizard counting contract is preserved after identical old/new measurements
on 70 Python files and the 29 utility regressions. Its five existing function
ceiling failures remain failures. Bandit, documentation coverage, Vulture and
missing import-boundary contracts remain explicit T12 work; the cognitive
engine is still unavailable. No threshold was weakened and no product runtime
capability was added. The mutation timeout test now restores its normal budget
before a subsequent read; the 50 ms drain assertion remains intact.

The first unpublished product release remains **0.1.0**, with finite scope and
remaining gates in [ROADMAP.md](../ROADMAP.md). No tag or release is authorized.
This maintenance does not complete T12/T13 or turn historical native model/approval
proof into fresh proof for the changed ty/dependency set. Continue with the
existing T12 brief below and preserve all required UNKNOWN/FAIL results.

**First next-session action:** read the T12 brief and current acceptance matrix,
inspect actual module imports, then add reviewed Import Linter contracts for
the SDK-only boundary, semantic-to-port direction and filesystem isolation.
Continue within T12: correct/review the five Lizard ceiling failures, review
Bandit/Vulture/cohesion/docstring findings, collect final-input statement/branch
coverage and bounded product mutation evidence, and reconcile every acceptance
row with current observations. The maintenance Cosmic Ray proof used disposable
fixtures, and its 90% coverage run used the earlier ty 0.0.100 candidate; neither
is final-input T12 acceptance. Recheck the shared cognitive engine upstream;
if unavailable, name its owner/external condition and retain UNKNOWN rather
than substituting complexipy. Stop before T13.

Handoff verification also observed intermittent local timing failures: the first
normal commit hook completed 186 tests in 501 seconds with timeouts in diagnostics,
typed child startup and empty/changed-workspace symbol negotiation. All three
passed unchanged in a focused 50-second rerun. Host load exceeded 129 on ten
logical CPUs; contention is a correlation, not a demonstrated root cause. No
deadline, assertion or runtime code was changed. Retain this observation for
T12 if it recurs; the complete normal hooks must pass before this save point
is synchronized, and its final CI result belongs in the final response.

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

## Next authorized stage: T12 only

Read README.md, AGENTS.md, AGENTS.skills-first.md, current design-revision evidence,
adopted engineering policies, specification/plan and acceptance matrix. Use the
[T12 brief](superpowers/plans/2026-10-28-reference-parity.md#t12-full-affected-input-engineering-acceptance-and-plan-reconciliation).

1. Run effective interpreter/tool/source provenance and the complete required gate.
2. Run the adopted deeper analyzers against explicit actual runtime/test scopes:
   C901, qualified cognitive scoring, Lizard, cohesion, Interrogate, Vulture,
   Bandit, statement/branch coverage, bounded Cosmic Ray, deptry, pip-audit and
   Import Linter. Add reviewed import boundary contracts; no new capabilities.
3. Recheck upstream cognitive qualification and execution-host native discovery/
   configured Git-source refresh. If required closure is unavailable, retain
   UNKNOWN/FAIL with owner and external condition; withhold strict acceptance.
4. Map every P/S/C/D/W/H/E row to observed evidence, inventory platform exclusions,
   finish stage gate/review/sync, then stop before T13.

## Remaining acceptance gaps

- November 11 maintenance reconciles current project component selections with
  verified installed source content, refreshed native refs and fresh project
  discovery; the maintenance receipt records the completed observations and scope.
  Native model/approval behavior on the changed runtime set remains T12 evidence.

- T12 deeper engineering, unresolved cognitive qualification and changed-runtime
  native behavior evidence;
  T13 fresh whole-branch review, full milestone acceptance and deliberate stop.
- Cognitive qualification remains UNKNOWN; complexipy is not a passing authority.
  Historical duplicate/global
  scope findings remain bounded by the November 11 observations above. Preserve
  caches/defaults and distinguish source discovery from native behavior acceptance.
- Native approval evidence is programmatic actual-host protocol interaction;
  no GUI/human-action claim is made. No release is accepted or published.

Use the [execution record](evidence/2026-11-01-execution.md),
[T9 mutation evidence](evidence/2026-11-01-mutations.md),
[T10 evidence](evidence/2026-11-01-symbols.md),
[T11 evidence](evidence/2026-11-01-codex-acceptance.md) and
[request guide](configuration.md). The ignored task ledger and private native
transcripts are under .superpowers/sdd/2026-10-28-reference-parity. Fresh clones
use tracked evidence/fixtures and exact-commit CI. Use gh for GitHub reads and
authorized writes. Never publish private source, journals or raw host transcripts.
