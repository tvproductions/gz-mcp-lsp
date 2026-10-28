# Astral alignment contract

Maximal conformance with Astral's documented project, packaging and Python
tooling practices is required for this starter and its Python adopters. This is
starter-owned engineering policy, checked against official documentation on
October 18, 2026. Astral does not prescribe this repository's governance model,
unittest choice, release authority or domain architecture; those remain governed
by the project's existing authorities. Recheck the official sources during scoped
maintenance and record changes in project decisions.

Adopt and verify every applicable documented Astral recommendation. Departures
need a concrete constraint, evidence, an owner and a revisit condition; supported
alternatives and preview features require an explicit applicability/decision
record. Complete the [acceptance contract](astral-acceptance.md), using the
[worked migrations](astral-migrations.md). File configuration alone is not
acceptance. Record results in existing project authorities, without adding a
parallel lifecycle or automatically enabling more tools/features.

## Package structure

New applications and libraries use `src/<import_package>/`, ordinary-package `__init__.py`, a
declared build backend and a separate `tests/` directory. CLI applications expose
commands in `[project.scripts]`. Typed libraries include `py.typed` and verify
that the built wheel contains it. Use `uv init --app` or `uv init --lib` with the
project's verified Python selection. Check the installed uv version's generated
files: defaults can change. Current uv documentation describes packaged `src/`
applications by default since uv 0.12; earlier application defaults differ.
See [creating projects](https://docs.astral.sh/uv/concepts/projects/init/).

Initialization depends on existing metadata, not whether the product is called
greenfield or brownfield. When creating a new ordinary Python project without
`pyproject.toml`, use `uv init --app --package --build-backend uv` or
`uv init --lib --build-backend uv`, with the verified exact Python selection.
Inspect workspace discovery before running init; do not accidentally enroll a
standalone project in a parent workspace. Existing code without pyproject may
use init after inventory, but generated scaffolding does not migrate that code.
If pyproject already exists, including a tool-only file or one copied from this
template, preserve and reconcile it directly. Do not delete it to rerun init.
uv refuses init in that case. Creation commands do not replace acceptance proof.

Intentional namespace parents and stub-only distributions follow uv_build's
documented namespace/stub layout, verified in built artifacts and installed
consumers. Do not add namespace-parent `__init__.py` files that alter discovery.
Document non-project workspace coordinators separately from runtime packages.

```text
example-project/
├── .python-version
├── pyproject.toml
├── uv.lock
├── README.md
├── src/
│   └── example_project/
│       ├── __init__.py
│       └── py.typed       # typed library
└── tests/                # unittest
```

Select `uv_build` for pure Python. Pin its verified build requirement within an
explicitly selected family; select another supported backend only for a concrete
need such as compiled extensions or required custom build behavior. Verify
wheel/sdist contents, installed imports, commands and package data. Tests must
import the installed package without `sys.path` insertion or ad hoc source-file
loading. Test built artifacts outside the checkout as well as editable installs.
See [uv's build backend](https://docs.astral.sh/uv/concepts/build-backend/).

Before release/artifact acceptance, use `uv build --no-sources` to verify
independence from development build sources, preserving the default sdist-to-wheel
path. Inspect published dependency metadata and provide declared runtime
distributions separately; building does not resolve/test their consumer delivery.
Record build inputs independently of the runtime lock. Retain isolated builds;
prefer evidenced package-specific build-dependency augmentation over disabling
isolation. Alternative/dynamic/native builds need their own input/ABI evidence.
See [publishing guidance](https://docs.astral.sh/uv/guides/package/).

## Configuration and environments

`pyproject.toml` is the authority for Python metadata, supported Python range,
dependencies, build backend, entry points and supported tool configuration.
Use `[project]`, `[build-system]`, `[project.scripts]`, `[dependency-groups]`,
`[tool.uv]`, `[tool.ruff]` and `[tool.ty]` as applicable. Avoid duplicate Ruff,
ty or uv configuration files with conflicting precedence. Use standardized
dependency groups for development tools; `tool.uv.dev-dependencies` is a legacy
field. Runtime requirements, optional features and development groups have
distinct purposes. See [dependency management](https://docs.astral.sh/uv/concepts/projects/dependencies/),
[Ruff configuration](https://docs.astral.sh/ruff/configuration/) and
[ty configuration](https://docs.astral.sh/ty/configuration/).

Commit the uv-generated `uv.lock` and exact `.python-version`; ignore `.venv/`.
Use `uv add`/`uv remove`, `uv lock`, `uv sync` and `uv run` for project management.
Do not manually edit locks or use ad hoc installs to alter the project environment.
Use `--locked` for routine checks and CI so stale declarations fail instead of
silently rewriting the lock. `--frozen` skips freshness validation and cannot
replace that check. A universal lock records resolutions; supported platforms
still require execution evidence. See [project files](https://docs.astral.sh/uv/concepts/projects/layout/)
and [locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/).

Verify effective uv/Ruff/ty configuration and actual executable/interpreter
provenance using the acceptance guide. Competing uv.toml/ruff.toml/ty.toml,
user/system settings, environment and CLI overrides can change the effective
contract. Inspect packaging/environment redirection and bypass flags. Do not
discard reviewed project configuration through blanket isolation/no-config flags.

Locked execution proves lock consistency, not exact environment contents or
executable origin. Exact sync establishes the selected environment; locked runs
normally retain extra packages. Avoid ad hoc `--with` overlays and external PATH
fallbacks in baseline proof. PEP 723 scripts and uv tool environments have separate
selection/locking contracts. Clean installed runtime tests remain necessary even
after exact development sync. Keep runtime, extras and dev/hygiene groups distinct.

The [baseline policy](../baseline-policy.md) still selects Python 3.14.x, with
the evidenced XPPython3 host exception. Align the actual interpreter, exact pin,
`requires-python`, Ruff target, ty target and CI. Pin uv itself for reproducible
resolution; document allowed tool families and verify freshness within them.
Do not adopt preview features solely to maximize the number of enabled options.

This checkout selects uv/uv_build 0.13.x, Ruff 0.17.x, pre-commit 4.x,
complexipy 8.x and Lizard 1.24.x. Exact tested selections live in configuration
and locks. These execution selections do not exempt newer stable tool families
from review under the latest-tooling requirement. Required ty uses its current 0.0.x beta family because no stable
release exists; the starter maintainer owns this exception and must revisit it
at stable release or the next scoped maintenance. See the
[migration receipt](../evidence/2026-10-18-astral-alignment.md).

Centralization applies where a tool supports it. AGENTS.md and project decisions
own governance; native plugin catalogs, pre-commit YAML and CI YAML retain their
native contracts. Application settings may remain in their project-owned file
under the [configuration contract](../project-configuration.md). `bundle.json`
owns template identity and composition; package metadata mirrors its version.
Generated wheel resources must match their authoritative checkout inputs.

## Checks and governance

Ruff check/format, ty and unittest form the routine gate, executed through pinned
uv dependencies by both pre-commit and CI. Select strict Ruff rules deliberately;
review each added family and fix findings rather than selecting every rule or
adding blanket ignores. The starter selects errors/imports, modern Python,
bugbear, simplification and Ruff-specific rules (`E4`, `E7`, `E9`, `F`, `I`,
`UP`, `B`, `SIM`, `RUF`). The formatter controls formatting. C901 and deeper
analysis run at adoption/release acceptance and on demand under the Python
policy, outside the four routine hooks and routine CI. These selections
are our reviewed baseline; Astral does not mandate this exact set. See
[Ruff rule selection](https://docs.astral.sh/ruff/linter/#rule-selection).

Keep one documented verification contract, matching local commands, hooks and CI.
Use Astral's official setup-uv action, reviewed immutable action revisions and an
explicit uv version in GitHub Actions; validate the exact Python pin there.
See [Astral's CI guidance](https://docs.astral.sh/uv/guides/integration/github/).
Record actual results, supported runtime/platform scope, unresolved findings and
compatibility exceptions in existing project authorities. A config file alone
does not establish enforcement; installing hooks locally and observing CI are
separate evidence. No new backlog system, scheduler or upstream skill is added.

## Workspaces

Use uv workspaces when interconnected packages in one repository can share a
resolution and environment. Each runtime member owns its `pyproject.toml` and `src/`
package; a coordinator without `[project]` need not invent a runtime package.
The root declares `[tool.uv.workspace]` membership and owns the shared
lock. Declare member dependencies explicitly, using workspace sources where
appropriate. Verify members independently as installed artifacts as well as
together: a shared environment can hide undeclared dependencies.

For an invented application, the root configuration declares membership:

```toml
[tool.uv.workspace]
members = ["services/api", "services/worker", "packages/shared_utils"]
```

Each directory contains its own `pyproject.toml` and package under `src/`.
If the API depends on the shared package, its member configuration includes:

```toml
[project]
name = "example-api"
version = "0.1.0"
requires-python = ">=3.14,<3.15"
dependencies = ["example-shared-utils"]

[tool.uv.sources]
example-shared-utils = { workspace = true }
```

The shared member's project name is `example-shared-utils`. Membership alone
does not declare dependency edges. Local member dependencies are editable by
default. A shared lock exposes incompatible requirements during resolution;
it cannot make conflicting requirements compatible. Root commands lock the
workspace together. For a project root, `uv sync`/`uv run` select that project
and its dependencies by default; the pinned Windows proof observes all members
selected for a root without `[project]`. Record root kind and use explicit
`--all-packages` to sync all members or `--package example-api` to select one.
Use ordinary single-project uv management when there is only one package.

Shared installed dependencies can conceal missing declarations. Verify each
built member with only its declared runtime distributions, then the combined
system. Selected-member exact execution is a useful additional control; a broad
all-member run alone is insufficient. Root uv settings and member source metadata
have distinct precedence; inspect actual selection and wheel Requires-Dist.

Workspaces are unsuitable when packages require incompatible dependencies,
separate environments or disjoint Python families. Document independent projects
and path dependencies where those boundaries require them. Do not force ordinary
3.14 and host-bound 3.12 code into a single environment. See
[Astral's workspace guidance](https://docs.astral.sh/uv/concepts/projects/workspaces/).

## Existing projects must reconcile

Adopting this baseline commits a project to refactoring nonconforming structure,
configuration and execution paths. Preserving existing files during helper
configuration protects work; it does not grant permanent exemption from policy.
Inventory gaps, map code and authorities, plan the migration and implement it in
bounded, verified changes. Update imports, entry points, resources, docs, tests,
hooks and CI together. Keep public behavior, operational data and rollback
evidence intact. Adoption is incomplete while required reconciliation remains.

An exception needs a demonstrated host or compatibility constraint, affected
scope, evidence, owner and revisit condition. Preference for the old layout is
insufficient. The helper remains preservation-first and does not perform that
refactor automatically. A configuration-only request reports the remaining
migration; authorization to adopt the full baseline includes necessary refactoring
within the agreed project scope.
