# Starter continuation — October 9, 2026

## Authority and final stack

Read root AGENTS.md, README.md, docs/architecture.md and docs/adoption.md.
This handoff describes the final changes prepared for publication; verify live
HEAD, worktree, remote and CI before continuing. Historical measurements and
verification notes are in docs/verification.md and docs/evidence/.

The active default is Superpowers + gz-skills. SP-BP is an expected third
component, pinned but deferred and explicitly disabled until readiness and
explicit adoption are established. Existing backlog/handoff authority remains.
The baseline pins are SP v6.4.1 and gz-skills v0.5.0; this change does not update
upstream pins, choose a lite/heavy profile, or certify combined native loading.
FDAU is the primary precedent. gzkit is a separate heavier ecosystem and its
lifecycle is not imported. App operational skills and deterministic domain code
remain project-owned.

Strong Python/tool preferences belong to starter and its project binding.
SP and gz-skills remain agnostic; SP-BP should be agnostic too. No upstream
plugin implementation changed. Review released upstream updates independently;
the bundled baseline is not a latest-version claim.

## Implemented starter behavior

- Immutable bundle and native marketplace catalogs; SP-BP disabled by default.
- Preview/apply/status helper preserving existing instructions, configurations,
  profiles and installed sources; conflicts stop writes.
- Read-only bounded structural backport assessment and incremental mapping guide.
- Bootstrap front door that prefers gzs-router for engineering catalog selection
  and SP using-superpowers for feature work.
- Python engineering skill with runtime/idiom, stdlib/adapter, persistence,
  version-aware design and on-demand hygiene guidance.

The helper still copies only the front-door skill. Read the Python engineering
skill from a reviewed starter checkout until its native discovery/adoption is
established. Configuration generation is not plugin installation or discovery
proof. Native project installation, fresh-session conformance, Claude end-to-end
adoption and OpenCode remain unverified/deferred.

## Final Python and hygiene choices

Starter targets Python >=3.14,<3.15, Ruff py314, and a uv runtime pin. Verification
used uv-managed Python 3.14.8. CI now uses uv and Python 3.14 only; earlier
3.11/3.13/3.14 results do not prove this new workflow. Check its live run.

The required routine standard is Ruff check/format, ty and unittest through
pre-commit. Existing routine Ruff selection is preserved. ty/pre-commit
configuration and agreed stricter Ruff rules remain pending in starter; policy
is not a claim that those tools are enforced here.

The selected complexity tools are **Ruff 0.15.18 + complexipy 8.0.1 + Lizard
1.24.1**, pinned in the explicit hygiene group. Xenon and Radon are retired from
starter's selected toolchain. Ruff C901 20 and complexipy cognitive 15 are
independent checks, not interchangeable measurements. Deeper hygiene remains
explicitly on demand: no complexity hooks, manual hooks, CI gates or scheduler.

Other on-demand selections are Interrogate, Vulture, Bandit, Coverage.py through
unittest, Cosmic Ray, deptry, pip-audit and Import Linter. Their installation and
full Python 3.14 proofs remain pending; Cosmic Ray is selected, not verified.
pip-audit inspects pinned uv exports without a second resolution. Review package
and pinned-plugin freshness at adoption, reviewed upgrades and quarterly
maintenance on demand; release age alone does not establish abandonment.

Consult the skill's Python 3.14 opportunity guide during design/dependency
review. Assess concrete benefits over 3.13 and porting risks; a version pin
alone supplies no API/idiom guidance or permission for broad modernization.

## Settled C/C/C contract

Read skills/python-engineering/references/ccc-contract.md. The explicit checker
is skills/python-engineering/scripts/complexity_check.py, contract
**lizard-functions-v1**:

- Original source and native Lizard 1.24.1 scores; no Radon emulation or syntax
  normalization. Count functions, async functions, methods and nested functions
  once each. Omit synthetic class blocks, lambdas and module-level statements.
