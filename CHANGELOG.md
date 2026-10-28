# Changelog

## 0.7.1 — October 26, 2026

The maintainer explicitly directed release without waiting for the gzkit-owned
engine, whose arrival has no promised date. Consumer preparation ships now;
actual engine integration/qualification remains open and unscheduled in issue #1.
The cognitive exception continues at ceiling 15, without a strict-acceptance claim.
See the [release receipt](docs/evidence/2026-10-26-0.7.1-release.md).

- Refresh Ruff 0.17.2 to 0.17.3 in both independent uv baselines after official
  release review; keep the selected rule families and four routine hooks intact.

- Prepare the consumer boundary for the cognitive engine the maintainer says is
  coming from gzkit: 42 independently specified fixtures, fail-closed source
  inventory/ceiling checks and installed-engine provenance. This is not a private
  scorer or a completed cognitive fix. Engine selection, qualification, corpus
  measurements and removal of the release exception await a separately reviewed
  upstream candidate, without holding this patch release.

- Book the deferred cognitive qualification correction as
  [issue #1](https://github.com/tvproductions/gz-skills-first-starter/issues/1),
  after verified 0.7.0 publication. No correction is implemented or released;
  ceiling 15 and the existing ownership/qualification requirements remain.

## 0.7.0 — October 26, 2026

Published at the maintainer's explicit direction with cognitive qualification
deferred to planned 0.7.1. The cognitive ceiling remains 15; neither complexipy
nor the proposed shared engine is certified. This exception permits this release,
not a strict-acceptance claim or automatic adopter waiver. See the
[candidate freshness and acceptance receipt](docs/evidence/2026-10-26-0.7.0-release.md).

- Refresh root ty to 0.0.92. Pin the already-required Interrogate, Vulture,
  Bandit, Coverage.py, deptry, pip-audit and Import Linter in both hygiene groups.
  Keep all deeper analysis outside the four routine hooks and routine CI.
  Add the real CLI-to-execution-wrapper import boundary and clarify production
  docstrings; retain and review analyzer findings instead of suppressing them.
- Refresh the standard interpreter to Python 3.14.10, verified against the
  October 25 security release. Both baselines use the pinned official Astral
  download metadata while retaining required uv 0.13.5 and separate Python families.

- Permit scheduled dependency scans and reviewed update PRs for independent
  standard Python and X-Plane/XPPython3 baselines. Adopters choose starter and/or
  upstream updates and their own timing. This is a maintenance-policy correction,
  not a release-wide pin refresh or automatic adoption of updates.
- Configure weekly Dependabot jobs for standard Python, the independently locked
  X-Plane/XPPython3 tool baseline and GitHub Actions. Add Python 3.12.16 standalone
  tool probes and CI coverage without changing the four routine hooks. Hosted bot
  operation, root build-only update PRs and embedded-host compatibility remain
  unverified; Python/uv execution pins and plugin catalogs need separate review.
  See [scope and evidence](docs/engineering/dependabot.md).
- Fix clean Linux provisioning of X-Plane's Python 3.12.16 by pinning Astral's
  newer interpreter download metadata in that project's uv configuration;
  retain uv 0.13.5 and exact runtime requirements. Exclude local project identities
  from bot package lookups. Initial hosted scans completed successfully; actual
  update-PR generation and simulator compatibility remain unverified.
- Establish this template as the shared policy alignment source for gz-skills
  and Backplane, with source consistency checks and prospective major-release
  PRDs for independently versioned components. Delegate lite/heavy definitions,
  requirements tracking, labeling, backlog/release monitoring and handoffs to
  Backplane; retain independent versions, consumer policies and readiness gaps.
- Define this repository's Git sync ritual in AGENTS.md, independent of installed
  skills: scoped review, checks, hooked commit, normal push, exact-commit CI and
  explicit separation of sync completion from release acceptance.
- Confirm the user-directed Python N-1 policy for ordinary GZ projects: stay
  one stable minor behind (currently 3.14), with the latest verified patch.
  Latest-tooling requirements and the host-controlled runtime exception remain
  distinct. Assess gzkit's scorer as a candidate for a tiny shared package.

The [latest-toolchain receipt](docs/evidence/2026-10-24-latest-toolchain.md) records
actual updates and checks. Strict cognitive acceptance remains blocked.

- Require latest stable baseline tooling across tool families for this starter
  and both adopter lanes. Older family ranges/pins are not freshness exemptions;
  stale or unknown required evidence blocks acceptance. Keep the explicit Python
  runtime-family policy and evidenced compatibility exceptions visible.
- Refresh execution to Python 3.14.9, uv/uv_build 0.13.5, Ruff 0.17.2, ty 0.0.91,
  complexipy 8.1.0 and Lizard 1.24.3, with setup-uv v10.3.2. Resolve transitive
  locks through uv; pre-commit/Cosmic Ray and the routine hook set are retained.
  Update SP to released v7.0.1 at its exact tag commit in both catalogs; retain
  current gz-skills and explicitly deferred Backplane.
- Enforce source-independent builds in the existing CI artifact check with
  `uv build --no-sources`, matching local acceptance guidance.
- Add a cognitive qualification canary: complexipy 8.1.0 scores nine keyword
  conditional expressions zero. The compatibility probe must fail rather than
  certify that analyzer. Independent cognitive qualification/replacement remains
  open; this candidate is not eligible for an unqualified strict release.

- Record a read-only [tooling freshness review](docs/evidence/2026-10-24-tooling-freshness.md):
  the released Python/uv/build/ty/complexipy/Lizard selections have newer
  same-family releases. Report newer Ruff/CI-action families and SP independently;
  no upgrades or compatibility claims are made by this review.

- Clarify uv initialization by existing metadata: use init for new ordinary
  projects without pyproject, preserve/reconcile existing or template-generated
  metadata, and explicitly migrate brownfield code/dependencies. Replace weak
  greenfield “prefer” wording with the canonical packaged initialization path.

- Make this repository's tooling-maintenance routine explicit in AGENTS.md:
  read-only freshness review before starter release preparation, inventory of
  execution/CI/plugin pins, dated evidence and explicit retain/update decisions.
  Keep upgrades scoped and verified; no pins, environments, hooks or schedules
  change as part of this instruction update.

## 0.6.0 — October 24, 2026

- Add the single template-owned `update-gz-template` skill as the canonical
  entry for adopter update review and migration. This scoped ownership exception
  replaces zero authored skills; generic dependency maintenance stays in gz-skills.
- Configure previews/seeds the project `.agents/skills/update-gz-template/SKILL.md`,
  compares its content, preserves local edits, rejects symlink/duplicate destinations
  and rolls back prior writes on skill creation failure. Package the source skill
  with checked wheel resources and verify installed behavior outside the checkout.
- Add canonical update/first-bootstrap guidance for pre-skill adopters. Existing
  adopters must reconcile the new managed skill alongside fragment/lock/host files;
  adding a skill alone does not upgrade provenance or establish conformance.

This is an adoption-capability minor, not a compatible-fix patch. No runtime/tool/
plugin pin or file schema changes. Published v0.5.0 remains immutable.

Verification: 39 adoption tests, the four routine checks, skill validation,
bundle/both catalogs, source-independent build and isolated installed seeding,
complexity checks, and a twelve-command disposable 0.5-to-0.6 upgrade proof.
See the [release receipt](docs/evidence/2026-10-24-0.6.0-release.md). Fresh-session
host discovery and broader conformance automation remain separately unverified.
The GitHub release records exact-commit CI and supplies a portable skill ZIP
for existing adopters alongside the source/wheel assets.

## 0.5.0 — October 24, 2026

- Clarify Python-only scope for both adoption lanes; other languages, likely
  including Go, remain future work. Make adopter MAJOR.MINOR.PATCH rules explicit,
  including public contract/deprecations, 0.x classification and independent
  product versions. Pass the clarification through packaged adopter instructions.
  Record the maintainer's personal consistency purpose and future guidance by
  language, environment and CLI/TUI/web/desktop application type.

- Implement maximum applicable Astral acceptance guidance following a Projects-
  focused uv documentation review. Bind requirement/evidence records, effective
  uv/Ruff/ty configuration, exact selected environments, executable provenance,
  source-independent builds and clean installed behavior to adoption guidance.
  Reconcile workspace root/member semantics, namespace/coordinator applicability
  and the approved Ruff selection. Pass the contract through adopter instructions
  and regenerate the wheel resource. This minor release delivers the expanded
  adoption obligations; existing adopters require reviewed reconciliation.
- Execute invented flat-application, typed-library and workspace migrations on
  Windows with pinned Python 3.14.8/uv 0.13.1. Retain 64 command records, typing
  positive/negative controls, separate member installations and eight matching
  artifact inventories from four source-independent builds. Record the starter's
  effective configuration and bounded acceptance, preserving wider unknowns.
  Helper behavior, dependency pins, the four hooks and CI contract are unchanged.

- Clarify the user-directed release-planning policy for this starter and
  adopting projects, passing it through baseline policy and adopter instructions:
  every major release, including 1.0.0, always requires a newly written PRD;
  minor releases bundle
  related changes, with SP-BP intended to assist once ready and explicitly
  adopted; patches remain compatible fixes and clarifications. Preserve the
  existing 0.x compatibility rules and published release identities.
- Preserve the original Astral assessment, follow-up evaluation and uv review as
  historical evidence, with current implementation and continuation links. Add
  no generic conformance checker, maintenance skill, lifecycle or routine gate.

- Require explicit lite/heavy selection before completed adoption, with the same
  applicable Python foundation in both lanes. Preserve heavy's intended Backplane
  composition and report its current deferred readiness separately.
- Require applicable deeper analysis at adoption and release acceptance, plus
  on demand. Keep the four routine hooks and routine CI unchanged. Missing,
  failing or stale required evidence blocks strict acceptance; exceptions remain
  conditional, never 100% conformance.
- Add a single greenfield/brownfield runbook covering first adoption, old-starter
  upgrades, disposable target candidates, three-way managed-file reconciliation,
  preserved local edits/provenance, rollback and explicit completion records.
- Resolve temporary test-fixture roots before comparing with the helper's
  canonicalized paths. This fixes six macOS subtest failures without changing
  helper behavior, file schemas, runtime/tool pins or plugin pins.

Adopter impact: this is a policy/adoption minor. Reconcile instructions and
provenance together using [the 0.5 runbook](docs/adoption-0.5.md); do not merely
change the version string or expect configure to overwrite old records. Existing
products keep their own versions and public behavior. New adopters must select a
lane and establish the Python baseline; generated host files alone are insufficient.
Both lanes follow SemVer and require a new PRD for every major including 1.0.0.

Verification and limits: the [release receipt](docs/evidence/2026-10-24-0.5.0-release.md)
records locked sync, four routine
hooks/35 adoption tests on macOS without a TMPDIR workaround, twelve analyzer
contract tests, bundle/both catalogs, normal and source-independent builds,
isolated installed CLI checks, complexity checks, bounded macOS Cosmic Ray
compatibility and disposable first-adoption/upgrade scenarios.
The GitHub release identifies the exact commit and remote CI result. Required
broader analyzer compatibility/freshness, real-adopter migration and fresh-session
host acceptance remain separately scoped; no unqualified baseline conformance
is certified. Automatic lane/evidence/PRD validation and three-way upgrade merging
remain design work. Backplane is still disabled; there is no dependency refresh,
package-registry upload or downstream-project mutation in this release.

## 0.4.1 — October 18, 2026

- Verify disposable v0.4.0 Codex CLI discovery on Windows/0.163.0. Preserve
  the initial UNKNOWN/trust-rejection receipt; after explicit user approval of
  only that project's native trust entry, fresh model sessions load the intended
  SP/gz-skills pair, all 35 discovered skill files match pinned Git blobs and an
  outside-project control preserves defaults. Native installed/cache state can
  include disabled Backplane; it remains disabled and absent from discovery.
  Desktop UI, other harnesses and Backplane readiness remain separate proofs.
  Correct the stale acceptance instruction expecting a
  starter-authored `skills-first-start` skill; verify only upstream identities
  and their exact owning sources.
- Verify the next selected on-demand tool: pin Cosmic Ray 8.7.0 from its 8.x
  family in `hygiene`, with uv-generated transitive resolutions. No baseline
  selection or routine gate changes; this completes a bounded compatibility
  proof for an already-selected tool.
- Add an explicit disposable-source/unittest probe for Windows/Python 3.14.8:
  two killed and two intentionally surviving mutants, source restoration and
  passing post-run tests. Failed-baseline, timeout and launch-error controls
  expose the baseline CLI's zero exit for an incompetent launch. Inspect stored
  worker/test outcomes rather than trusting exit zero or the report's kill count.
  No score gate, application mutations or new hooks/CI steps are introduced.
- Preserve the published v0.4.0 tag and historical receipts. An authorized
  adopter pilot is the next adoption milestone; other analyzer/platform proofs and
  analysis-utility ownership remain open. See [compatibility evidence](docs/evidence/2026-10-18-cosmic-ray.md).

Adopter impact: compatible verification and guidance corrections for existing
baseline commitments; no new required tool selection, routine gate, managed-file
schema or helper behavior. Cosmic Ray is now pinned in the on-demand hygiene
group after its Windows/Python 3.14.8 proof. Its baseline CLI can return zero on
a launch error, so inspect structured outcomes. No adopter migration or plugin
update is performed by this release.

Verification: 35 routine adoption tests, twelve explicit analyzer tests, the four
approved hooks, bundle/both catalogs, locked sync/lock check, source/wheel build
and isolated installed CLI checks. The implementation commit passed Ubuntu CI;
release metadata is verified before tagging. Codex CLI discovery evidence uses
published v0.4.0 and unchanged component pins; it does not establish fresh-session
acceptance of every later starter revision. Desktop UI, other harnesses,
Backplane readiness and remaining deeper-tool proofs stay open.

## 0.4.0 — October 18, 2026

- Complete the next code backlog item: refactor adoption validation, configuration
  rendering, write planning and rollback into bounded functions. Preserve public
  behavior and error messages; add public-helper checks for failed replacement,
  later-write rollback, concurrent-file preservation and disabled alternate
  plugin sources. Simplify the analyzer's scope validation without changing its
  fail-closed contract. All source/tests/utilities pass the existing on-demand
  cyclomatic/cognitive checks. See [before/after evidence](docs/evidence/2026-10-18-complexity-remediation.md).
  No pins, thresholds, hooks or CI gates change for this refactor.
  Latest verification is 35 routine adoption tests and
  twelve explicitly run analyzer tests, plus the routine and artifact checks.

- Policy change: require maximal documented Astral alignment for Python project
  layout, packaging, configuration, environments and verification. Full adopters
  must refactor nonconforming structure/configuration; preservation during helper
  configuration does not waive the baseline. Compatibility exceptions require
  evidence, an owner and revisit condition. Preserve behavior, data and existing
  authorities during migration. Pass the requirement through adopter instructions.
- Migrate the starter implementation to `src/skills_first_starter`, uv_build and
  an installed console command. Retain `starter.py` as a compatibility launcher.
  Include checked generated bundle/catalog/instruction resources in wheels and
  exercise installed behavior outside the checkout with explicit SHA provenance.
- Establish project-locked Ruff/ty/pre-commit and the four approved routine hooks,
  shared with CI. Add reviewed UP/B/SIM/RUF lint families; fix their findings and
  type-check all Python source/tests/utilities. Deeper analyzers remain on demand.
- Document Cargo-style workspace membership, shared locks and environments,
  explicit editable dependency edges and member command selection. Keep this
  single-package starter a standard uv project. Align CI with Astral's reviewed
  immutable checkout/setup-uv action examples and explicit tool/runtime pins.
- Fix the compatibility probe's Windows legacy-locale source decoding, cover it
  with an explicit regression, add LF normalization and explicit subprocess
  decoding. Preserve historical receipts and visible existing complexity debt.
- Pin refresh within Ruff's selected 0.15 family: 0.15.18 to 0.15.22. Select uv
  and uv_build 0.13.1, pre-commit 4.7.0 and required ty 0.0.89. ty is beta with no
  stable release; record this compatibility exception and revisit on stable
  release or the next scoped maintenance. Python remains 3.14.8. Other analyzer
  and plugin pins, profile choices and Backplane deferral remain unchanged.

Adopter impact: this minor release changes the baseline adoption
contract and supersedes the unpublished 0.3.1/0.3.2 candidates. Reconcile generated
instructions and provenance explicitly; migrate packaging/imports, tool config,
hooks and CI with rollback evidence. Configuration-only helper use still
preserves project files and reports remaining adoption work. No package-registry
publication is included. See the
[alignment contract](docs/engineering/astral-alignment.md) and
[migration receipt](docs/evidence/2026-10-18-astral-alignment.md).

Verification on managed Python 3.14.8 / Windows: 31 adoption tests, eleven
explicit analyzer tests, four approved pre-commit hooks, Ruff/ty, bundle and both
catalogs, lock consistency, source/wheel builds and isolated installed CLI checks.
New packaging utilities meet existing complexity ceilings; the refreshed
Ruff/complexipy/Lizard probe passes without waiving CLI legacy debt. Static
portability checks pass; on-demand uv audit reports zero known vulnerabilities
in 17 third-party packages. Remote CI and native loading remain unobserved.

Release verification supersedes those earlier candidate limits: the final
implementation commit passed the Ubuntu routine/artifact CI gate. The release
metadata commit is verified with the same locked local gate before tagging.
Native skill loading, macOS execution, Cosmic Ray compatibility and other
deeper-tool proofs remain unverified; SP-BP stays deferred and disabled.

## 0.3.2 — Unreleased

- Fix generated provenance and Codex marketplace sources to use the canonical
  renamed `tvproductions/gz-skills-first-starter` repository. An end-to-end
  configure regression first reproduced the old alias in the generated files.
  Existing adopters keep their files until explicitly reviewed reconciliation;
  no force overwrite or automatic migration is introduced.

- October 18 follow-up pin refresh: advance gz-skills from v0.7.0 to the latest
  published v0.8.0 at `75bcd11ee9371ecff1a7b3432d2af29d4bdbb788` in the bundle
  and both native catalogs. Refresh current guidance; preserve the historical
  0.7.0 installation evidence. This adds upstream explicit-only release support,
  without granting publication authority or enabling Backplane. The existing
  0.3.2 development version remains unreleased; no published version is changed.
  See [the scoped update receipt](docs/evidence/2026-10-18-gz-skills-0.8.0.md).

- Pin refresh: update Superpowers from v6.4.1 to the latest stable v7.0.0,
  published October 10, 2026, at full SHA
  `bb92a77741419a4ab5f06e711a283343f1ada0c3`. Align the bundle and both native
  catalogs. Retain gz-skills, Backplane and Python/tool pins.
- Correct current SP guidance: Backplane's historical compatibility baseline
  does not constrain active SP while Backplane remains deferred and disabled.
  Prepare patch 0.3.2 as explicitly requested; no adopter baseline policy changes.

Adopter impact: review SP 7's workflow changes and reconcile the recorded bundle,
catalog source and native installation through the host manager when authorized.
Preserve prior pins for rollback, project instructions and profile choices.
Backplane enablement still requires separate readiness and compatibility review.
No installed plugin cache or other project is changed by this update.

See [the scoped update assessment](docs/evidence/2026-10-11-superpowers-7.0.0.md)
for release/manifest evidence, compatibility limits and Python opportunity decisions.
Fresh-session native loading and SP 7/Backplane compatibility remain unverified.

Verification: 28 unittest tests, bundle/both-catalog validation, Ruff 0.15.18
check/format and offline uv lock consistency passed on actual managed Python
3.14.8. The lock refresh changed only template version metadata; no Python code
or development-tool resolution changed.

## 0.3.1 — Unreleased

- Policy change: require cohesion in the adopter minimum on-demand Python tool
  standard. Clarify that downstream tool requirements are independent of the
  starter helper's own needs; adopters own tool pins, runtime verification and
  interpretation of class scores. Pass the requirement through the generated
  instructions fragment and linked baseline/engineering guidance.
- Prepare patch version 0.3.1 as explicitly requested by the user for this
  requirement clarification. Runtime, analyzer and upstream component pins are
  retained; no cohesion dependency is added to the starter environment.

Adopter impact: reconcile project instructions and the selected development tools
against the reviewed policy. Verify cohesion on the selected runtime with invented
class fixtures, preserve project thresholds and record inapplicable scopes or
compatibility gaps. Keep the tool outside hooks and CI gates. Selection does not
establish installation or Python 3.14 compatibility; this starter has no cohesion
compatibility receipt. Existing adopters are not automatically migrated.

Verification: 28 unittest tests, bundle/both-catalog validation and Ruff 0.15.18
check/format passed on Python 3.14.8. The offline uv lock refresh changed only
the starter's version metadata. This policy/documentation change requires no
Python 3.14 API changes; no cohesion execution or compatibility claim is made.

## 0.3.0 — 2026-10-11

- Establish the zero-skill ownership contract: this template authors and
  distributes no agent skills. SP + SP-BP + gz-skills remains the intended stack,
  with SP and gz-skills active and SP-BP deferred/disabled pending readiness and
  explicit adoption. Project operational skills remain project-owned.
- Move adoption instructions into `docs/adoption-workflow.md`, Python policy and
  references into `docs/engineering/`, and on-demand analysis utilities and their
  CLI tests into `tools/engineering/`. Preserve the existing Python/tool policy
  and analyzer semantics. Remove all starter `SKILL.md` packages.
- Configure now writes host configuration, provenance and project instructions
  without installing a front-door skill or creating skill discovery directories.
  Instructions route directly to upstream/project workflows and require review
  of template releases, dependency updates and baseline-policy changes.
- Add the structure/ownership contract, supporting design precedents and an
  explicit migration guide. Correct stale copied guidance about gz-skills v0.6.0
  maintenance and setup capabilities without invoking setup or selecting a profile.
- Clarify that adopters stay current within Python 3.14.x, or host-compatible
  3.12.x for XPPython3-bound projects. Exact execution pins are refreshed verified
  selections rather than permanent adopter patch requirements. XPPython3's
  embedded runtime remains host-controlled and requires separate validation.
- Add `docs/baseline-policy.md` as the adopter version-range/selection authority,
  separate from checkout-specific execution pins. Release guidance distinguishes
  policy changes from pin refreshes; unsettled tool families remain explicit gaps.
- Require relevant code to observe the selected Python family's idioms, stdlib
  advances and deprecations through bounded evidence-backed review. Delegate
  reusable workflows to SP/gz-skills while keeping runtime policy starter-owned;
  the pinned Pythonic-pattern skills do not prove complete version-audit coverage.
- Inspect seven relevant gz-skills instruction bodies and verify their Git blob
  hashes against the pinned release; document Python pattern, portability,
  environment/maintenance and debt/change-review coverage and its limits.
- Reinforce upstream runtime/engineering-policy obedience while leaving runtime
  discovery in gz-skills. Record the separately authorized neighboring-source
  reinforcement as released v0.7.0 at `6ebf803e4a2775d3742c84984a03548275b7c926`,
  selected consistently by the bundle and both native catalogs. Tagged installs
  passed in disposable Codex/Claude configuration and the uvx snapshot installer.
- Correct the relocated analyzer test fixture to write Python source as UTF-8;
  Windows' legacy locale encoding otherwise invalidates its Unicode cases.

Adopter impact: reconcile older managed records and project instructions; retire
legacy starter skills only after reviewing and preserving project edits. Configure
blocks legacy starter skill names in all four inspected discovery surfaces before
any writes and preserves their contents. It never performs an automatic migration.
Keep prior pins/configuration for rollback and preserve application skills,
dependencies, overrides, profiles and native manager state.

Verification: 28 routine unittest tests, bundle/both-catalog validation and pinned
Ruff lint/format checks on Python 3.14.8, plus the relocated analyzer's ten public
CLI tests. Template metadata/lock changes select 0.3.0; SP/SP-BP and runtime/tool
pins are retained. The independent gz-skills update is recorded above.
The relocation requires no new Python 3.14 APIs; concurrency, annotation,
compression and template-string opportunities are deferred as unnecessary here.
Historical evidence retains its original paths/hashes and failures. Fresh-session
host loading, ty/pre-commit enforcement and the other documented gaps remain
unverified or pending. The GitHub release identifies the full verified template
commit and CI outcome; native loading evidence remains separate.

## 0.2.0 — 2026-10-11

- Adopt gz-skills v0.6.0 at exact commit
  `e722e808647481c4c9d2feab61f1843aa8e0b19a` in the bundle and both native catalogs.
  Its nineteen-skill catalog adds project setup and Pythonic pattern review/apply;
  maintenance now supports freshness-only review and starter/plugin inventory.
- Update guidance that previously described these released capabilities as
  proposals. Preserve approved starter Python 3.14 and retired-tool policy over
  upstream profile defaults. SP and deferred/disabled SP-BP pins are unchanged.

Adopter impact: existing managed locks and front-door skills require reviewed
reconciliation; configure refuses to overwrite older records. Keep prior pins
for rollback, preserve app files and explicit profiles, and use the native host
manager only when its update is authorized. This release does not invoke project
setup, select lite/heavy, install plugins or migrate other projects.

Compatibility review: gz-skills' Python CLI now requires >=3.13, compatible with
the starter's pinned 3.14.8. Native plugin consumption does not require that CLI.
The pin change needs no new Python APIs; concurrency, annotation introspection,
compression and template-string machinery are deferred as unnecessary here.
See [the update assessment](docs/evidence/2026-10-11-gz-skills-0.6.0.md).

Verification: 25 unittest tests, bundle/both-catalog validation and Ruff 0.15.18
check/format passed on Python 3.14.8. uv lock refresh changed only the starter
version; a subsequent lock check passed. Release notes identify the full release
commit and its GitHub CI result. Starter-specific fresh-session loading remains unverified;
upstream installation evidence does not prove this combined bundle loads.
ty/pre-commit and the other documented tooling gaps remain outstanding.

## 0.1.0 — 2026-10-11

Initial versioned template baseline; earlier untagged development commits did not
establish a published release.

- Immutable native catalogs for independent SP and gz-skills sources; SP-BP
  remains pinned, pre-release, deferred and disabled.
- Preview/apply/status adoption with conflict preservation, idempotence and a
  starter-owned front door; read-only structural backport assessment.
- Python 3.14 family policy with exact patch 3.14.8, baseline configuration
  guidance permitting project additions/extensions/overrides, and maintenance
  routing to gz-skills.
- Explicit UTF-8 reads and preservation of existing host TOML line endings.
- Starter version and exact revision in new adopter records, plus a read-only
  `version` command and version-bearing configure/status/validate output.

Adopter impact: reconcile older managed files from a reviewed starter checkout.
Unversioned starter records retain their existing SHA and require review; the
helper does not overwrite them or invent version provenance. App dependencies,
settings and explicit profiles remain project-owned.

Verification: 25 unittest tests, bundle validation (including both native
catalogs), Ruff 0.15.18 check and format check passed on Python 3.14.8.
The GitHub release notes identify the exact verified release commit.
gz-skills v0.5.0 remains its latest published release as checked October 11;
newer upstream main changes are not included in this baseline.
Native host discovery and
end-to-end installation remain unverified; ty/pre-commit enforcement and other
documented Python tooling gaps remain outstanding. This version does not certify
combined-stack compatibility or SP-BP readiness.
