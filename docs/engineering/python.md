# Python engineering

The [adopter baseline policy](../baseline-policy.md) owns allowed version ranges
and selection rules. This document supplies their engineering application;
checkout-specific execution pins do not replace that policy.
Runtime discovery belongs in gz-skills. Require its workflows to obey the
project's adopted runtime/engineering policy and report conflicting evidence;
the starter does not duplicate the discovery procedure.

This policy binds the starter's Python standards to project engineering work.
These standards are required for projects started from this starter, not an
optional profile. gzkit is a separate ecosystem. Read the project's AGENTS.md,
configuration and current evidence; preserve unrelated work and operational
contracts. In an existing project, report gaps before proposing a bounded
adoption change. This policy does not authorize a broad application refactor.

## Runtime and version-aware decisions

### Latest stable within the selected family

Baseline tooling must use its latest stable release across tool families. An old
family restriction is not a freshness exemption; review new stable families and
verify compatibility before selecting exact pins. The allowed Python families are **3.14.x for ordinary
projects** and **3.12.x for XPPython3-bound projects**. Ordinary GZ code
deliberately stays one stable minor behind (N-1); this keeps 3.14 while 3.15
is latest. Use the newest verified patch in that family and review a coordinated
family migration when N-1 changes. Tooling still follows latest stable releases. Check official release
information at new-project setup, adoption,
scoped tool upgrades, before every release and quarterly on-demand maintenance. Do not use an older
patch merely because it is installed or satisfies a minor-only selector.

Declare each other baseline tool's approved family in project configuration or
decisions using that tool's actual release/compatibility scheme; do not assume all
tools follow Python's versioning. Apply this rule to uv, Ruff, ty, pre-commit and
the selected on-demand analyzers. Tools not yet installed or verified remain
adoption gaps. Tool family changes require compatibility review; retaining an
older family requires an explicit evidenced, owned and dated exception. Such a
selection is conditional/noncurrent, not strict freshness acceptance.

Verify the latest stable tooling and the latest patch in the approved Python
family, run the relevant checks,
then record exact runtime/tool pins and locks. Use the exact Python patch in
`.python-version` and CI; commands must honor it rather than override it with
`--python 3.14`. Verify the executing interpreter, including existing virtual
environments. A pin makes runs reproducible; it does not prove ongoing freshness.
Refresh during authorized setup/maintenance rather than resolving “latest” on
every invocation. A check-only request reports a stale pin without upgrading it.

If the newest release has a demonstrated compatibility problem or a host imposes
another version, record the selected version, evidence, reason, checked date and
revisit condition. Report that as an exception, not a current baseline claim.
Preserve adopter dependencies and explicit overrides. Keep these preferences
starter-owned; no upstream plugin policy, hooks or schedules follow from them.