- Ceiling 20 for each function, each module's arithmetic function mean, and the
  overall function-weighted mean. Compare unrounded scores; 20 passes.
- Native assertion semantics: assert itself adds no decision; Boolean decisions
  in its expression count. Empty module means are undefined and excluded from
  denominators; empty scopes without Python files are errors.
- Compile/parse and AST function discovery must agree. Lizard's skipped inline
  suites are unsupported measurements, not hidden passes. Do not rewrite app
  code solely to satisfy Lizard. Missing tools, wrong versions, discovery errors
  and invalid scopes return exit 2; violations return 1; clean checks return 0.
- Explicit relative source scopes, path deduplication, symlink refusal and
  excluded plugin/archive/environment/output trees. No application execution.

This is a reviewed function-based rebaseline, not universal Xenon/Radon parity.
The equal ceilings make averages mathematically bounded by the maximum, but
all three remain explicitly reported and enforced. Preserve failures and compare
stable identities/scores; do not waive them by regenerating snapshots.

## Verification and evidence

Nineteen adoption tests, ten on-demand checker CLI tests, bundle validation,
routine Ruff lint/format and engineering-skill validation passed on Python 3.14.8.
Run checker tests explicitly with the hygiene group; they are not routine CI
complexity gates. Unsupported inline-suite and generated-code suppression tests
verify visible measurement errors rather than fabricated scores.

Final receipts: docs/evidence/2026-10-09-starter-ccc-v1.json and
2026-10-09-cob-reports-ccc-v1.json. Both retain absolute complexity failures with
zero tool errors. Starter has one function violation (maximum 31). Source-only
cob_reports verification measured 88 files and 649 functions: maximum 100,
overall mean 7.14946, 42 function violations and 12 module violations.
No cob_reports dependencies, hooks or app code changed; no protected data was
accessed. Its workboard records the external checker assessment.

The earlier comparison receipt records 585/621 matching legacy function scores.
Combined exploratory Ruff/Lizard/complexipy checks caught all 43 legacy failing
functions and added 31 failures. Class/nested populations differ. These are
specific corpus observations, not a universal compatibility guarantee.

Gzkit issue #1183 records Xenon/Radon retirement and the final findings:
https://github.com/tvproductions/gzkit/issues/1183
Gzkit issue #1184 requests its separate Python 3.14 opportunity/support review:
https://github.com/tvproductions/gzkit/issues/1184
Neither issue implies gzkit implemented starter's checker or changed support.

## Next useful work

1. Check the published revision's CI and independently test authorized native
   onboarding/discovery in a disposable project; record exact loaded sources.
2. Establish Python skill adoption and routine ty/pre-commit enforcement without
   expanding the approved hook set or copying upstream plugin skills.
3. Scope existing complexity remediation separately; retain honest failures.
4. Verify the other selected hygiene tools on invented Python 3.14 fixtures.
5. Review broader gz-skills routing and new-project skeleton improvements only
   when authorized. Keep upstream preferences portable and SP-BP deferred.


## Repository rename — October 10, 2026

The operator renamed the public GitHub template to tvproductions/gz-skills-first-starter. Canonical URL: https://github.com/tvproductions/gz-skills-first-starter. Existing local development checkout remains /Users/jbabb/Documents/Devel/skills-first-starter; the Git origin is updated to the new URL. The skills-first-starter marketplace identifier, Python project name and adoption identities remain unchanged for compatibility. SP-BP remains expected and deferred; no upstream pins or installation behavior changed.

## Baseline maintenance policy — October 11, 2026

The Python runtime family remains 3.14.x; `.python-version`, CI and current
starter commands now select exact patch 3.14.8. This supersedes the minor-only
runtime pin described above. Baseline Python tools must use the latest stable
release within each explicitly selected family, checked at setup/adoption and
scoped on-demand maintenance, then pinned after relevant verification. Record
evidence and revisit conditions for compatibility exceptions; an installed
interpreter does not establish freshness. Other tool/plugin pins are unchanged.

