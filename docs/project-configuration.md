# Project configuration and dependency baseline

The starter supplies a small engineering baseline that projects can extend.
It does not supply a closed application dependency list. Projects may have many
runtime packages, optional features, development groups and local adapters.
Keep those declarations and their ownership when adopting or updating the stack.
The helper itself uses the standard library and requires no runtime packages.
Use the [0.5 adoption/migration runbook](adoption-0.5.md) for mandatory lanes,
existing managed-file reconciliation and required acceptance evidence.

## Choose the configuration home

Python project metadata, builds, dependencies and supported uv/Ruff/ty settings
belong in `pyproject.toml` under the required
[Astral alignment contract](engineering/astral-alignment.md). Separate native
hook/CI/host files retain their own contracts. Existing projects must reconcile
nonconforming configuration and structure as part of full baseline adoption.
Verify the resulting effective configuration and execution through the
[Astral acceptance contract](engineering/astral-acceptance.md), including uv's
own configuration/override precedence, selected environment and tool provenance.
Centralized declarations alone do not prove that the tools used them.

Use either `pyproject.toml` or a project-owned `settings.json` for application
settings, following the project's existing convention. Link the chosen file and
its loader from project instructions. Python dependency declarations still belong
in `pyproject.toml`, with resolved versions in `uv.lock`; JSON application settings
do not replace uv's dependency metadata.

| Concern | Authority |
| --- | --- |
| Runtime packages | `project.dependencies` in `pyproject.toml` |
| Optional application features | `project.optional-dependencies` |
| Development and on-demand tools | Separate `dependency-groups` |
| Workspace membership and local member dependencies | Root `tool.uv.workspace`, member dependencies and `tool.uv.sources` |
| Exact resolved Python environment | Project-owned `uv.lock` |
| Application settings | A project namespace under `tool` in TOML, or project-owned `settings.json` |
| Plugin sources | Reviewed bundle and native marketplace configuration |
| Adopted template identity | Starter version and exact SHA in `.skills-first/bundle.lock.json` |
| gz-skills profile | Its version-specific `.gz-skills/settings.json` contract |

See uv's official [dependency field guide](https://docs.astral.sh/uv/concepts/projects/dependencies/).
An application `settings.json` is separate from `.gz-skills/settings.json` and
host settings. Preserve the latter files' own schemas and explicit profile
choices. Neither the starter nor uv supplies an application settings loader.

For example, an invented application could choose this TOML namespace:

```toml
[tool.example_app]
schema_version = 1
output_directory = "products"

[tool.example_app.extensions]
enabled = ["summary_export"]
```

Or the same application could choose JSON:

```json
{
  "schema_version": 1,
  "output_directory": "products",
  "extensions": {"enabled": ["summary_export"]}
}
```

These illustrate application-owned schemas, not new starter inputs. Choose one
source of truth; if an existing project needs both, document their distinct
responsibilities and precedence instead of duplicating values.

## Additions, extensions and overrides

Add app dependencies to the existing project declarations. Extend optional
features and dependency groups without replacing unrelated entries. Keep routine
tools separate from on-demand hygiene, which remains outside hooks and CI gates.
The standard-library preference requires a reason for additional packages, not
a prohibition on them. Record purpose, compatibility and resource cost at the
appropriate project seam.