As checked October 26, 2026, Python's current 3.14 baseline patch is
[3.14.10](https://www.python.org/downloads/release/python-31410/). Recheck at the next
setup or maintenance event; this date is not an evergreen latest-version claim.

Use uv-managed Python in the selected family. Confirm the actual interpreter through
`uv run --managed-python python --version` (honoring the project's exact pin).
Keep `requires-python`,
`.python-version`, Ruff's `py314` target, ty's Python target, hooks and CI aligned.
Use the same workflow with Python 3.12 for XPPython3-bound code, aligning metadata
and Ruff/ty targets to 3.12. The family is the policy; the exact patch is the
project's verified execution selection, refreshed during authorized maintenance.
The starter's 3.14.10 pin is not a permanent patch requirement for adopters.

XPPython3 embeds its interpreter: its current
[installation documentation](https://xppython3.readthedocs.io/en/latest/usage/installation_plugin.html)
shows Python 3.12, and its
[development documentation](https://xppython3.readthedocs.io/en/latest/development/index.html)
describes the integrated runtime (checked October 11, 2026). Select the latest
stable host-compatible 3.12 patch for standalone development and tests. Inspect
the installed host's actual Python patch and validate plugin behavior there;
a uv environment upgrade does not upgrade XPPython3's embedded interpreter.
If that interpreter trails the latest upstream patch, record the host limitation,
evidence and revisit condition rather than replacing its runtime independently.
Review host updates separately. Historical XPPython3 releases can require another
family; record such a compatibility exception rather than assuming 3.12 works.

## Toolchain ownership

Apply the required [Astral alignment contract](astral-alignment.md): `src/`
packages, declared builds and entry points, centralized Python configuration,
uv-managed locked execution, installed-artifact verification and reviewed
workspace boundaries. Existing adopters must reconcile gaps through refactoring;
preserve behavior and authorities throughout the migration.

| Concern | Required choice |
| --- | --- |
| Standalone Python installation, environments, dependency resolution and locks | uv-managed Python, `pyproject.toml` and project-owned `uv.lock` |
| Lint and format | Astral Ruff, reviewed selection and verified exact tool version |
| Type checking | Astral ty, with the selected Python family reflected in its target |
| Routine tests | Standard-library unittest |
| Routine hooks | Pre-commit running only Ruff check/format, ty and unittest |
| Deeper analysis | Separately pinned on-demand tools; outside hooks and CI gates |

Use Astral tooling for the responsibilities above and keep declarations, locks,
commands and CI aligned. Additional app dependencies remain project-owned and
require a concrete purpose. A host-controlled runtime or tool compatibility
exception needs evidence and a revisit condition. Report required tools that
are not installed/enforced; do not silently substitute another toolchain or
interpret an upstream profile as permission to change project policy.

## Version-aware design

Observe the [code currency requirement](../baseline-policy.md#code-must-follow-its-python-version)
at adoption, runtime-family changes, feature design, code review and scoped
maintenance. Use gz-skills for reusable review/refactoring and SP for feature
work; this document binds their work to the selected Python family. Identify
relevant older patterns and review useful replacements, including stdlib options,
while preserving behavior. Record reasons for deferring concrete improvements.
The [verified Python workflow mapping](../gz-skills-python.md) covers pattern
detection/application, portability, setup, maintenance and debt/change review.
These have narrower scopes than a complete version/idiom audit; report gaps in
the installed workflows explicitly.

Prefer clear current Python idioms and suitable standard-library APIs. Runtime
metadata constrains tools; it does not establish which APIs or idioms are
appropriate. Check the official [Python 3.14 release notes](https://docs.python.org/3.14/whatsnew/3.14.html)
and versioned [library documentation](https://docs.python.org/3.14/library/)
when behavior, syntax, deprecations or removals matter. In migrations, read the
intervening release notes and porting sections as well. Deferred annotation
evaluation and annotation introspection are examples that warrant inspection.
Do not mechanically remove `from __future__ import annotations` or substitute
new syntax without checking its effect on consumers and dependencies. Validate
changed behavior on the pinned runtime; keep modernization within task scope.

For 3.14 design and dependency review, read the [3.14 opportunity guide](python314-opportunities.md)
and assess concrete gains over 3.13: annotation introspection, bounded executor
submission, appropriate stdlib file/compression APIs and structured templates.
Choose adopt/defer/not-applicable with evidence; a successful migration is not
proof that new capabilities were evaluated. Keep this binding starter-owned.
For XPPython3-bound code, consult versioned 3.12 documentation and mark 3.14-only
opportunities unavailable in the host; assess separately scoped standalone code
only against its own declared runtime. A 3.12 pin cannot validate 3.14 syntax/APIs.

## Routine engineering

Use project-locked Ruff check, Ruff format, ty and unittest through uv; never
pytest. Pre-commit runs the routine checks. Inspect available configuration
before giving executable commands; report missing tooling rather than claiming
it is installed. Favor strict linting with a pinned Ruff release and reasoned
exceptions. The reviewed routine selection is E4/E7/E9/F/I/UP/B/SIM/RUF, as
specified by the [alignment contract](astral-alignment.md); do not silently
select ALL, suppress findings or loosen thresholds to pass. Complete the
[Astral acceptance record](astral-acceptance.md), including effective configuration,
exact environment selection, tool provenance and installed-artifact evidence.

Combine TDD, BDD and DDD for consequential behavior: first demonstrate a failure
at a public seam, describe observable outcomes and model domain meanings. Favor
hexagonal architecture: the domain core performs no I/O, defines ports, and
adapters own external effects. Skills orchestrate commands and hold no domain
logic. Use the available SP and gz-skills workflows for their portable design
and engineering disciplines; this policy supplies the Python-specific binding.

Prefer the standard library, including `sqlite3` for SQLite. Pydantic is allowed.
Record any other dependency's purpose and resource cost, and keep it at an
adapter boundary outside the domain core. A skill-local script serves only its
own skill and imports no other skill's scripts. Shared code or a system of
record belongs in a package behind one CLI.

## Adoption/release analysis and on-demand hygiene

Run applicable deeper tools at adoption and before release acceptance, as well
as when requested. Keep them outside the four routine hooks and routine CI;
run an explicit acceptance preflight rather than adding them to every change.
Record actual tool versions, source scope, results, reviewed findings and
applicability. Missing compatibility/installation or unperformed required checks
remain UNKNOWN and block strict acceptance. Legacy failures remain failures;
an accepted exception is conditional, never a clean measurement. Required stale
or unknown freshness and a known incorrect analyzer block strict release/adoption
acceptance; a passing routine gate or maintenance-skill summary cannot override
that result. Resolve and pin development tools
through uv after their Python 3.14 compatibility is established. Use explicit
source/test scopes and invented fixtures; exclude operational data and records.

| Tool | Required interpretation |
| --- | --- |
| Ruff C901 | On-demand cyclomatic ceiling 20 per function; never raise the threshold to pass |
| Cognitive scoring | Required ceiling 15; use the selected gzkit-derived CPython AST approach after qualification. Complexipy is retained locally only for defect reproduction, not acceptance authority. |
| Lizard | Per-function cyclomatic measurements and module/project aggregates for a reviewed C/C/C approximation; do not claim Radon-equivalent scores |
| cohesion | Required adopter on-demand class cohesion analysis; review attribute-sharing scores against class responsibilities and project context |
| Interrogate | Measure docstring presence; review usefulness and correctness separately |
| Vulture | Investigate dead-code candidates and external consumers before deletion |
| Bandit | Review severity, confidence and code context; no blanket suppressions |
| Coverage.py | Measure branch and statement coverage through unittest; report consequential gaps |
| Cosmic Ray | Selected mutation tester; use a unittest test command and bounded mutation scope |
| deptry | Check missing, unused and directly used transitive dependencies; review dynamic imports before changing declarations |
| pip-audit | Audit exact resolved dependencies for known vulnerabilities; record scope, skipped packages and advisory results |
| Import Linter | Verify project-specific forbidden imports and layers, including indirect violations of domain/adapter boundaries |

These selections form the minimum adoption/release and on-demand analysis standard for adopters;
they are not determined by which tools the starter's helper needs. Adopters may
extend this standard with project-specific checks. Required selection does not
prove installation, compatibility or clean results.

### Cognitive analyzer qualification

The user selected gzkit's CPython AST approach as the replacement direction.
Prefer one shared, separately versioned engine used by gzkit and this starter;
do not import the whole gzkit lifecycle or create an unrelated scoring model.
The extraction review must resolve discovery coverage and preserve a documented
metric contract before replacing the acceptance tool.

Complexipy 8.1.0 is installed for evaluation but is not qualified as sole evidence
for cognitive acceptance. The October 24 probe reproduces a blind spot: nine
conditional expressions in keyword argument values score zero, while equivalent
tuple expressions score nine. The compatibility probe now records the failed
canary and exits nonzero. A successful complexipy CLI run cannot override that
failure. Keep the cognitive ceiling of 15; require qualified replacement or
independent evidence before claiming that requirement passes. Historical passing
receipts retain their narrower observed scope, not an evergreen qualification.
See [the defect assessment](../evidence/2026-10-24-complexipy-assessment.md).

The maintainer confirmed that the shared engine is coming from gzkit. The
starter's [consumer qualification boundary](cognitive-integration.md) prepares
fixtures, independent corpus inventory and ceiling enforcement; it supplies no
scoring implementation. The engine remains unselected/uninstalled, so these
tools and their passing regression tests do not establish cognitive acceptance.
Keep the cognitive exception covering 0.7.0 and 0.7.1 until the actual upstream candidate is pinned,
qualified and measured. Do not create a private scorer or an extraction project.

### Adopter class cohesion requirement

Use [cohesion](https://github.com/mschwager/cohesion) as a project-owned,
pinned development tool for on-demand analysis of Python classes. Its documented
metric measures class and instance attribute usage across methods. Review low
scores against actual responsibilities; the score alone does not establish a
design defect. Record the source scope, tool version, class scores and reviewed
findings. For a scope without applicable classes, record not-applicable with a
reason rather than reporting a passing measurement. Do not introduce classes
solely to obtain a score or transplant another project's numeric threshold.

At adoption, select and verify the tool's release family and exact stable version
under the baseline policy, then retain the project-owned pin/lock. Verify its
standalone CLI on the project's selected Python runtime and representative,
invented class fixtures before claiming compatibility. Existing use in another
project is useful evidence, but does not verify a different runtime or scope.
Missing installation or verification remains an adopter gap; compatibility
exceptions require evidence and a revisit condition.

This is a downstream minimum requirement. The starter does not need cohesion
installed to validate its helper and supplies no universal cohesion version,
threshold or Python 3.14 compatibility receipt. Keep it outside hooks and CI
gates, using its standalone CLI without adding Flake8 to the routine toolchain.

### Dependency and import analysis

deptry, pip-audit and Import Linter are selected on-demand tools, not extra pre-commit checks.
Use [deptry's rules](https://deptry.com/rules-violations/) against the actual
project metadata; distinguish runtime dependencies, development tools and
plugin-discovered imports. Findings do not authorize package removal.
Define [Import Linter contracts](https://import-linter.readthedocs.io/en/stable/contract_types/)
from the project's real domain, ports and adapters. Keep reviewed contracts in
project configuration; do not invent a package layout or blanket-ignore debt.

[pip-audit](https://github.com/pypa/pip-audit) works with uv-managed environments
and pinned requirements exports. Keep uv as the resolver: export the existing
lock with `uv export --locked --format requirements.txt --no-emit-project`
to a task-specific temporary file, choosing the intended dependency groups.
Check the export contains exact versions and the full selected transitive set.
Run the project-pinned auditor through uv against that file with `--no-deps`
and `--disable-pip` to avoid a second resolver. Retain exported hashes. Do not
claim direct `uv.lock` support from `pip-audit --locked`; the documented native
lockfile format is `pylock.*.toml`. Record what was audited and what was skipped;
no known advisories is not proof of absence of vulnerabilities. Do not run
`--fix` or upgrade packages as part of a check-only request.

### Complexity policy: Ruff, complexipy and Lizard

Historically, Ruff 0.15.18 and complexipy 8.0.1 passed focused Python 3.14.8
syntax, threshold-boundary and invalid-syntax checks. The current cyclomatic toolchain selects Lizard 1.24.3 and retires both Xenon and
Radon. The saved two-tool receipt is historical; use the new three-tool receipt
for Lizard evidence. Ruff measures cyclomatic branching;
complexipy adds cognitive costs such as nesting. Use cyclomatic 20 and cognitive
15 as ceilings, not targets to write up to. Cyclomatic 20 retains the numeric
upper boundary of Radon's former C rank, but Ruff and Radon counting differs.
Cognitive 15 is a separate metric, not a translation of C/C/C. Use Lizard's
per-function measurements to recover the three-part approach: maximum function
score, each module's mean, and the overall function-weighted mean. Starting
cyclomatic ceilings are 20/20/20, under the reviewed function-based contract for classes, nested functions,
assertions, exclusions and empty modules. These ceilings are implemented by the explicit Lizard checker; see the
[counting contract](ccc-contract.md) before running or adopting it.
When all three use the same population and ceiling, the maximum already bounds
the averages; retain averages for visibility and future stricter policies.
Lizard's counting differs from Radon and Ruff. Compare changed scores and
verdicts explicitly; complexipy's script score is not a module average. This changes only the starter's policy;
do not rewrite other projects' complexity contracts without authorization.

The starter pins Ruff in `dev` and complexipy/Lizard in `hygiene`. Their
purpose is static development analysis. Ruff/complexipy add native wheels;
Lizard adds a Python analyzer. All use uv storage/download resources, with no
application runtime dependencies or service calls. Run from the reviewed starter root, replacing REPORT_DIR with an unused
task-specific temporary directory created first:

```bash
uv run --locked --group hygiene ruff check --select C901 --ignore-noqa src tests tools/engineering
uv run --locked --group hygiene complexipy src tests tools/engineering --cache-dir REPORT_DIR/cache --output-format json --output REPORT_DIR/cognitive.json
```

Run all three even when one reports findings. Use the evaluation probe for
Lizard compatibility scores. Run `tools/engineering/complexity_check.py` explicitly for
the C/C/C gate using the contract command and source scope. In an adopting project, select
its explicit source and invented-test paths and use its reviewed tool pins.
Do not add C901 to routine Ruff selection, complexipy to hooks, or complexity
checks to CI. No routine pre-commit selection changes are implied.

The [historical two-tool baseline](../evidence/2026-10-09-complexity-evaluation.json)
contains source hashes and scores: `configure` is cyclomatic 21/cognitive 57;
`project_config` is cyclomatic 10/cognitive 28. Those historical measurements
remain failing evidence. The [October 18 remediation](../evidence/2026-10-18-complexity-remediation.md)
records the current passing source separately with before/after hashes, public
behavior checks and unchanged ceilings. New code meets both ceilings; existing over-limit
functions may only improve, with no new over-limit functions. Compare stable
file/function identities and scores, not only failure counts. Do not regenerate
a snapshot to hide regressions, suppress findings or raise limits. Refactoring
is separately scoped and verified. Routine checks passing does not establish
that the on-demand complexity checks are clean.

The [historical three-tool receipt](../evidence/2026-10-09-three-tool-complexity-evaluation.json)
records the earlier source hashes, Lizard measurements and aggregates.

See [the evaluation procedure](complexity-evaluation.md) to reproduce
the compatibility checks and interpret the evidence. Full Python grammar support
is not established by the synthetic cases.

Record comparable legacy measurements and findings as a baseline that may only
shrink. Do not transplant another project's Interrogate, coverage or mutation
percentage thresholds. Write useful docstrings; do not add filler or redundant
tests to improve a score.

For Cosmic Ray, first prove a clean unmodified test baseline, then use an
isolated disposable code checkout, a bounded time budget and per-test-run
timeouts. Keep session databases and reports outside source and operational
records. Classify surviving mutants, equivalent mutants, timeouts and tool
errors separately; inspect survivors before adding meaningful tests. A failed
baseline or broken tool execution is not a successful mutation assessment.
Its [official tutorial](https://cosmic-ray.readthedocs.io/en/latest/tutorials/intro/index.html)
documents a configurable unittest command. Selection does not prove Python 3.14
compatibility: verify a pinned release with a small synthetic unittest fixture
before adopting it. The starter now pins Cosmic Ray 8.7.0 in `hygiene`, selected
from the 8.x release family. Its [Windows/Python 3.14.8 proof](../evidence/2026-10-18-cosmic-ray.md)
uses invented standalone fixtures, not application code or a mutation-score gate.
This verifies that bounded workflow, not full Python 3.14 grammar, every platform
or adopter compatibility. The baseline CLI returns zero for a test-command launch
error; require a normal worker and a survived test result for an unmutated
baseline. Classify `incompetent`, missing/pending and abnormal worker outcomes as
tool errors; classify output `timeout` separately from genuine kills. Neither
`exec` nor `cr-report` exit zero proves all mutants completed correctly.

To reproduce explicitly, choose a new output path outside source/operational
records and run from the reviewed checkout:

```bash
uv run --locked --group hygiene python tools/engineering/evaluate_cosmic_ray.py --output REPORT.json
```

The probe uses disposable source, a 120-second subprocess budget, five-second
test timeouts and a deliberate 0.1-second timeout control. Existing receipt paths
are refused. Mutation execution and the synthetic proof stay outside hooks/CI.

## Periodic dependency freshness review

Generic maintenance belongs to gz-skills. Route authorized dependency/tool
updates to `gzs-update-dependencies` and dependency-risk assessments to
`gzs-dependency-risk-audit`, preserving project scope and authorities. This policy
binds those workflows to the selected Python family, tool choices and verification
requirements; it does not duplicate their inventory, resolution or audit process.
The pinned gz-skills v0.8.0 maintenance skill supports freshness-only review and
template/plugin inventory. Review mode leaves pins and environments unchanged.
Preserve this starter's Python 3.14 family and retired Xenon/Radon decisions over
upstream profile defaults; the pin update does not select a lite/heavy profile.

At setup/adoption, before every release, reviewed tool upgrades and quarterly
on-demand maintenance, apply
the [configuration and baseline contract](../project-configuration.md)
and [stack maintenance binding](../adoption.md#maintaining-the-adopted-stack).
Include the adopted starter revision, SP, SP-BP and gz-skills alongside runtime
and development tools. Record date, selected/latest versions, official evidence
and adopt/defer decisions; keep support floors distinct from tested pins. Preserve
app additions and overrides, and report missing evidence without claiming currency.
Release age alone does not prove abandonment. Verify changed tools on the pinned
Python patch and retain comparable complexity evidence.

Scheduled scans and update PRs may supplement these reviews under the
[two-baseline scanning contract](../baseline-policy.md#scheduled-dependency-scanning).
Cover standard and X-Plane/XPPython3 environments independently; absent declarations
or locks are coverage gaps. Updates require review and applicable verification
before merge. No automatic merge, publication, maintenance hook or extra deeper
analysis CI gate follows. Adopters choose their update sources and timing.
Keep these tool preferences starter-owned and upstream plugins agnostic. SP-BP
remains disabled until readiness and explicit adoption are established.

## Ownership and evidence

Keep code in a Git development checkout and data in a separate location. Live
databases remain local outside synced storage. For persistence, use immutable
applied migration entries, refuse to silently initialize a missing live record,
and create and verify a recovery copy with the data after every write; a failed
recovery copy fails the run. Resolve paths from one configuration module with
environment overrides. Commands are read-only or dry-run unless explicitly
asked to write; output names, counts and status only. New program-input filenames
contain no spaces; do not rename existing inputs without a reviewed migration.

Report actual checks, unresolved failures and unverified capabilities. Current
SP and gz-skills remain independently owned. SP-BP is an expected addition to
the target stack, deferred until readiness and explicit adoption are established;
existing backlog and handoff authority remains in place. Never infer plugin
installation, a profile choice or publication permission from this policy.