The adopter instructions fragment and front-door skill now pass along maintenance
guidance for the starter template, SP, SP-BP and gz-skills independently. Read
docs/project-configuration.md and docs/adoption.md's stack maintenance procedure.
Preserve app additions, settings and overrides; reconcile managed-file changes
with preview and rollback. No automatic migration, native install, scheduling or
upstream policy change is supplied. SP-BP remains expected, deferred and disabled
until readiness and explicit adoption. Existing adopters must review the changed
fragment/skill; configure refuses to overwrite different managed copies.

Generic maintenance ownership is now explicitly assigned to gz-skills. Route
authorized updates to `gzs-update-dependencies` and dependency-risk assessments
to `gzs-dependency-risk-audit`. The starter retains policy and adoption bindings;
do not implement a duplicate local maintenance skill or generic freshness
reporter. Freshness-only reporting and generalized template/plugin inventory are
upstream enhancement proposals, not verified release capabilities. No upstream
issue filing or plugin change has occurred as part of this decision.

## Template versioning — October 11, 2026

The template now declares independent version 0.1.0 in `bundle.json`, matching
the existing starter package metadata. Read docs/versioning.md and CHANGELOG.md.
No prior tags or GitHub releases were found; the initial baseline is unreleased.
`starter.py version` reports the checkout's label. New configure records include
starter repository, version and full SHA; configure/status/validate output exposes
the version. The label is not proof of release publication or host readiness.
Legacy unversioned locks are preserved and require reviewed reconciliation.
This is additive metadata under schema 1, not automatic migration. Tags/releases
remain a separate authorized operation; no upstream pins or skill ownership changed.

## Initial template release — October 11, 2026

The operator authorized local and GitHub release publication. The initial
template release is v0.1.0; its annotated tag and GitHub release identify the
exact release commit. Recheck the live remote tag and release before continuation.
The release candidate passed 25 unittest tests, bundle/both-catalog validation
and Ruff 0.15.18 lint/format checks on uv-managed Python 3.14.8. GitHub CI must
also be checked on that final commit.

gz-skills main has newer changes, but v0.5.0 remains its latest published release
as checked today. Independent upstream pins remain unchanged. Native host
discovery, ty/pre-commit enforcement and SP-BP readiness remain outstanding;
publication does not certify those capabilities. The historical unreleased
versioning note above describes the state before this publication.

## gz-skills v0.6.0 baseline — October 11, 2026

This supersedes earlier current-pin and proposal statements. gz-skills v0.6.0
was published after the initial starter release and is now selected at exact
commit e722e808647481c4c9d2feab61f1843aa8e0b19a in the bundle and both catalogs.
The starter version is 0.2.0, reflecting new adopted skill capabilities.
Read docs/evidence/2026-10-11-gz-skills-0.6.0.md and its changelog entry.

Freshness-only review and template/plugin inventory are shipped upstream now.
Project setup and Pythonic pattern review/apply bring the catalog to nineteen
skills. No setup invocation, lite/heavy selection, plugin installation or adopter
migration is implied. Starter Python 3.14 and retired-tool decisions take
precedence over upstream defaults. SP/SP-BP pins and SP-BP deferral are unchanged.
Preserve v0.1.0 and historical evidence; verify the new release tag and CI live.

## Zero starter-authored skills — October 11, 2026

This supersedes earlier skill ownership, copying and discovery plans. The user
selected zero authored/distributed skills for the starter. Read `docs/structure.md`,
`docs/adoption-workflow.md`, `docs/engineering/python.md` and `docs/migration-0.3.md`.
SP + SP-BP + gz-skills remains the intended stack; SP-BP stays deferred/disabled.
Python 3.14, Astral tooling, exact verified pins and routine/on-demand boundaries
remain binding. No upstream policy, dependency pins or profile choices change.

