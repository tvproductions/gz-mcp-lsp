# Project handoff — 2026-11-11

## Resume here: native source reconciliation before T12

The latest user request is to preserve this handoff and Git-sync the project
skill deduplication fix. Work is on **main in the primary checkout**. The base
for this save point is `5e74aeacd5f318062eb9b0b4c0877da5c6861bf0`; the final
sync response identifies the new commit and exact-commit CI. No T12 execution,
plugin update, full starter upgrade, tag or release is part of this save point.

Completed maintenance:

- Backported minimum-only uv compatibility at `5e74aea`: accept >=0.13.6,
  retain CI 0.13.6. Local full gate/normal hooks passed with uv 0.13.7, and
  [exact-commit CI](https://github.com/tvproductions/gz-mcp-lsp/actions/runs/43022296870)
  passed all three platforms. [Receipt](evidence/2026-11-11-uv-compatibility.md).
- Added a project-only enabled=false override for gz-skills@gz-skills while
  keeping gz-skills@skills-first-starter enabled. Fresh actual Codex discovery
  drops from 40 entries/20 duplicated names to 20 entries/zero duplicates.
  Outside-project discovery remains 20 standalone entries; user configuration
  is byte-unchanged. [Receipt](evidence/2026-11-11-skill-discovery.md).
- Source-independent build and outside-source distribution verification passed
  after the exclusion. This sync reruns the routine gate and normal hooks;
  final Git/CI results belong in the final response, without receipt-only commits.

**First next-session action:** start a fresh session and perform a read-only
native plugin/source inventory. Compare the installed starter-marketplace
gz-skills 0.10.1 with the repository's recorded 0.8.3 selection in
`.skills-first/bundle.lock.json` and both native catalogs. Use OpenAI Docs,
the project update-gz-template skill and gzs-update-dependencies as appropriate.
Expected result: one active source, with actual installed identity versus intended
pin explicitly established. The source mismatch remains open; deduplication is
not evidence of pin agreement. Do not silently rewrite provenance to match the
cache or change native installations/defaults without scoped update authority.
Preserve global activation elsewhere and leave cache management to the manager.

The current conversation may retain its already injected duplicate catalog;
fresh app-server skills/list with forceReload verified the corrected project
configuration. Raw local probes are not tracked and are unnecessary to resume;
the sanitized receipt above preserves counts, source versions and limitations.
Starter provenance remains v0.7.1 with the explicit uv-policy backport.
Fresh hosted Dependabot scanning against corrected inputs remains unverified.

T12/T13 remain unfinished. Once source reconciliation is understood, use the
existing T12 brief below within its approved stage boundary, preserve required
UNKNOWN/FAIL results and stop before T13. This handoff does not itself authorize
a plugin upgrade or waive cognitive/native acceptance gaps.

## Retained implementation checkpoint — 2026-11-01

**T0-T11 implemented, with actual installed/native host evidence. Stop before T12.**
T11 commit `05aa14b9885e511f04340e422298d784e8a74174` passed
[three-platform CI](https://github.com/tvproductions/gz-mcp-lsp/actions/runs/41358262222).
The user requested T11 completion and
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

- November 11: [project skill deduplication](evidence/2026-11-11-skill-discovery.md)
  now yields 20 gz-skills entries with zero duplicates, preserving global defaults.
  Installed starter gz-skills 0.10.1 still differs from recorded 0.8.3; E4 source
  reconciliation remains open. Historical duplicate observations below predate
  the project exclusion.

- T12 deeper engineering and unresolved cognitive qualification/native discovery;
  T13 fresh whole-branch review, full milestone acceptance and deliberate stop.
- Cognitive qualification remains UNKNOWN; complexipy is not a passing authority.
  Native source/version reconciliation remains open; historical duplicate/global
  scope findings are bounded by the November 11 observations above. Preserve
  caches/defaults.
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
