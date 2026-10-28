# Adopter baseline policy

The current template is Python-only in both lite and full/heavy adoption lanes.
Other languages, likely including Go, require a future designed and released
baseline; the portability of upstream skills does not establish template support.

## Required adoption lane and completion

[Backplane owns the lite/heavy mode definitions](https://github.com/tvproductions/superpowers-backplane/blob/main/docs/superpowers-backplane/modes.md)
and the requirements, labeling, backlog/release monitoring and handoff workflows.
This template references that authority; it supplies no alternative mode lifecycle.
Every adopter explicitly records `lite` or `heavy` through the pinned gz-skills
setup workflow. Keep its existing settings schema and choices; a missing file or
`profile: null` is pending selection. The stored value records intent, not proof
that the selected Backplane capabilities are installed or ready.

Both modes meet this template's same applicable Python/Astral foundation,
SemVer/PRD policy and required adoption/release analysis. Backplane remains under
development and disabled until readiness and explicit activation. Preserve
existing project authorities meanwhile; do not implement the missing management
workflows here or certify whole-stack readiness from a profile selection.

Follow the [greenfield and brownfield runbook](adoption-0.5.md). Track lane,
configuration, Python conformance, required analysis and native readiness
separately. Required FAIL/UNKNOWN/stale evidence blocks strict acceptance.
Evidenced exceptions remain visibly conditional, never 100% conformance.
The helper does not enforce these acceptance decisions automatically.

Prove Python baseline adoption through the
[Astral acceptance contract](engineering/astral-acceptance.md), retaining actual
evidence, applicability and owned exceptions in project authorities. Applicable
Astral recommendations are the default to adopt and verify; configuration-only
helper success does not establish full baseline or native-host acceptance.

This is the adopter-facing authority for version selection. Read it at the
reviewed starter version/SHA recorded in `.skills-first/bundle.lock.json`, then
compare it with later published releases during maintenance. A copied exact pin
is evidence of one tested environment; it is not the template's permanent
requirement for every adopter.

## Release planning

Adopters version their own public product contract using `MAJOR.MINOR.PATCH`:
after 1.0, incompatible changes require major, compatible additions minor, and
compatible fixes patch. During 0.x, additions and changes requiring reconciliation
increment minor; compatible fixes increment patch. Define the project's public
contract and explain compatibility impact in release notes. See the full
[version contract](versioning.md#version-contract), including deprecations.

The starter and adopting projects follow the same release-planning rule for
their independently versioned products: **every major release, including 1.0.0,
always requires a newly written PRD** for that major. Reference it in release
preparation and evidence; a reused PRD or version-number change alone is
insufficient. Each adopter keeps its PRD in its project-owned authority.

Minor releases bundle a coherent selected set of related changes using the
project's existing backlog and handoff practices. SP-BP is intended to help
coordinate bundles after readiness and explicit adoption; while deferred, keep
the existing authorities. Patch releases remain compatible fixes and
clarifications. Preserve compatibility classification as well as release scope;
see [versioning](versioning.md#version-contract) for the starter's 0.x/stable
rules. These obligations do not authorize publication or adopter-file rewrites.

## Allowed Python families

Ordinary GZ projects deliberately stay **one stable Python minor release behind**
(N-1). Python 3.15 is currently the latest stable minor, so the selected family
is 3.14, always at its latest verified patch. This is an explicit runtime policy,
not permission to keep old tool families. Review the N-1 selection when Python
adds a stable minor and migrate deliberately; do not silently change interpreter
families during dependency resolution. Host-bound code follows its supported
runtime exception instead.

| Project scope | Allowed range | Selection rule | Reason |
| --- | --- | --- | --- |
| Ordinary Python project | `>=3.14,<3.15` | Latest verified stable 3.14 patch | User-directed N-1 runtime policy |
| XPPython3-bound code | `>=3.12,<3.13` | Latest verified stable host-compatible 3.12 patch; record the actual embedded patch separately | Host compatibility, not a general preference for an older Python |

These ranges select one minor family per scope, not permission to resolve any
Python version above a minimum. Match project metadata, Ruff/ty targets, local
execution and CI to the selected family. Split standalone and host-bound scopes
only when the project has a real boundary and separate verification; do not infer
that all dependencies or shared code support both families.

XPPython3's current [installation guidance](https://xppython3.readthedocs.io/en/latest/usage/installation_plugin.html)
shows Python 3.12 and its [development guidance](https://xppython3.readthedocs.io/en/latest/development/index.html)
describes an integrated interpreter, checked October 11, 2026. The host owns that
runtime. Check the installed host/version and actual Python patch, review stable
host updates and test in the host. Updating a standalone uv interpreter does not
update the embedded interpreter. If the host restricts a patch or family, record
the supported selection, official evidence, reason and revisit condition. Do not
independently replace the embedded runtime to satisfy a freshness target.

## Tool and dependency selection

Maximal [Astral alignment](engineering/astral-alignment.md) is required for
project structure, Python configuration, packaging and execution. Adopters must
refactor nonconforming code/configuration as part of baseline adoption, or record
an evidenced compatibility exception with an owner and revisit condition.
Preservation during configuration is not permanent exemption from the baseline.

Use uv for standalone Python, project environments, dependency resolution and
locks; use Astral Ruff for lint/format and ty for type checking. Use unittest and
pre-commit for the approved routine checks. Keep deeper analysis outside hooks
and routine CI. Execute applicable deeper analysis at adoption and release
acceptance, plus on demand; a tool inventory alone is insufficient.
[Python engineering policy](engineering/python.md) defines those checks
and the required engineering practices; missing enforcement remains a reported gap.

The engineering policy's selected on-demand tools are a minimum standard for
adopters, independent of the starter helper's own tooling needs. This includes
`cohesion` for class cohesion analysis, with adopter-owned version selection,
pins and runtime verification. Record inapplicable scopes and compatibility gaps
explicitly; keep these checks outside hooks and CI gates. Adopters may add
project-specific tools without weakening the adopted minimum.

Use the latest stable release of every selected baseline tool, verified against
official live sources. This binds the starter itself and both adopter lanes.
Compare newer stable families as well as patches: an old allowed range or exact
pin cannot be used to declare a stale tool current. Review release changes and
compatibility, adopt the newest stable selection, then retain exact pins/locks.
The explicit Python/embedded-host families above remain separate runtime policy.

An older tool is permitted only as an explicit compatibility exception with
evidence, an owner, accepted-by authority and a dated revisit. It remains
noncurrent/conditional; do not claim strict freshness acceptance. Missing latest
release evidence, untested compatibility or a known incorrect analyzer is not a
passing result. Do not widen application support claims or override dependency
constraints merely to obtain a newer resolution. Application dependency intent
remains project-owned; assess its latest stable compatible selections and record
why an older constraint is retained.

Application dependencies and their compatibility bounds remain project-owned.
SP, SP-BP and gz-skills remain independently versioned with full-SHA source pins.
Select updates independently under reviewed compatibility decisions; SP-BP stays
disabled until readiness and explicit adoption. An upstream default does not
override this baseline or the project's existing authorities.

## Code must follow its Python version

gz-skills owns runtime discovery for Python workflows. Require it to honor the
project's adopted allowed ranges, supported runtime and engineering policy, report
conflicting or missing evidence, and verify host compatibility where applicable.
The starter does not duplicate its discovery algorithm or supply a parser/helper.
Source coverage and unreleased upstream work are recorded in the
[Python workflow mapping](gz-skills-python.md).

A current interpreter is not sufficient. At adoption, runtime-family changes,
feature design, code review and scoped maintenance, assess the relevant code
against the selected Python family's current idioms, supported APIs, deprecations
and standard-library improvements. Preserve required public behavior while
replacing outdated patterns where there is a demonstrated benefit. Do not leave
an older approach solely because the runtime still accepts it.

Use versioned official documentation and record the affected scope, candidate,
benefit, compatibility risk, adopt/defer/not-applicable decision and verification.
Use the [3.14 opportunity guide](engineering/python314-opportunities.md) for 3.14
code; assess XPPython3-bound code against 3.12 and the actual host. Retained older
patterns need a reason where a concrete improvement was identified. Review code
through bounded changes rather than treating a runtime update as permission for
an application-wide rewrite or adopting every new feature.

Use the [verified gz-skills Python mapping](gz-skills-python.md) to select
pattern detection/application, cross-platform review or scoped debt/change review.
gz-skills owns reusable engineering review/refactoring workflows; SP supports
feature design and implementation. Use discovered, version-appropriate gz-skills
workflows to assess and implement authorized changes while applying this project's
runtime policy. The pinned Pythonic-pattern detect/apply skills cover concrete
pattern simplification; they do not establish a complete Python-version idiom or
stdlib audit. If the installed release lacks a needed workflow, report the gap
and assess the scoped code against the linked versioned documentation. Do not
claim upstream capability or add a competing starter skill.

This is an explicit dependency on separately versioned gz-skills capabilities,
not permission to put starter-specific Python preferences into upstream plugins.
Record the workflow release and its scope when relying on it; review a future
upstream capability before changing the project's routing or claiming coverage.

## Reproducible execution and maintenance

Check official release information at setup/adoption, before each release, scoped
upgrades and quarterly on-demand maintenance. Verify the latest stable tooling
and latest patch in the explicitly approved Python family against relevant
project checks, then record the exact selected Python patch in
`.python-version` and CI and exact dependency/tool resolutions in the appropriate
lock/configuration. Keep that environment stable between authorized updates;
do not resolve a moving latest version on every run. A freshness-only review
reports gaps without changing pins or environments.

An installed interpreter, an allowed range or a passing lock validation does not
establish freshness. Record the checked date, selected/latest versions, official
evidence, compatibility findings and adopt/defer decision. A demonstrated
compatibility exception requires a reason and revisit condition. A new family
requires compatibility review, not automatic indefinite deferral; a newer
template does not silently change project policy. The starter maintainer and each
adopter own release/adoption eligibility: required stale, unknown or unverified
freshness evidence blocks acceptance. gz-skills supplies the maintenance workflow;
it does not replace this responsibility. Retain dated evidence for the actual
candidate inputs and recheck live releases for each release preparation.

The starter itself also needs an exact interpreter/tool set to verify its helper.
Its `.python-version`, CI, `pyproject.toml` and `uv.lock` describe that checkout's
execution baseline. They are separate from the allowed-range policy above.

Template release notes must distinguish **policy changes** (allowed families,
required tools, compatibility exceptions or verification obligations) from
**pin refreshes** within existing policy. Review both, reconcile affected project
guidance/configuration, and preserve project additions and rollback evidence.
Follow [stack maintenance](adoption.md#maintaining-the-adopted-stack) through
gz-skills. Scheduled scans and update PRs are permitted as described below;
this policy adds no competing maintenance skill or generic freshness reporter.

## Scheduled dependency scanning

This repository maintains a reviewed dependency baseline for adopters to consult.
Adopters choose starter updates, independent upstream updates or both, and own
their update timing, compatibility decisions and project verification. Consulting
this baseline does not require adopting its scanning service or schedule.

Scheduled scanning and dependency-update PRs must cover both cases independently:

| Baseline | Required inputs | Verification boundary |
| --- | --- | --- |
| Standard Python | Python 3.14.x project declarations, exact interpreter/tool pins and uv lock | Checks on the selected managed interpreter and installed artifacts |
| X-Plane/XPPython3 | Host-compatible Python 3.12.x project declarations, exact interpreter/tool pins and separate uv lock | Standalone checks plus separate evidence from the actual embedded host |

Keep Python dependencies and supported tool configuration in each baseline's
`pyproject.toml`, with uv-generated locks and exact `.python-version` files.
Use independent projects/environments for these incompatible runtime families,
not one shared workspace resolution. Do not duplicate app-specific X-Plane
dependencies from another adopter; application dependencies remain project-owned.
Track Python and uv execution pins and GitHub Actions revisions in their native
files as part of coverage. Plugin/catalog inventory remains separately required;
a package scan does not establish plugin freshness or native discovery.

Propose current stable tooling independently for each runtime; any retained
incompatible version needs the existing evidenced exception and revisit condition.
Keep Python-family changes under explicit review and preserve exact pins between
updates. Regenerate affected locks and packaged resources through their owning
tools, and run applicable repository and changed-tool checks before merge.
Do not automatically merge, publish releases, activate Backplane or update native
plugin installations. Scans and passing CI do not replace release-specific
freshness receipts, compatibility review or embedded-host verification.

This checkout configures weekly Dependabot jobs for the standard helper's Python
3.14 project, the independent Python 3.12 tool project in `baselines/xplane/`,
and GitHub Actions. See [coverage and limits](engineering/dependabot.md).
The X-Plane project is a dependency-only standalone reference, not a simulator
plugin or host certification. Hosted scans and actual update PRs remain UNKNOWN
until observed after the configuration reaches the default branch. Python/uv
execution pins, plugin catalogs and missing deeper tools still require the
existing maintenance review. Missing inputs, failed queries and unverified host
behavior must remain explicit gaps; local configuration is not operational proof.
