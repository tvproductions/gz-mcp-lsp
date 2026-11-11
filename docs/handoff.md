# Implementation handoff — 2026-11-01

**T0-T11 implemented, with actual installed/native host evidence. Stop before T12.**
The final synchronization response must report the exact final commit's platform
CI before T11 is treated as accepted. The user requested T11 completion and
instructed that accepted branches/worktrees be merged to main and removed.

## Workspace and verified checkpoints

Continue on **main in the primary checkout** after the final acceptance sync.
T10 is `a71bcd445f47dac46a43812b9c996cb87b71bfd0`; T11 adds tests, distribution
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

Keep CPython **3.14.10**, MCP SDK **2.3.0** and ty **0.0.95**.
uv accepts **>=0.13.6**, with CI testing **0.13.6**; supported callers need not
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

- T12 deeper engineering and unresolved cognitive qualification/native discovery;
  T13 fresh whole-branch review, full milestone acceptance and deliberate stop.
- Cognitive qualification remains UNKNOWN; complexipy is not a passing authority.
  Native discovery retains duplicate/global-scope FAIL. Preserve caches/defaults.
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
