# Astral adoption acceptance

Use this guide to prove the required [Astral alignment contract](astral-alignment.md)
for the starter and its Python adopters. Adopt and verify every applicable Astral
recommendation. A departure requires a concrete constraint, evidence, owner and
revisit condition. Absence of a feature can justify not-applicable; convenience
or an existing layout cannot justify skipping a required reconciliation.

This is a verification contract recorded in the project's existing planning,
review or handoff location. It adds no lifecycle, agent skill or automatic
migration. The [worked migrations](astral-migrations.md) illustrate three paths;
the [uv review](uv-deep-dive.md) explains the underlying execution boundaries.

## Establish scope before running commands

Record project root/revision and dirty state, reviewed starter version/SHA,
application versus library, distribution/import/command names, supported Python
family and platforms, exact execution pins, workspace root kind and members,
and intended release/deployment products. Identify existing project authorities,
the authorized migration and rollback point. Protect operational data and user
changes. Configuration-only work reports unperformed reconciliation explicitly.

Keep three conclusions distinct: helper configuration, Python baseline acceptance
and fresh-session native skill discovery. `configure`/`status` prove their
documented file contract, not Python conformance or host loading. Do not describe
an unfinished migration as completed adoption.

## Requirement and evidence matrix

Use the row identifiers below in a project-owned record. Every row needs an
actual result or a reasoned applicability decision, not merely a command to run.

| ID | Required acceptance | Authority | Evidence to retain |
| --- | --- | --- | --- |
| A01 | Project identities, scope and rollback are explicit | This guide; adoption/backport guidance | Revision/dirty state, source-to-target mapping, affected public behavior, rollback reference |
| A02 | Runtime packages use `src/`, installed imports, declared backend/entry points | Alignment: Package structure | Layout/config diff; installed import origin and command behavior; no path injection |
| A03 | uv_build for pure Python, or owned backend exception | Alignment: Package structure | Verified build pin, actual backend, demonstrated need and build proof for alternatives |
| A04 | Python metadata and supported tool settings are centralized and effective | Alignment: Configuration and environments | Config inventory/precedence, relevant nonsecret overrides, analyzed file scope and selected settings |
| A05 | Actual managed interpreter matches the approved family/exact execution pin | Python: Runtime and version-aware decisions | Interpreter version, implementation, base executable, architecture/variant; pin/metadata/Ruff/ty/CI reconciliation |
| A06 | Latest stable tooling across families and the approved Python family's latest patch were checked at setup/adoption/release/maintenance | Baseline policy; Python: Latest stable within the selected family | Dated official release evidence, exact chosen versions, compatibility exceptions; no freshness inference from a lock |
| A07 | Lock matches declarations and exact selected environments are reproducible | Alignment; uv locking/syncing guidance | Lock consistency, locked exact sync, selected groups/extras/member scope and environment path |
| A08 | Routine commands use the declared tools and targets | Alignment: Checks and governance | Executable provenance and versions, reviewed Ruff selection, ty target, unittest results; no ad hoc overlay substituting for baseline proof |
| A09 | Local, installed hooks and CI enforce the reviewed routine contract | Alignment: Checks and governance | Command/scope comparison, observed hook installation and run, exact-commit CI result/platform; distinguish missing/unknown |
| A10 | Original dependency intent and sources survive migration | Project configuration contract; uv dependency guidance | Runtime/extras/groups distinction, direct/transitive constraints, markers, source map and lock diff; wheel Requires-Dist |
| A11 | Release artifacts build independently of development sources | Alignment; uv publishing guidance | `uv build --no-sources`, recorded build inputs, sdist-to-wheel path, wheel/sdist inventory and resource/metadata checks |
| A12 | Clean installed artifacts preserve public behavior | Alignment: Package structure | Separate temporary environment outside checkout, intended runtime dependencies only, import/CLI/resource tests; no editable source/PYTHONPATH shortcut |
| A13 | Library typing/layout/support claims are verified when applicable | Alignment; Python policy | Wheel typing marker/stubs/namespace inventory, installed API checks, supported dependency-bound evidence or owned exception |
| A14 | Workspaces have explicit edges, root kind and selected-member proof | Alignment: Workspaces | Membership/dependency/source mapping, root/member selections, shared checks plus independent built-member installation |
| A15 | Private/special sources preserve identity and authentication boundaries when applicable | Project configuration contract; uv index/auth guidance | Named source/index bindings, index strategy/default decisions, redacted authentication/trust proof; no committed secrets |
| A16 | Deployment/dynamic/native builds have applicable verification | Alignment; uv build/container guidance | Non-editable deployment behavior, target runtime/ABI, build isolation/input/cache-key decisions and actual product evidence |
| A17 | Exports and standalone script/tool environments have explicit consumers/contracts | uv project/export/script/tool guidance | Consumer, generation command/groups, separate lock/pins where used, artifact test; uv.lock remains project authority |
| A18 | Exceptions and wider Python engineering obligations remain visible | Python policy; alignment; existing project authority | Owned evidence/revisit, on-demand tooling gaps, code-currency decisions and separate host runtime evidence |