The `skills/` tree is removed. Documentation owns adoption and Python policy;
`tools/engineering/` owns the relocated static analysis utilities and CLI tests.
Configure writes configuration, provenance and an instructions fragment with
direct workflow routing; it creates no skill discovery tree. Legacy starter
skill names block preview/apply before writes on all four inspected surfaces;
preserve their content and follow reviewed migration rather than deleting them
automatically. Project-owned operational skills remain supported and preserved.

The working template is 0.3.0, unreleased; metadata and uv lock agree. Current
checks: 28 routine unittest tests, bundle/both-catalog validation, Ruff check and
format, and ten relocated analyzer CLI tests on Python 3.14.8. Historical receipts
retain original paths, hashes and failures. New APIs are unnecessary for this
relocation. Fresh-session host loading and existing enforcement gaps remain
unverified/pending. No plugin installation, schedule, tag or release publication
is implied. Recheck live worktree and publication state before continuation.

`docs/baseline-policy.md` now owns adopter allowed ranges and selection rules,
separately from checkout execution pins: stay current within 3.14.x normally or
host-compatible 3.12.x for XPPython3-bound code. Inspect/test the embedded runtime
separately. Code must observe relevant family-specific idioms, stdlib advances
and deprecations through bounded review, not merely a runtime bump. SP/gz-skills
supply reusable workflows; current Pythonic-pattern skills provide partial
coverage, not a complete version audit. Preserve that capability gap. Release
notes distinguish policy changes from pin refreshes. The relocated analyzer
fixtures now write source explicitly as UTF-8 for Windows portability.

Runtime discovery is owned by gz-skills; do not repeat its three-location
procedure in starter/adopter instructions. The user authorized neighboring
source changes: gz-skills pending 0.7.0 reinforces discovery and scoped current
idiom/stdlib/deprecation assessment in five existing Python workflows, preserving
project-policy precedence and upstream portability. It is unreleased; this
starter remains pinned to v0.6.0 and has not migrated installed consumers.
Read `docs/gz-skills-python.md` for coverage and status. Seven inspected installed
v0.6.0 instruction bodies matched the pinned release's Git blob hashes after
checkout newline normalization; that does not establish fresh-session loading.

## Authorized 0.3.0 / gz-skills 0.7.0 release — October 11, 2026

The user authorized publication of both releases. gz-skills v0.7.0 is published
at `6ebf803e4a2775d3742c84984a03548275b7c926` with immutable tag, wheel/sdist and SHA-256 checksums. Its five
Python workflows own runtime discovery and scoped version-aware practices.
Tagged installs passed in disposable Codex/Claude configuration and uvx snapshots;
see `docs/evidence/2026-10-11-gz-skills-0.7.0.json` for limits and channel status.
The starter selects that exact commit in its bundle and both catalogs. Earlier
pending-release and v0.6.0-current statements above are historical.

Starter 0.3.0 releases the zero-skill structure and explicit baseline policy.
Recheck the published tag, release commit and GitHub CI before continuation.
Adopters must reconcile legacy skill copies/managed records; no automatic app
migration, profile selection or SP-BP activation occurs. Fresh-session combined
stack loading and existing enforcement gaps remain separate from publication.

## Adopter cohesion minimum — October 11, 2026

The user clarified that the selected Python tools establish an adopter minimum,
independent of the starter helper's own needs, and selected patch version 0.3.1
for this change. Cohesion is required for downstream on-demand class analysis.
The baseline policy, Python policy and generated instructions fragment carry
the requirement. Adopters own version selection, pins, runtime verification,
class-score interpretation and recorded inapplicable scopes; no universal
threshold or compatibility proof is supplied by the starter.

The development metadata selects 0.3.1, unreleased. No cohesion dependency is
added to the starter environment. Existing runtime/tool/plugin pins and routine
hook/CI choices are retained. Recheck live state and verification before release;
publication and migration of other projects remain separately authorized work.

## Independent SP update — October 11, 2026

