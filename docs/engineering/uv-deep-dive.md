# uv documentation deep dive: maximum Astral alignment

Implementation update: the user's subsequent authorization is implemented in the
[acceptance contract](astral-acceptance.md), [executed migrations](astral-migrations.md)
and [starter receipt](../evidence/2026-10-18-astral-acceptance.md). The review below
retains its original assessment and research boundary as historical evidence.

Reviewed October 18, 2026, starting from [uv's official documentation](https://docs.astral.sh/uv/).
The user specifically requested careful attention to Projects and maximum
Astral compliance. This review precedes implementation selection and qualifies
the earlier [bounded proposal](astral-guidance-evaluation.md).

The starter has the right core structure. Its guidance is too compressed to
establish maximum alignment across real project operations. The largest gaps
concern effective execution, project/workspace selection, distribution metadata,
and the distinction between development and release environments. An acceptance
checklist remains necessary, but its content must expand beyond checking that
the expected files and tools exist.

## Scope and evidence

Read the nine Projects concept pages: structure, creation, dependencies, running,
locking/syncing, configuration, builds, exports and workspaces. Followed their
relevant links into Python selection, persistent configuration, resolution,
indexes, backend behavior, tools/scripts, authentication, caching, migration,
CI/container/pre-commit integration, preview and support/versioning policies.
The settings/environment references were consulted for selected controls; this
is not a claim to have verified every reference option or every integration.

Documentation observations below describe the live site on the review date.
It is not versioned documentation for every historical uv release. Separate
local experiments used **uv 0.13.1, managed CPython 3.14.8, Windows x86_64**.

The repository baseline was commit `1c107649154b9e62f87be6416f929b8c76234151`
with the preceding evaluation documentation still uncommitted. Research changes
are likewise uncommitted; no new remote CI run is claimed.

Retained evidence:

- [Execution/configuration receipt](../evidence/2026-10-18-uv-behavior-probe.json):
  twenty command records covering lock behavior, extra packages, overlays,
  external executables, inline scripts and configuration precedence.
- [Projects/workspace receipt](../evidence/2026-10-18-uv-projects-probe.json):
  root/member selection, an intentionally undeclared import, development sources,
  published dependency metadata, editable source changes and virtual packages.

Fixtures were invented, temporary and cleaned up. Child uv operations used
offline mode and existing cached/bundled build support. Only disposable
environments were deliberately contaminated or reconfigured. No adopter,
dependency pin, user configuration, plugin, hook or CI contract was changed.
The receipts include setup data, arguments, observed results and negative
controls; they are research evidence, not a generic maintenance utility.

## What maximum alignment means here

Treat every applicable Astral recommendation as the default to adopt and prove.
Record a concrete reason, evidence, owner and revisit condition for departures.
Mark an item not applicable only when the project lacks its triggering need.
Supported alternatives and experimental features need explicit treatment; merely
enabling more flags cannot establish conformance.

Preserve the user's independent decisions: Python 3.14 family and XPPython3
exception, unittest, the four routine hooks, on-demand deeper analysis, separate
product/template/plugin versions, and a new PRD for every major release. Those
are starter policy, not instructions supplied by uv. Recommendations below are
proposed reconciliations, not newly enacted obligations.

## Projects: the distinctions our guidance must preserve

### 1. A project, package, environment and distribution are different things

`pyproject.toml` identifies a project; uv manages its environment and lock.
Packaging determines whether the project's own imports and entry points are
installed. A successful dependency sync alone is insufficient evidence of
installed application behavior. `uv.lock` is uv's managed resolution record,
not a snapshot of arbitrary source contents. [Structure and files](https://docs.astral.sh/uv/concepts/projects/layout/).

For this starter, keep the declared backend, installed `src/` package and CLI.
Acceptance should identify the distribution name, import name, entry points,
environment path, lock and source revision separately. A reviewer must be able
to tell which of those identities each check actually verified.

### 2. Current creation defaults support our direction

Current uv initializes packaged applications and libraries under `src/`, with
uv_build by default; application defaults changed in 0.12. Library templates
include `py.typed`. uv also supports unpackaged and bare initialization.
[Creating projects](https://docs.astral.sh/uv/concepts/projects/init/).

Keep our stronger packaged-project baseline. Migration examples must inspect
the generated output of the pinned uv version instead of assuming older
`main.py` tutorials or copying their Python/tool selections. Initialization is
a starting point; it does not establish this starter's full engineering policy.

### 3. Separate dependency intent from development source selection

Published runtime requirements and extras belong in standard project metadata;
development groups are local. `tool.uv.sources` supplies uv-specific development
sources and does not replace published requirements. Directory path dependencies
are not editable by default; workspace dependencies normally are. All groups
participate in resolution, and incompatible selections require deliberate
conflict handling. [Managing dependencies](https://docs.astral.sh/uv/concepts/projects/dependencies/).

Our examples should show the resulting wheel's `Requires-Dist`, not stop at
a successful local workspace import. In the probe, the application wheel
declared its core dependency; an undeclared hidden import stayed absent from
metadata even though it worked in a broad development environment. That is a
real acceptance boundary, not a resolver defect.

### 4. Package installation can be explicitly disabled

`tool.uv.package = false` can prevent project installation despite a declared
backend. Project operations normally ignore an unrelated active virtual
environment unless asked to use it; `UV_PROJECT_ENVIRONMENT` can redirect the
target environment. Build isolation is separately configurable.
[Configuring projects](https://docs.astral.sh/uv/concepts/projects/config/).

The probe confirmed that a backend declaration did not defeat `package=false`.
Acceptance must inspect effective packaging/environment controls and prove
installed imports. Do not automatically reject a justified workspace coordinator
that owns no runtime package; distinguish it from a runtime member silently
skipping packaging. Our current blanket member/package wording needs that
qualification before a worked workspace guide is written.

### 5. A locked run can execute outside the expected package set

uv can launch an executable outside the project environment. Per-invocation
`--with` dependencies can overlay project requirements, while inline-metadata
scripts have separate execution semantics.
[Running commands](https://docs.astral.sh/uv/concepts/projects/run/).

The probe ran an invented `.cmd` from an extra PATH directory and added a local
wheel through `--with`, both with `--locked`. A passing locked command therefore
does not establish that its executable came from the declared dev group or
that its effective dependencies matched the project environment alone.

For acceptance, record executable provenance/version and group selection. Treat
ad hoc overlays as separately scoped experiments, not routine baseline proof.
Keep regular engineering utilities in the declared project environment unless
a separately managed script/tool contract is intentional and verified.

### 6. Lock validity and environment exactness need separate evidence

`--locked` checks consistency without rewriting the lock; `--frozen` skips the
freshness check. Sync is exact by default, whereas run normally retains extra
packages; `run --exact` removes them. Neither lock consistency nor a successful
sync proves current upstream releases. Group-only selections can omit the
project itself, and partial installation flags intentionally omit packages.
[Locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/).

The probe confirmed undeclared installed packages survived a locked run and
were removed by exact run/sync. Stale project metadata blocked a locked run;
the frozen control still executed. The starter's initial locked all-group sync
already supplies exact cleanup in its full gate. Document that role rather
than claiming each subsequent locked run independently supplies it.

An exact development environment still contains legitimately selected dev
dependencies. It cannot alone prove that runtime imports declare every needed
dependency. Keep separate clean installed-artifact verification.

### 7. Workspaces require selection and isolation discipline

Workspace members share a lock/resolution. Membership does not declare runtime
dependency edges. Root source declarations can be overridden by member source
declarations, including marker cases where fallback may be surprising. Shared
environments can mask undeclared imports; incompatible environment needs warrant
separate projects. [Using workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/).

The documentation's ordinary root-selection statement needs qualification in
our guidance. On pinned uv, a **packaged project root** selected itself and its
dependencies by default; a **root without `[project]`** installed all members by
default. The latter is an observed local result, not a universal claim about
other versions. Record root kind and explicit package selection in examples.

The negative control deliberately imported an undeclared hidden member. It
passed after all-member sync and failed under selected-member exact execution.
That failure was expected. Independent built-member installation remains the
stronger distribution proof; selected-member execution complements it.

### 8. Build proof must cover source independence and metadata

Plain `uv build` creates the sdist and builds its wheel from that sdist. Asking
explicitly for both source and wheel builds changes that relationship. Build
dependency constraints/hashes are separate controls; a project environment lock
does not by itself describe every isolated build input.
[Building distributions](https://docs.astral.sh/uv/concepts/projects/build/).

The starter already exercises the sdist-to-wheel path and installs its wheel
outside the checkout. Preserve this evidence. Add an explicit decision about
build inputs for alternative backends and dynamic build requirements instead
of describing every uv build as project-lock-controlled.

Astral specifically recommends `uv build --no-sources` before publishing to
check independence from development build sources.
[Building and publishing packages](https://docs.astral.sh/uv/guides/package/).
Under maximum alignment, this belongs in the release/artifact acceptance work,
not a vaguely optional advanced appendix. The probe executed it successfully
for an invented workspace application. Building alone still did not detect its
undeclared import; inspect metadata and exercise installed behavior as well.

This build check concerns build dependencies. It does not prove that an
unpublished workspace runtime dependency can be resolved by a consumer. The
release path must also supply and install the declared runtime distributions.

Retain isolated builds by default. For a demonstrated dependency-build problem,
Astral recommends augmenting missing build dependencies before disabling
isolation. Record package-specific exceptions and verify build/runtime ABI
compatibility when relevant; do not adopt global isolation bypasses as a
generic fix. [Build isolation guidance](https://docs.astral.sh/uv/concepts/projects/config/#build-isolation).

### 9. Backend layout and resource rules need explicit checks

uv_build supports pure Python, namespace packages, stub packages and configured
resource inclusion. Namespace parents intentionally differ from ordinary
`__init__.py` packages. Source inclusion does not automatically mean wheel
inclusion; exclusions and package/data placement matter. Compiled extensions
need another backend. [Build backend](https://docs.astral.sh/uv/concepts/build-backend/).

Keep uv_build as our default and verify actual wheel/sdist contents. Add
namespace/stub applicability to the library path without prescribing empty
`__init__.py` files that break intended namespaces. The starter's resource-copy
checks are useful concrete evidence, but their implementation is helper-specific.

### 10. Exports are interoperability outputs

uv supports requirements, standardized pylock and CycloneDX exports. Its project
lock remains authoritative; Astral discourages maintaining requirements files
alongside it without an integration need. CycloneDX export is preview on the
reviewed site. [Exporting a lockfile](https://docs.astral.sh/uv/concepts/projects/export/).

For adopters, require a documented consumer and generation path for any export,
including selected extras/groups and platform implications. Do not create a
second manually maintained dependency authority or make an SBOM export a new
routine gate merely because the feature exists.

## Supporting concepts that affect Projects

### Effective configuration is a uv issue too

uv merges project/user/system settings, but same-directory `uv.toml` wins over
pyproject uv settings. Arrays merge; environment settings override persistent
configuration and CLI overrides both. Workspace persistent configuration is
root-scoped. Explicit config-file input uses uv-format configuration; disabling
configuration discovery also removes intended project settings.
[Configuration files](https://docs.astral.sh/uv/concepts/configuration-files/).

The probe's conflicting `required-version` in `uv.toml` took precedence and
failed as expected. Extend the proposed effective-configuration work beyond
Ruff/ty. Do not recommend blanket `--no-config` as compliance hardening: it can
discard the project's reviewed choices, including its managed-Python preference.

Root-scoped uv settings do not erase the documented member dependency metadata
and source-override behavior. Teach those categories separately.

Record only relevant nonsecret effective values and configuration locations.
Inspect overrides such as `UV_PYTHON`, `UV_PROJECT_ENVIRONMENT`, `UV_NO_SYNC`,
`UV_FROZEN`, `UV_NO_PROJECT`, group selectors and preview controls before claiming
execution parity. [Environment reference](https://docs.astral.sh/uv/reference/environment/).
There is no justification to dump the entire user environment into evidence.

### Python reproducibility has more than one selector

Managed Python means installed by uv, not necessarily the newest available
patch. uv's downloadable interpreter catalog is tied to the uv release.
Exact patch requests and minor-version requests have different upgrade behavior;
Python implementation, architecture and free-threaded/debug variants also matter.
[Python versions](https://docs.astral.sh/uv/concepts/python-versions/).

Keep official freshness verification and exact pins. Record the interpreter that
actually executed, implementation/variant and architecture where relevant. If
the approved uv release cannot supply a required new patch, review that tool
constraint explicitly rather than claiming its download catalog proves upstream
freshness or quietly selecting another runtime. No upgrade was performed here.

### Resolution is broader than one successful installation

Universal resolution can select different versions for markers. Lowest-bound
testing is a separate recommendation for published libraries. Constraints narrow
requirements; overrides replace them. `environments` limits resolution, whereas
`required-environments` checks wheel coverage for dependencies lacking sdists;
neither executes application tests. uv ignores dependency `requires-python`
upper bounds during resolution; do not treat that metadata as an enforced host
compatibility check. [Resolution](https://docs.astral.sh/uv/concepts/resolution/).

Our approved Python family is unchanged. The library migration needs an explicit
decision and evidence for claimed dependency/support bounds; the starter has no
runtime dependencies, so that is not a missing helper runtime test. Review
platform constraints, override decisions, prerelease policy and release cutoffs
where relevant. A successful resolver result cannot certify the host or ABI.

### Index selection is part of dependency identity

uv's default first-index behavior protects source selection rather than pooling
all indexes like pip's closest alternative. Named explicit indexes can limit
which packages use them; choosing a replacement default changes PyPI fallback.
Named source bindings need project-owned definitions. Authentication and index
selection are distinct. [Package indexes](https://docs.astral.sh/uv/concepts/indexes/).

For private/specialized-source adopters, require an explicit index/source map
and review any unsafe strategy. Do not translate a pip extra-index configuration
mechanically or infer that a version number uniquely identifies its source.
Ordinary public-index projects can record their simpler case explicitly.

### Credentials and TLS need the documented integration path

uv has HTTP credential lookup and storage behavior distinct from project files;
its ordinary credential store is plaintext, and native secure storage is preview
on the reviewed site. Direct URL credentials have persistence caveats.
[HTTP credentials](https://docs.astral.sh/uv/concepts/authentication/http/).
Corporate trust roots have supported system/custom certificate mechanisms.
[TLS certificates](https://docs.astral.sh/uv/concepts/authentication/certificates/).

Propose secure references and redacted verification for applicable projects.
Avoid embedding secrets in committed sources or bypassing verification to make
a private installation work. No credentials, trust settings or registries were
accessed or changed during the experiments.

### Caching does not replace build-input accounting

uv's cache keys differ for registry, Git and local inputs. Dynamic metadata or
external build inputs may need explicit cache keys; custom keys replace defaults.
Refresh and reinstall address different states, and cache contents should not
be edited manually. [Caching](https://docs.astral.sh/uv/concepts/cache/).

The probe changed editable source behavior while the lock hash stayed identical.
Maximum reproducibility therefore needs source revision, dirty state and build
input evidence as well as a lock. Avoid indiscriminate cache purges as a default
migration step; use a targeted, demonstrated reason.

### Scripts, project tools and user tools have different contracts

PEP 723 scripts ignore project dependencies and can have adjacent script lock
files. [Running scripts](https://docs.astral.sh/uv/guides/scripts/).
`uvx`/`uv tool` use isolated tool environments and have their own version/cache
selection. [Tools](https://docs.astral.sh/uv/concepts/tools/).
Tool commands ignore project-local uv configuration and read user/system
configuration instead. [Tool configuration scope](https://docs.astral.sh/uv/concepts/configuration-files/).
The pip interface targets environments explicitly or by its own discovery rules.
[Using environments](https://docs.astral.sh/uv/pip/environments/).

The script probe failed without its script lock, ran separately once locked,
and used the project package when invoked through `uv run ... python inline.py`.
That is why command spelling matters. Keep baseline checks in project dev
groups. Use separately pinned script/tool contracts only when their isolation
serves a real need; do not substitute unpinned `uvx` checks for locked project
checks. Preserve the verifier's explicit clean-environment wheel installation.

## Migration, CI and deployment

Astral's migration guide distinguishes original dependency intent from compiled
requirements, imports constraints to preserve reviewed versions, and converts
development requirements into groups. [pip-to-project migration](https://docs.astral.sh/uv/guides/migration/pip-to-project/).
uv intentionally differs from pip in configuration and other behavior; pip's
configuration/environment settings do not automatically configure uv.
[pip compatibility](https://docs.astral.sh/uv/pip/compatibility/).

Our worked migrations should preserve original direct/transitive distinctions,
platform markers, source intent and rollback evidence. A freeze of a dirty
environment is not a substitute for reviewing dependency intent. Avoid using a
migration as an implicit dependency upgrade.

The official CI guide recommends setup-uv, explicit uv pinning and locked
installation; it also shows how CI Python selection can override local pins.
[GitHub Actions](https://docs.astral.sh/uv/guides/integration/github/).
Our immutable actions, explicit versions and common gate are strong. Acceptance
should demonstrate actual interpreter and command parity, with declared platform
scope. Support by uv is separate from tested support by our application.
[Platform support](https://docs.astral.sh/uv/reference/policies/platforms/),
[Python support](https://docs.astral.sh/uv/reference/policies/python/).

Astral offers lock/export/compile hooks.
[Pre-commit integration](https://docs.astral.sh/uv/guides/integration/pre-commit/).
These are available integrations, not a requirement to replace our approved
four-hook gate. Keep the user's hook boundary and existing locked failure
behavior. Evaluate any future change separately rather than adding a hook
as an unreviewed interpretation of maximum alignment.

For deployable containers, Astral discusses pinned uv images/digests, excluding
host `.venv`, cache mounts, layered installs, compatible runtime environments
and non-editable delivery. [Docker integration](https://docs.astral.sh/uv/guides/integration/docker/).
Adopt the applicable practices when the project has a deployment target. A
development all-group environment is not the production acceptance target.
Require an actual deployment check when applicable; Docker itself is not a
universal starter dependency. The starter currently has no container deployment.

`uv version` and `uv publish` provide mechanisms, not release authorization or
this project's source-of-truth policy. Keep `bundle.json` authoritative and
mirror package/lock versions through the existing release procedure. A registry
upload does not follow from a build or Git sync.

## Preview and version-policy decisions

uv documents its own versioning scheme: minor changes may break compatibility;
patches include enhancements as well as fixes.
[uv versioning](https://docs.astral.sh/uv/reference/policies/versioning/).
Keep the approved 0.13.x family and exact tested execution selection until
authorized maintenance. Do not import uv's release scheme into this template's
separate SemVer/PRD rules.

Preview status requires checking feature by feature. The reviewed docs label
audit, on-sync malware checks, native authentication, some build-hash controls,
centralized environments, pylock and SBOM capabilities as preview or otherwise
experimental. Supported invocation without a feature flag does not necessarily
mean stable. [Preview features](https://docs.astral.sh/uv/concepts/preview/).
Evaluate useful features, but record evidence and adoption/defer decisions;
blanket preview activation is not the route to maximum documented conformance.
Retain selected pip-audit and on-demand boundaries; this review authorizes no
replacement audit tool or new automatic check.

## What changes in our assessment

| Priority | Repository gap | Recommended reconciliation |
| --- | --- | --- |
| First | Effective configuration proposal names Ruff/ty but barely covers uv | Include uv discovery, overrides, runtime/executable provenance, environment path and group selection |
| First | Locked execution is required but its limits are underexplained | Distinguish lock validity, exact sync, development dependencies, overlays, separate scripts and runtime artifact proof |
| First | Workspace default selection is stated too generally | Specify root kind and package selection; demonstrate shared-environment negative controls and isolated member artifacts |
| First | Presence of backend/layout can be mistaken for installation proof | Check effective packaging controls and installed imports/entry points; explain coordinator roots |
| First | Build/deployment guidance was ranked broadly as advanced | Elevate source-independent release builds, declared distribution metadata and clean installed behavior into the core acceptance work |
| Next | Library/project variants lack complete examples | Cover typing markers, namespaces/stubs where needed, support-bound evidence and workspace publication paths |
| Next | Migration mapping omits some dependency/source semantics | Preserve direct intent, transitive constraints, markers, source selection and exact rollback state |
| Next | Private-source/deployment/dynamic-build decisions are scattered | Add triggered sections with concrete applicability and evidence; require a reason for departures from recommendations |
| Alongside | Stale Ruff-policy sentence and incomplete acceptance record | Correct prose during implementation and trace every applicable recommendation to observed proof |

The first group belongs in the acceptance contract and worked application path,
not an optional appendix. Later rows are triggered by project capabilities;
they require an explicit decision instead of silent omission. This is the
stronger interpretation required by the user's maximum-alignment direction.

## Next implementation boundary

Revise the earlier proposal around these findings before implementing it. The
acceptance record should cover project kind, effective configuration, source and
metadata identity, runtime/tool provenance, lock consistency, selected exact
environments, installed behavior, workspace isolation and applicable release/
deployment practices. Each row needs source authority, expected result, observed
evidence, applicability and any owned exception/revisit condition.

Then execute the invented application, typed-library and workspace migration
paths and retain receipts. These negative-control fixtures are not complete
worked migration examples. No new conformance CLI, generic maintenance reporter,
adopter pilot, plugin policy, hook or CI gate is implied. Shared workflows remain
upstream-owned; project operational behavior remains adopter-owned.

Python 3.14 opportunity decision: the review benefits from executing the pinned
runtime and testing real uv semantics. No new concurrency, annotation, template
or compression API is needed in shipped code; defer additional machinery.
No version bump, PRD, release or Git synchronization is selected by this review.

## Verification of this review unit

The required locked all-group sync, four routine pre-commit hooks, bundle/both
catalog validation, sdist-to-wheel build and isolated installed CLI/resource
verification passed after the research documents and receipts were written.
Local Markdown link targets, JSON parsing and `git diff --check` also passed.
These checks validate the research save point; the proposed adopter acceptance
procedure and complete migration examples remain pending implementation.