This matrix binds the existing policies together; it does not replace their full
content. For example, A18 does not waive required on-demand selections simply
because no deeper analyzer was needed for one migration. An outstanding tool
compatibility proof stays outstanding.

## Verify effective configuration and execution

Inventory root/member/ancestor configuration, applicable user/system settings,
CI environment and wrapper commands. Read relevant nonsecret values; never
attach whole environment dumps, private credential stores or authentication
URLs. Record intentionally different contexts rather than flattening them.

- uv: same-directory `uv.toml` overrides pyproject uv settings; project/user/
  system settings merge, with environment and then CLI overrides. Persistent
  workspace settings are root-scoped; member dependency/source metadata has
  its own documented behavior. Inspect packaging/managed flags, Python request,
  environment path, lock/sync bypasses, group/extras selection, sources and
  preview controls. `--no-config` can discard the intended baseline.
- Ruff: inspect the nearest config for representative files in every scope,
  explicit inheritance, same-directory competing configs, CLI overrides,
  exclusions and actual file discovery. One file's settings do not prove all
  paths use the same rules.
- ty: inspect discovered project/user configuration, merged settings and arrays,
  competing `ty.toml`, environment and CLI overrides, exclusions and import
  environment. Verbose output is supporting evidence, not a complete settings
  dump. `--config-file` takes a ty-format file, not pyproject.