The user authorized updating SP to latest stable and selected another patch.
The 0.3.2 development template selects SP v7.0.0 at
`bb92a77741419a4ab5f06e711a283343f1ada0c3` in the bundle and both catalogs.
Read `docs/evidence/2026-10-11-superpowers-7.0.0.md` for the official release and
manifest review. Earlier v6.4.1-current statements above are historical.
Backplane is independently pinned and remains disabled; its old compatibility
baseline does not constrain active SP. Before future enablement, review its
readiness and SP 7 compatibility. No installed plugins or other projects are
updated. Recheck live publication and host verification state before continuation.

## Astral alignment and starter remediation — October 18, 2026

The user requires maximal Astral alignment, including necessary adopter
refactoring and remediation of the starter itself. Read
`docs/engineering/astral-alignment.md` and
`docs/evidence/2026-10-18-astral-alignment.md`. Preservation during helper
configuration does not exempt an adopter from the required baseline. Full
adoption includes bounded verified reconciliation; constrained exceptions need
evidence, an owner and revisit condition. Existing authorities and public
behavior remain binding. Cargo-style workspaces apply to compatible connected
packages, with explicit dependency edges, not every repository.

Development version is now 0.4.0, unreleased. Helper code is an installed
`src/skills_first_starter` package with uv_build and a console command; the root
script is a compatibility launcher. Root bundle/catalog/template files remain
authoritative; regenerate checked wheel resources with
`uv run --locked python tools/package_resources.py` after changes. Installed
wheels need explicit published `--starter-ref` provenance. No skills are authored
or redistributed, and no profile was selected. Current gz-skills pin is 0.8.0,
superseding earlier current-pin statements; SP and deferred Backplane are unchanged.

Routine ty/pre-commit enforcement and reviewed stricter Ruff selection are now
implemented, superseding earlier gap statements. Local hooks are installed.
Read current AGENTS.md/README checks. Observed local Windows verification:
31 adoption tests, eleven explicit analyzer tests, bundle/both catalogs,
Ruff check/format, ty, pre-commit, locked sync/lock check, wheel built from sdist
and isolated installed CLI verification. The Windows legacy-locale probe failure
was fixed with Python source-encoding detection and a regression test. Static
portability checks pass. On-demand audit reports no known vulnerabilities in
17 third-party packages, with experimental uv audit limitations recorded.

Python stays 3.14.8. uv/uv_build are 0.13.1, Ruff 0.15.22 (retaining 0.15.x),
ty 0.0.89 (beta exception), pre-commit 4.7.0; complexipy/Lizard unchanged. CI
uses reviewed immutable checkout/setup-uv selections and exact tool/runtime pins.
Actual remote CI and fresh-session native skill loading remain unverified on
this candidate. Existing complexity debt, other on-demand tool proofs and
shared/local utility ownership remain open. No commit, push, tag, release,
installed-plugin change or adopter migration is implied by this work.

## Complexity backlog item completed — October 18, 2026

The user requested continuing with the next backlog item. The repository-local
complexity remediation is complete in the existing unreleased 0.4.0 candidate;
all preceding alignment work is retained. Read
`docs/evidence/2026-10-18-complexity-remediation.md` and its before/after receipts.
Adoption validation/rendering/planning/writing are decomposed without changing
public behavior. The checker scope resolver is also decomposed; native scoring,
fail-closed discovery and `lizard-functions-v1` are unchanged.

Ruff C901, complexipy and Lizard all pass over `src tests tools` at the existing
ceilings. Lizard maximum drops 30 to 16, cognitive maximum is 14; the measured
population increases 81 to 98 through extraction and new tests. Historical failing
receipts remain intact. Latest verification: 35 routine adoption tests, twelve
explicit analyzer tests, approved pre-commit checks, ty/Ruff, catalogs, lock,
build and isolated installed CLI checks. This supersedes the prior current-state
statement about existing starter complexity debt. No complexity hook/CI gate,
dependency refresh, tag, release or adopter mutation was introduced.

Remaining work includes fresh-session host/adopter proofs, shared/local utility
ownership and selected deeper-analyzer verification, especially Cosmic Ray's
Python 3.14 unittest proof. Do not claim those from passing local package checks.