Projects may select newer compatible tool versions or different package sources.
Review the changed version constraint or source in project metadata and resolve
the project lock. For transitive incompatibilities, distinguish constraints that
narrow supported requirements from uv overrides that replace requirements; an
override needs evidence that the resulting combination works. Consult uv's
[resolution guide](https://docs.astral.sh/uv/concepts/resolution/). Record the
reason, affected packages, compatibility checks and rollback version in project
decisions. Do not discard a dependency conflict to make adoption appear successful.

Application settings defaults, extensions and explicit overrides belong to the
project loader. Document its precedence, collection merge/replacement behavior,
schema validation and handling of invalid values. A reasonable new-project
choice is defaults followed by explicit project values and documented environment
overrides. Existing projects retain their own established semantics. The starter
does not implement that precedence or interpret the example files above.

Dependency and configuration flexibility does not silently waive the starter's
required Python engineering standards. Preserve existing-project authorities and
report adoption gaps; for new starter projects retain Python 3.14, the approved
routine checks and the documented XPPython3 host exception. Project-specific
plugin revisions require a reviewed catalog and consistent lock/discovery sources,
as described in [adoption](adoption.md#getting-current-sp-and-gz-skills).

## Keep the baseline current

Use the [adopter baseline policy](baseline-policy.md) for allowed version ranges
and selection rules, independently of the reviewed checkout's exact execution pins.

Generic maintenance workflows belong in gz-skills. Use its discovered
`gzs-update-dependencies` for authorized dependency/tool updates and
`gzs-dependency-risk-audit` for risk assessments. This document supplies project
policy and source locations. The starter supplies no competing maintenance skill
or generic freshness-report command. The pinned gz-skills v0.8.0 maintenance
skill supports freshness-only review and template/plugin source inventory.
Review mode leaves pins and environments unchanged; updates require scoped
authorization. Apply the guidance below as this project's binding, preserving
its approved Python family, retired tools and explicit profile choices over
upstream defaults.

The required baseline rule is **latest stable tooling**, including review of
new stable tool families. An older family is not a freshness exemption. Python's family is 3.14.x normally and 3.12.x for XPPython3-bound
projects. Exact patches record verified execution choices; adopters must refresh
them rather than retain the starter's patch indefinitely. The embedded XPPython3
runtime remains host-controlled; document limitations and validate it separately.
At setup/adoption and scoped
maintenance, verify the latest patch from official sources, test it, and record
an exact runtime pin shared by local execution and CI. For other baseline Python
tools, assess the latest stable upstream release across families under the tool's
versioning scheme; an old range requires an evidenced exception, not a current claim. An installed version, minor-only
selector or old lock does not establish freshness. Family changes require
separate review; compatibility exceptions need evidence and a revisit condition.
See the [Python baseline rule](engineering/python.md#latest-stable-within-the-selected-family).

The current Python pin is 3.14.10, checked October 26, 2026 against the
[official release](https://www.python.org/downloads/release/python-31410/).
`requires-python` describes the allowed 3.14 family; `.python-version` selects
the exact execution patch. The [0.7.0 release receipt](evidence/2026-10-26-0.7.0-release.md)
records the candidate's tool refreshes, retained selections and exceptions.

A minimum supported version, a tested exact pin and the latest available release
are different facts. The current exact tool pins are reproducibility anchors;
they are not established oldest-supported versions or a claim to be latest.
Do not turn them into unbounded `>=` requirements without testing the intended
support range. Adopters may add bounded requirements and retain exact resolutions
in their own lock; shared baseline changes do not automatically migrate them.

At setup/adoption, before each release, scoped tool upgrades and quarterly
on-demand maintenance:

1. Inventory Python, uv, runtime/dev/hygiene packages, CI/hook tool versions, the
   adopted starter revision and pinned SP/SP-BP/gz-skills releases. Check current official release and compatibility
   evidence; do not infer freshness from a copied template or release age alone.
2. Record the checked date, baseline pin, latest release, supported minimum if
   tested, Python/platform risks, evidence links and adopt/defer decision.
   A selected but unverified tool is a gap, not a supported baseline dependency.
3. For an authorized upgrade, update affected declarations, locks, commands and
   guidance together. Plugin bundle changes also update both native catalogs.
   Run the required project checks on the actual pinned interpreter; verify
   changed analyzers separately and retain honest legacy measurements.
4. Review the adopter's diff independently. Preserve additional packages,
   settings, profiles and authorities; keep the previous lock/pins for rollback.
   Record host discovery separately from configuration validation.

This is maintenance guidance, not an automatic updater, scheduled review or
dependency upgrade. The Python policy's [freshness procedure](engineering/python.md#periodic-dependency-freshness-review)
supplies the detailed assessment. No fresh package-release inventory is claimed
by this documentation change. Python 3.14's new concurrency, compression and
template APIs are not needed for this preservation contract; retain the existing
stdlib implementation rather than adding loader or resolver machinery.
Adopters also follow [stack maintenance](adoption.md#maintaining-the-adopted-stack)
for the template and all three independently owned plugins, including deferred
SP-BP.
Use the template's [versioning contract](versioning.md) and changelog when
reviewing a release; keep its version distinct from the adopter app's version
and retain the exact starter SHA.

## What is resilient today

`starter.py configure` previews its managed paths, preserves unrelated host TOML,
and refuses conflicting managed records. It leaves application `pyproject.toml`,
`uv.lock`, `settings.json` and other project files untouched on preview, apply and
repeat adoption. Tests exercise this at the public configure seam, including a
project with many invented dependency declarations and explicit overrides.
They prove file preservation, not resolution or compatibility of those packages.
Adoption reads managed text as UTF-8 and retains existing host TOML line endings;
the regression test also simulates a legacy Windows default encoding.

There is no automatic baseline merge, app settings loader, dependency resolver
integration or adopter migration command. Changed starter-managed files require
reviewed reconciliation; fresh-session skill discovery remains unverified by file
checks. The starter now configures pinned ty and the approved pre-commit checks;
adopters must configure and verify their own enforcement. Other gaps remain in
the [roadmap](../ROADMAP.md#python-engineering-policy-follow-up).
