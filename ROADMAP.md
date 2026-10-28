# Roadmap

## Unscheduled: upstream cognitive engine integration

Tracked as [issue #1](https://github.com/tvproductions/gz-skills-first-starter/issues/1).
The initial 0.7.1 target is superseded: the maintainer directed releasing the
consumer preparation without waiting for an engine with an unknown delivery date.
After verified 0.7.1 publication, issue #1's milestone was cleared and milestone
0.7.1 closed for the delivered consumer preparation/Ruff patch. No later release
target is assigned to engine integration.

The maintainer explicitly authorized releasing 0.7.0 without waiting for the
cognitive fix, then booking the correction for 0.7.1. Qualify the selected
CPython AST approach at ceiling 15, including keyword conditionals and functions
under module-level loops/match. Preserve historical failing evidence, public
contracts, thresholds and upstream ownership. Leave gzkit untouched; no extraction
project, private scoring fork or plugin installation follows from this booking.
The existing [extraction assessment](docs/evidence/2026-10-24-gzkit-cognitive-extraction.md)
owns the demonstrated gaps. Release 0.7.1 does not deliver the engine or fix its
scoring defects; those remain this unscheduled follow-up.

Consumer-side preparation now supplies 42 qualification cases, independent
inventory and ceiling checks, and fault-rejection regressions. The maintainer
confirmed that gzkit will supply the engine without a promised date; no private engine or new
extraction project is being created. See the
[integration boundary](docs/engineering/cognitive-integration.md). Actual engine
selection, qualification and corpus proof remain pending; issue #1 stays open.

## 0.6: one canonical template-update skill

The user requested a template-native update entry. The starter owns only
`update-gz-template`, seeds it through configure, packages/verifies its bytes and
preserves local edits. [Canonical updating](docs/updating.md) includes bootstrap
for 0.5 and older adopters. Generic maintenance remains upstream. Fresh-session
discovery remains a separate operator-run proof.

## 0.5 policy delivery and remaining enforcement

Version 0.5.0 bundles expanded Astral acceptance, mandatory lite/heavy selection,
required adoption/release analysis, explicit adopter SemVer/major PRDs, and the
[greenfield/brownfield runbook](docs/adoption-0.5.md). These are binding review
obligations; the helper remains configuration-only. Keep both lanes equally strict
on the Python foundation and preserve heavy's intended Backplane composition.

The [design record](docs/engineering/strict-adoption-design.md) separates those
delivered policies from remaining automatic lane/evidence/PRD validation and
reviewed upgrade tooling. Real-adopter pilots, remaining analyzer verification
and native-host proofs remain open. Future language/environment and CLI/TUI/web/
desktop matrices require their own designs; current scope is Python-only.

## Implemented initial scaffold

- Immutable SP + SP-BP + gz-skills bundle with independent sources.
- Codex and Claude native marketplace catalogs.
- Preview/apply/status Codex project configuration for empty and existing projects.
- Preservation/conflict/symlink/duplicate/gzkit checks and unittest coverage.
- Originally zero starter-authored skills; 0.6 adds only the
  canonical template-update entry. Documented adoption workflow and direct workflow
  routing in adopter instructions. Analysis utilities live in ordinary tooling.
- Default SP + gz-skills activation with SP-BP pinned but disabled.
- Read-only structural assessment and guidance for incremental backporting.
- Documented native loading/verification boundaries.
- Independent template version metadata and CLI reporting, version/SHA adopter
  provenance, changelog and release policy. Initial v0.1.0 is published.

## Next adoption proofs

1. An authorized adopting repository pilot (FDAU is the primary candidate).
   Map existing configuration and adapters; do not replace project authorities.
2. Codex desktop UI acceptance, separate from the completed CLI proof below.
3. Claude project-scope installation, lifecycle, and combined-stack conformance
   after upstream Backplane Claude acceptance.
4. OpenCode support after upstream Backplane V1/V2 adapter and verification.

Completed October 18: [fresh-session Codex CLI acceptance](docs/evidence/2026-10-18-codex-discovery-verified.md)
on Windows/0.163.0 using published v0.4.0. After explicit user approval of only
the disposable project's native trust entry, fresh model sessions load SP and
gz-skills from the intended source; all 35 discovered skill files match pinned
Git blobs. An outside-project control preserves existing defaults and loads
zero starter-source skills. The initial UNKNOWN/trust-rejection receipt remains
historical evidence. Backplane remains disabled; combined-stack readiness and
other harnesses are not established by this CLI result.

## Later extensions

- Observe hosted Dependabot scans and real update PRs for both independent
  standard and X-Plane/XPPython3 projects and GitHub Actions. Local configuration,
  separate X-Plane tool declarations/lock and bounded standalone verification
  now exist; actual hosted operation and embedded-host verification remain UNKNOWN.
  See [coverage and limits](docs/engineering/dependabot.md). Adopter update
  sources and timing remain adopter-owned.
- Reviewed update/rollback automation that preserves existing native installs.
- Generic maintenance remains owned by gz-skills; no local maintenance skill or
  generic freshness reporter is planned. The pinned gz-skills v0.8.0 supplies
  freshness-only assessment and template/plugin source inventory through its
  existing maintenance skill. The starter retains policy, catalog consistency and
  preservation bindings; current tests prove preservation, not dependency
  resolution or settings loading. See the
  [configuration contract](docs/project-configuration.md).
- New-project product templates selected by the adopter, not a mandatory framework.
- Optional app-owned plugin registration alongside the three engineering plugins.
- Synchronize bundle compatibility evidence as SP-BP completes its release and
  broader proposed capabilities mature.

No milestone above implies a release, current installed stack, or a completed
upstream capability. Requirements/traceability expansion belongs to Backplane,
not a duplicate lifecycle in this starter.

## Python engineering policy follow-up

Implemented after the [uv documentation deep dive](docs/engineering/uv-deep-dive.md):
the [Astral acceptance contract](docs/engineering/astral-acceptance.md),
[executed application/library/workspace migrations](docs/engineering/astral-migrations.md)
and [starter acceptance record](docs/evidence/2026-10-18-astral-acceptance.md).
Effective configuration, exact environment/provenance, root/member selection,
source-independent builds and installed dependency/typing/resource proof are
explicit. Maximum applicable Astral alignment remains the user-directed standard.
The preserved assessment and proposal remain historical; broader adopter, CI,
freshness and deeper-tool gaps stay separately visible in the acceptance record.

Reusable Python-version idiom/stdlib review belongs upstream in gz-skills.
The starter's [baseline policy](docs/baseline-policy.md) requires assessing code
currency, but the pinned Pythonic-pattern skills are not a complete version audit.
Record that coverage gap and review a future released workflow before routing
to it. gz-skills v0.7.0 reinforces runtime discovery and scoped version-aware practices
in its existing Python workflows; a comprehensive version audit remains a gap.

The required Python 3.14 engineering policy documents the
routine standards and on-demand hygiene selections, including Cosmic Ray,
deptry, pip-audit, Import Linter and adopter class cohesion analysis through
cohesion. This minimum adopter standard is independent of the helper's needs;
cohesion version selection and runtime verification remain adopter-owned.
The approved routine pre-commit selection
remains Ruff check/format, ty and unittest.
Implemented for 0.4.0: `src/` packaging with uv_build, project-locked ty and
pre-commit, reviewed strict Ruff rules and locked local/hook/CI commands. The
[Astral contract](docs/engineering/astral-alignment.md) requires adopter
refactoring with evidenced exceptions. Still pending: shared/local utility
ownership; pinned Python 3.14 verification of the remaining
selected deeper analyzers. Deeper analyzers remain outside hooks
and CI gates. SP-BP remains an expected addition, deferred pending readiness.

Completed after the v0.4.0 release: Cosmic Ray 8.7.0 is pinned in `hygiene`
under a selected 8.x family and has a Windows/Python 3.14.8 standalone unittest
proof. Four mutants complete: two killed, two intentionally surviving. Failed
baseline, timeout and launch-error controls distinguish broken runs; the
baseline CLI's zero exit on launch failure requires structured-result inspection.
See [the assessment](docs/evidence/2026-10-18-cosmic-ray.md). No mutation score
gate, app-code mutation, hook or CI step is added. Codex CLI discovery using
published v0.4.0 is now verified; the next adoption milestone is an authorized pilot.

Complexity remediation completed for the 0.4.0 candidate on October 18:
`configure` and `project_config` now separate validation, planning and write/
rollback responsibilities. The checker's scope resolver also meets the cognitive
ceiling. Ruff C901 (20), complexipy cognitive complexity (15), and the settled
Lizard function/module/overall contract all pass across `src`, `tests` and `tools`.
Maximum Lizard score is 16 and maximum cognitive score is 14. Preserve historical
failing receipts; see the [before/after assessment](docs/evidence/2026-10-18-complexity-remediation.md).
No thresholds, analyzer pins or measurement semantics changed. These checks
are required at adoption/release acceptance and available on demand, outside
routine hooks/CI; C901 remains absent from routine selection.

## Settled C/C/C implementation — October 9, 2026

This supersedes earlier pending-contract statements. The explicit on-demand
Lizard checker implements `lizard-functions-v1`: function/module/overall
ceilings 20/20/20, nested functions counted independently, no synthetic class
scores, native assertion semantics, undefined empty means, and fail-closed
syntax/discovery errors. Use native Lizard measurements without syntax adapters; unsupported inline
suites fail discovery instead of disappearing from the measurement. Read `docs/engineering/ccc-contract.md` and run its CLI explicitly. Ruff and complexipy remain independent
checks; routine pre-commit and CI selection are unchanged. SP-BP remains expected,
deferred and disabled. No cob_reports tool configuration or app code changed.
The source-only cob_reports receipt reports 649 functions, maximum 100, overall
mean 7.14946, 42 function and 12 module failures, zero tool errors; this is
verified enforcement with visible legacy debt, not a clean corpus.