See official [uv configuration](https://docs.astral.sh/uv/concepts/configuration-files/),
[Ruff configuration](https://docs.astral.sh/ruff/configuration/) and
[ty configuration](https://docs.astral.sh/ty/configuration/).

From the target root, adapt the representative source path and documented group
selection before executing:

```text
uv --version
uv lock --check
uv sync --locked --all-groups
uv run --locked --managed-python python --version
uv run --locked python -c "import platform,sys; print(sys.executable); print(sys.base_prefix); print(platform.python_implementation(), platform.machine())"
uv run --locked python -c "import shutil; print(shutil.which('ruff')); print(shutil.which('ty'))"
uv run --locked ruff --version
uv run --locked ty --version
uv run --locked ruff check --show-files .
uv run --locked ruff check --show-settings src/example_app/__init__.py
uv run --locked ty check -vv
```

All-group sync is appropriate only when the reviewed groups are compatible and
intended. With declared conflicting groups, verify each supported selection in
separate environments instead. Exact sync removes extraneous packages from its
target; first verify that target is the intended project-owned environment.
Do not point it at a shared/system environment. The selected tools' executable
paths must resolve to the intended environment, not an unrelated PATH fallback.

Run the project's four routine checks using the reviewed scope. For this starter
they are Ruff check/format, ty and unittest through pre-commit. A locked run
does not remove extras by default; `--with`, external commands, `--active`,
inline-metadata scripts, `uvx` and `uv pip` can change the execution contract.
Use `run --exact` for a selected exact proof when appropriate, or exact sync
before locked runs. Neither proves runtime dependency completeness in a broad
development environment. See [uv locking/syncing](https://docs.astral.sh/uv/concepts/projects/sync/).

## Verify artifacts and applicable variants

Build using `uv build --no-sources` before accepting a distribution/release.
Keep the default sdist-to-wheel path. Inspect both inventories and metadata,
including package resources, licenses, typing data and runtime dependencies.
The command checks development build-source independence; it does not establish
that unpublished workspace runtime dependencies are available to consumers.
Supply/install those distributions through the intended delivery mechanism.
Isolated build dependencies are separate from the project runtime lock: record
exact backend/other build inputs and any constraints or hashes needed for the
project. Retain isolation; prefer evidenced build-dependency augmentation to a
global bypass. See [publishing](https://docs.astral.sh/uv/guides/package/).

Install the built wheel into a fresh temporary environment outside the checkout.
Use that environment's interpreter/CLI directly, clear source-path shortcuts,
and verify import origins plus representative public behavior and resources.
For dependencies, use the reviewed runtime delivery selection; `--no-deps` is
valid only when dependencies are absent or separately installed and evidenced.
Do not treat a no-deps smoke check as general dependency resolution proof.

| Trigger | Required reconciliation/evidence |
| --- | --- |
| Typed library | Include and inspect `py.typed`; test installed public API and the supported consumer typing surface. Pure stub packages use their documented stub layout instead of invented runtime modules. |
| Intentional namespace | Use documented backend namespace configuration and wheel/import checks. Do not add `__init__.py` to a shared namespace parent just to match an ordinary-package example. |
| Workspace | Identify packaged/project root versus non-project coordinator; select `--package`/`--all-packages` explicitly. A root without `[project]` installed all members by default in the pinned Windows proof. Verify each built member with only declared runtime dependencies, then the combined system. |
| Incompatible environments/families | Use independent projects/environments and explicit dependency boundaries; a shared lock cannot make conflicting requirements compatible. |
| Published dependency ranges | Exercise claimed lower bounds separately from current exact development pins, or record an evidenced limitation. Keep routine tool pins unchanged; run the project's unittest behavior against the intended runtime dependency selection. |
| Private index, URL or Git dependency | Record source identity, named explicit-index/default/fallback decisions and immutable revision where required. Review unsafe index strategies; keep credentials outside committed metadata and evidence. |
| Container/standalone/host deployment | Verify the delivered product, compatible interpreter/ABI and non-editable runtime where applicable. Exclude host `.venv` from images. Pin build/runtime inputs; test embedded hosts separately. |
| Native/dynamic build | Document alternative backend, isolated build inputs and external compiler/ABI needs; configure cache keys for real external inputs, not indiscriminate cache purges. |
| Export or standalone script/tool | State consumer, selected groups/extras/platforms and generation path. Keep generated exports subordinate to uv.lock; separately lock/pin intentional PEP 723/tool environments. |
| Preview feature | Record concrete benefit, exact tested version, compatibility risk and adopt/defer decision. Do not blanket-enable preview or substitute experimental audits for selected tools. |

The migration examples cover ordinary pure Python, an inline typed library and
a compatible workspace. A project triggering other rows must supply its own
evidence; those examples do not certify private indexes, native builds or hosts.

## Record the result and close reconciliation

Copy this record into the existing project authority, expanding one row for each
matrix item and project-specific requirement:

```text
Project/revision/dirty state:
Reviewed starter version/full SHA and policy revision:
Product kind, platforms, root/member identities:
Verified Python/tool selections and checked date:
Configuration result / Python baseline result / native host discovery result:

ID | Applicability/reason | Command and scope | Observed result | Evidence | Open work/exception
A01 | ... | ... | PASS / FAIL / UNKNOWN / N/A / EXCEPTION | ... | ...

Exception: constraint, affected scope, evidence, owner, accepted-by, revisit condition.
Rollback: source/configuration/lock reference, preserved data, restore and verify steps.
```

PASS needs observed evidence. FAIL is a demonstrated unmet requirement; UNKNOWN
is unperformed or inconclusive verification; N/A needs a triggering-condition
reason. EXCEPTION means a project-authorized, evidenced departure with an owner
and revisit condition, and must be visible in the overall conclusion.

Do not claim complete baseline acceptance with required FAIL/UNKNOWN rows or
unaccepted exceptions. Report conditional acceptance explicitly when exceptions
are accepted. Configuration may be complete while Python adoption or native
discovery remains incomplete. Reconcile changed policy/fragment content through
a reviewed adopter diff; the helper's preservation refusal is not a force-update
mechanism. Retain rollback evidence and use existing project ownership.
