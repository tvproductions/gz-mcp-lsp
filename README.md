# GZ skills-first starter

A reusable, project-scoped starting point for **Superpowers + Superpowers Backplane + gz-skills**,
with room for each application's own operational skills and supporting code. Built for work and personal projects under `tvproductions`.

Its primary purpose is consistent engineering across the maintainer's own
projects. It deliberately records personal, strict design and tooling choices;
usefulness to other adopters is welcome, rather than a reason to dilute them.

This repository is the bundle catalog, adoption tool, and guidance home.

It is also the [policy alignment source](docs/versioning.md#ecosystem-policy-authority-and-consistency)
for the maintainer's gz-skills and Backplane repositories. Backplane owns
[lite/heavy modes](https://github.com/tvproductions/superpowers-backplane/blob/main/docs/superpowers-backplane/modes.md),
requirements tracking, labeling, backlog/release monitoring and handoffs.
The template refers to those workflows; it does not implement them.

Release **0.7.1** prepares independent qualification and consumer checks for
the future gzkit-owned cognitive engine and refreshes Ruff to 0.17.3 in both
Python baselines. No engine is installed or certified. Cognitive integration is
an open, unscheduled [follow-up, issue #1](https://github.com/tvproductions/gz-skills-first-starter/issues/1),
and does not block this release. The maintainer explicitly retains the cognitive
exception; this release does not claim strict cognitive acceptance. See the
[release evidence](docs/evidence/2026-10-26-0.7.1-release.md) and
[integration boundary](docs/engineering/cognitive-integration.md).

Version **0.6.0** includes the single template-owned `update-gz-template` skill.
See [canonical template updates](docs/updating.md), including bootstrap for
0.5.0 and earlier adopters.

**This is currently a Python-only template**, for both lite and full/heavy
adoption. Other language baselines, likely including Go, are future work and
are not supported adoption targets yet. Python's policies do not implicitly
define requirements for a future language baseline.

Future guidance will distinguish language, execution/deployment environment and
application type: CLIs, TUIs, web apps and desktop apps. Each supported target
will need explicit requirements and verification extending the shared foundation.
Current CLI guidance does not certify all of those future combinations.

Python projects must meet the [Astral alignment contract](docs/engineering/astral-alignment.md):
`src/` packaging, uv-managed locked execution, centralized Python configuration,
installed-artifact verification and aligned local/hook/CI checks. Adopters should
expect to refactor nonconforming projects; existing layout alone is not an exemption.
Use the [Astral acceptance record](docs/engineering/astral-acceptance.md) and
[worked application/library/workspace migrations](docs/engineering/astral-migrations.md)
to prove the result, including effective configuration and clean installed behavior.
**The starter owns one template-update skill.** Upstream plugins supply
the other engineering skills;
the starter supplies opinionated policy, deterministic configuration and provenance.
Adopters own update review and project operational skills. See the
[repository structure and ownership contract](docs/structure.md). It is
not another development lifecycle or an application framework. Existing projects
can adopt it without replacing their architecture. **xplane-fdau is the primary
reference implementation**, not a template whose domain rules should be copied.

The starter reinforces and highlights the behaviors supplied by gz-skills so
adopters understand the emphasis: keep runtime/dependency choices current through
`gzs-update-dependencies`, use Python-specific workflows for idiomatic code and
portability, and apply them under the project's adopted engineering policy.

The [adopter baseline policy](docs/baseline-policy.md) states allowed version
ranges and tool-selection rules. This checkout's exact pins describe a verified
execution environment; adopters maintain their own current verified selections
within policy. Review policy changes separately from pin refreshes.
Code must also follow relevant idioms and advances of its selected Python family;
a current runtime alone does not satisfy the baseline. Apply the policy through
SP/gz-skills workflows using the [verified Python skill mapping](docs/gz-skills-python.md)
and report gaps in their version-specific review coverage.

**SP-BP is an expected addition to the target SP + SP-BP + gz-skills stack,
but is not ready for normal adoption.** It remains cataloged and pinned for
future work, but the helper explicitly disables it and the default installation
steps omit it. Keep your existing backlog and handoff process. This starter does
not supply the missing Backplane implementation or certify the combined stack.

For current SP and gz-skills versions, follow
[checking and adopting upstream updates](docs/adoption.md#getting-current-sp-and-gz-skills).
The bundled pins are a reproducible baseline, not a promise to track latest.

Adopters can add dependencies, extend configuration and select reviewed overrides.
Use `pyproject.toml` or a project-owned `settings.json` for application settings;
Python dependencies still belong in `pyproject.toml` with a project-owned lock.
See [configuration and baseline maintenance](docs/project-configuration.md) for
ownership, freshness review and the helper's current preservation limits.
Adopters maintain the template, SP, SP-BP and gz-skills independently using
[stack maintenance](docs/adoption.md#maintaining-the-adopted-stack), including
tracking SP-BP readiness while it remains disabled.
Generic maintenance workflows belong to gz-skills; the starter supplies policy
and adoption bindings rather than another maintenance skill or freshness tool.

This checkout configures weekly Dependabot update PRs for its standard Python
project, a separately locked [X-Plane/XPPython3 tool baseline](baselines/xplane/),
and GitHub Actions. See [coverage and remaining manual review](docs/engineering/dependabot.md).
Hosted scans require observation after merge; local configuration does not prove
operation or embedded-host compatibility. Adopters choose starter updates,
independent upstream updates or both, and their own update timing.

## Agent: start here

The template has its own version, independent of its plugins and adopter apps.
`bundle.json` owns `template_version`; `starter.py version` reports it, and new
adoption records both version and full commit SHA. See
[versioning and release policy](docs/versioning.md) and [changelog](CHANGELOG.md).
The template baseline is [v0.7.1](https://github.com/tvproductions/gz-skills-first-starter/releases/tag/v0.7.1).
Start with the [greenfield/brownfield runbook](docs/adoption-0.5.md), including
existing-adopter upgrades and explicit acceptance/release requirements.
Verify a published tag and exact commit before adoption; a metadata value
alone is not proof of a release.

Read the target project's `AGENTS.md` and linked authorities, then read
[the adoption workflow](docs/adoption-workflow.md). Identify which path the
user requested before changing files:

| User's goal | Entry |
| --- | --- |
| Adopt into an existing project | Inventory installed sources, preview configuration, preserve existing authorities |
| Backport a preferred structure | [Structure mapping guide](docs/backport.md); make useful changes incrementally |
| Start a new project | [Use this template](https://github.com/tvproductions/gz-skills-first-starter/generate), then adapt the copied starter material to the product |
| Use an already adopted project | Project operational skills first; `gzs-router` for engineering skill selection; SP for feature design and implementation |

The adopter instructions route project operations to project-owned skills,
feature work to SP and engineering selection to gz-skills `gzs-router`. These
are references to independently maintained workflows; the starter installs no
routing skill or engineering catalog.

For starter development or a fresh-chat continuation, read
[the current handoff](docs/handoffs/2026-10-24-session-close.md).

## Quick start: an existing or empty project

Requires uv, Python 3.14, Git, and Codex with plugin support. GitHub CLI is useful
for checking upstream releases; Backplane's GitHub workflows remain deferred. No Python dependencies are needed for this tool.

Baseline tools use their latest stable release across tool families, with exact
pins after verification. Explicit Python/host runtime families remain distinct;
an older tool family is not a freshness exemption. Adopters stay current within Python 3.14.x,
or host-compatible 3.12.x for XPPython3-bound code. This starter's execution pin
is 3.14.10 (checked October 26, 2026), not a permanent adopter patch requirement.
Recheck at setup/adoption and scoped maintenance;
an installed older patch is not a freshness check. See the
[baseline rule](docs/engineering/python.md#latest-stable-within-the-selected-family).

```bash
git clone --branch v0.7.1 https://github.com/tvproductions/gz-skills-first-starter.git
cd gz-skills-first-starter
uv run --locked skills-first-starter validate
uv run --locked skills-first-starter configure --project /path/to/your-project
uv run --locked skills-first-starter configure --project /path/to/your-project --apply
```

The first configure command previews paths without writing. The second writes
project Codex settings, a pinned bundle record and an instructions fragment.
Configure also seeds the single project-scoped
`.agents/skills/update-gz-template/SKILL.md`; published 0.5.0 does not. SP and gz-skills are
enabled; SP-BP is explicitly disabled.
Existing `AGENTS.md` is preserved; new projects get an entry pointing to the
fragment. Existing configuration is extended only when it is compatible.
Conflicts, legacy duplicate skill discovery, symlinked destinations, and gzkit
projects stop before any writes. Repeating adoption with the same inputs is a
no-op. Review the configuration before trusting it in Codex.

Then follow [native installation and verification](docs/adoption.md). Configuring
files does **not** install plugins, authenticate GitHub, or prove skill discovery.
The native managers own their caches; upstream skills are never copied here.
Complete the [greenfield/brownfield runbook](docs/adoption-0.5.md), including
explicit lite/heavy selection and required adoption/release analysis. Configure
and status do not certify Python conformance or complete an existing migration.

```bash
uv run --locked skills-first-starter status --project /path/to/your-project
```

For agent-guided adoption, read [the adoption workflow](docs/adoption-workflow.md).
You can also [use this repository as a GitHub template](https://github.com/tvproductions/gz-skills-first-starter/generate),
then configure your new checkout from a separate, reviewed starter checkout.
A generated repository inherits the starter files; simplify it for your product
rather than turning this scaffolding into runtime dependencies. Running the copied
helper inside an adopting repo requires an explicit published `--starter-ref`;
the default refuses to mistake an adopting repo commit for a starter revision.

## Backporting an existing project

```bash
uv run --locked skills-first-starter backport --project /path/to/your-project
```

This read-only assessment suggests responsibilities to map onto existing material.
It does not move code or read operational record contents. Use
[backport guidance](docs/backport.md) to build a concrete mapping and apply useful
changes in small verified steps. Preserve current backlog practice while SP-BP
is deferred.

The [adopter instructions](templates/AGENTS.skills-first.md) provide direct
workflow routing and maintenance obligations. gz-skills supplies `gzs-router`
for its own catalog, including the released Pythonic pattern review/apply pair.
Profile setup remains a separate explicit adopter choice. Existing adopters
reconcile retired starter skill copies using the [migration guide](docs/migration-0.3.md).

## This checkout's bundle

The canonical pins are in [bundle.json](bundle.json). Both native catalogs use
those exact full commit SHAs, not moving branches.

| Component | Initial baseline | Owns |
|---|---|---|
| [Superpowers](https://github.com/obra/superpowers) | v7.0.1 | Feature design, plans, implementation, review |
| [Superpowers Backplane](https://github.com/tvproductions/superpowers-backplane) | Deferred; disabled by default | GitHub-backed backlog and handoff continuity |
| [gz-skills](https://github.com/tvproductions/gz-skills) | v0.8.0 | Portable engineering disciplines |
| Your app | Project-owned | Operational workflows, domain rules, code, evidence |

Published template 0.6.0 retains its original SP 7.0.0 selection.
Template 0.7.0 selects Superpowers
[v7.0.1](https://github.com/obra/superpowers/releases/tag/v7.0.1), the latest stable
release checked October 24, 2026. The old v6.4.1 selection came from Backplane's
recorded compatibility proof; deferred Backplane does not constrain active SP
updates. Review SP independently using the update guide. See the
[update assessment](docs/evidence/2026-10-11-superpowers-7.0.0.md) for scope and
verification limits.
This is a reviewed
starting set, **not a blanket compatibility certification**. Backplane has no
published release; its remaining host acceptance and external pilot are tracked
upstream. The pinned gz-skills release contains twenty skills, including
project setup, Pythonic pattern review/apply and freshness-only maintenance
review with template/plugin inventory. The starter does not invoke setup or
select a lite/heavy profile. Explicit selection is required before adoption is
complete; both lanes meet the same Python foundation and required adoption/release
analysis. Heavy retains deferred Backplane in its intended stack.
Approved starter Python policy takes precedence
over upstream profile defaults, including Python 3.14 and retired-tool choices.

## Current scope

- Implemented: immutable bundle catalogs, Codex project configuration, preview,
  idempotent adoption, conflict preservation, status, project instructions,
  read-only backport assessment, and automated tests.
- Claude Code: native bundle marketplace supplied; project install guidance
  documented. End-to-end installation is not verified by this starter yet.
- OpenCode: deferred until Backplane's adapter and variant verification exist.
- Fresh-session Windows Codex CLI discovery has a [v0.4.0 acceptance receipt](docs/evidence/2026-10-18-codex-discovery-verified.md),
  including pinned skill bytes and an outside-project control. Desktop UI,
  other harnesses and Backplane conformance remain separate operator-run checks;
  configuration or a manifest version is never treated as proof.
- No GitHub issue mutation, app migration, global installation, scheduling,
  autonomous jobs, or release publication occurs through `starter.py`.

See [architecture](docs/architecture.md), [adoption](docs/adoption.md), and
[roadmap](ROADMAP.md) for the boundary and remaining work.

## Checks

```bash
uv sync --locked --all-groups
uv run --locked pre-commit run --all-files
uv run --locked skills-first-starter validate
uv build --no-sources
uv run --locked python tools/verify_distribution.py
```

The tool uses Python's standard library. Non-gzkit projects started from this
starter carry its required Python engineering standards: uv-managed, pinned
Python 3.14; Ruff check/format, ty, unittest and pre-commit; current idioms;
stdlib-first code and explicit domain/adapter boundaries. See the versioned
[Python engineering policy](docs/engineering/python.md), including the
XPPython3 version exception and on-demand hygiene selections: Ruff C901 plus
cognitive scoring at ceiling 15 and Lizard (retiring Xenon and Radon),
Interrogate, Vulture, Bandit, Coverage.py, Cosmic Ray, deptry, pip-audit and
Import Linter, plus cohesion for adopter class cohesion analysis. These selections
form an adopter minimum standard, independent of the starter helper's own needs.
Adopters own cohesion pins and runtime verification. These deeper checks stay
outside routine hooks and routine CI. Complexipy is retained only to reproduce
its qualification defect; the selected gzkit-derived shared scorer is deferred
and not installed. Cognitive acceptance remains blocked. See the
[assessment](docs/evidence/2026-10-24-gzkit-cognitive-extraction.md).

The starter packages its helper under `src/skills_first_starter/`, uses uv_build,
and pins Ruff, ty and pre-commit in its dev group. The approved four routine hooks
run the same locked commands locally and in CI. Install them in a development
checkout with `uv run --locked pre-commit install`. The old `uv run starter.py`
launcher remains available; prefer `uv run --locked skills-first-starter`.
Regenerate wheel resources with `uv run --locked python tools/package_resources.py`
after changing the bundle, either catalog or the instructions template; tests
check their agreement. Wheels require explicit published `--starter-ref` for
configuration because an installed environment has no starter Git provenance.

Cosmic Ray 8.7.0 now has a bounded Windows/Python 3.14.8 synthetic unittest
proof, with killed/surviving mutants and explicit failed-baseline, timeout and
launch-error controls. Its baseline CLI can return zero for a launch error;
inspect structured outcomes as described in [the compatibility evidence](docs/evidence/2026-10-18-cosmic-ray.md).
Other deeper-tool gaps remain outstanding. The configuration helper writes an instructions fragment;
read the full Python policy from a reviewed starter checkout or reconcile it into
project-owned documentation with provenance. Supporting analysis utilities live
in `tools/engineering/`. Shared/local utility ownership still requires a design
decision. Existing Python adopters must reconcile the Astral baseline through
reviewed refactoring or evidenced compatibility exceptions. Preserve public contracts
and numeric thresholds; do not transplant another project's gates.

## Attribution and license

Original starter code and documentation are MIT licensed. Referenced projects
retain their own licenses and owners. The catalogs point to upstream sources;
this repository does not redistribute upstream skills. See [NOTICE](NOTICE).
