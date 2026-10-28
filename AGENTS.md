# GZ skills-first starter

This template currently supports Python projects only, in both lite and
full/heavy lanes. Other languages, likely including Go, are future scope;
do not claim their support or invent their baseline from Python policy.
This is the maintainer's opinionated consistency standard. Future CLI, TUI,
web-app and desktop-app guidance must identify language/environment applicability
and verification; do not generalize one target's proof to all product types.

For adoption into another project, start at
`docs/adoption-workflow.md` and preserve that project's instructions.
For continuation of starter development, read
`docs/handoffs/2026-10-24-session-close.md`; recheck live state before work.

This repository owns the bundle catalog, adoption helper, native marketplace
adapters, and guidance. Read README.md and docs/architecture.md before changes.
The starter owns one narrowly scoped skill, `update-gz-template`, for canonical
template updates. This user-directed exception replaces the zero-authored-skills
rule; generic engineering and dependency maintenance remain upstream-owned.
Keep all other workflow skills upstream- or project-owned; read
`docs/structure.md` and `docs/updating.md` for the ownership/update contract.
`docs/baseline-policy.md` owns adopter version-range and selection policy;
checkout pins record tested execution choices. Distinguish policy changes from
pin refreshes in release notes and adopter reviews.
This is a public scaffold; use invented fixtures and preserve upstream ownership.

Version the template independently of its upstream components and adopter apps.
This repository is the authoritative policy alignment source for gz-skills and
SP-BP as well as template adopters. Follow the consistency check and prospective
release rules in `docs/versioning.md#ecosystem-policy-authority-and-consistency`.
Backplane owns requirements tracking, labeling, backlog/release monitoring,
handoffs and lite/heavy mode definitions; reference its authority rather than
implementing those lifecycles here. Companion repository bindings do not imply
circular template adoption or impose policy on unrelated workflow consumers.
Read `docs/versioning.md`; `bundle.json` owns `template_version`, mirrored by
the starter's `pyproject.toml`. New adoption records version plus exact SHA.
For this starter and adopters, every major release, including 1.0.0, requires a
newly written PRD. Bundle related changes into minor releases using existing
backlog authority; SP-BP is intended
to assist after readiness and explicit adoption. Patches remain compatible fixes
and clarifications. See the versioning policy for the 0.x compatibility rules.
Keep `CHANGELOG.md` current for release preparation, preserve historical evidence
and never move published tags. Template edits or ordinary Git sync do not imply
tag or release publication.

SP, SP-BP, and gz-skills are independent components. FDAU is the primary design
precedent. SP-BP is an expected addition to the target stack, currently deferred
until readiness and explicit adoption are established. Keep existing backlog
and handoff authority. Do not vendor upstream skills, introduce a gzkit lifecycle,
or infer app domain rules from another adopting project. App operational skills and
supporting domain code remain project-owned.

For Python work, read `docs/engineering/python.md`. Non-gzkit projects
must follow `docs/engineering/astral-alignment.md`: maximal Astral conformance,
`src/` packaging, uv_build for pure Python, centralized pyproject configuration,
locked uv execution and installed-artifact verification. Adopters must refactor
nonconforming structure/configuration; preservation during configuration is not
an exemption. Keep behavior and authorities intact. Compatibility exceptions
need evidence, an owner and revisit condition. Apply this to the starter itself.
Complete `docs/engineering/astral-acceptance.md`, using the worked migrations.
Verify effective configuration, runtime/tool provenance, selected exact environments,
source-independent release builds and clean installed behavior. Track configuration,
Python acceptance and native discovery separately; adopt applicable Astral
recommendations and record evidenced departures. Preserve the routine hook set.
Projects started from this starter require uv-managed, pinned Python 3.14, current clear
Python idioms and suitable stdlib APIs. Consult versioned official documentation
for behavior changes, deprecations and removals; configuration alone does not
supply engineering policy. Keep metadata and tool targets aligned and validate
on the actual pinned interpreter. The documented XPPython3 host exception pins
its supported version and explains the difference.

The starter and adopters must use the latest stable baseline tooling, checked
against official live releases at setup/adoption, scoped maintenance and release
preparation. An older tool family is not a freshness exemption. Review and adopt
new stable families after compatibility verification; retained older tools need
an explicit evidenced exception, owner and dated revisit, and are not current. Python's
family deliberately stays one stable minor behind (N-1), currently 3.14.x;
XPPython3-bound projects retain the supported 3.12.x host exception. Record the
verified patch exactly in `.python-version` and CI, refreshing it during authorized
maintenance. The starter's exact patch is not a permanent adopter requirement.
Inspect/test XPPython3's embedded runtime separately; host limitations require
evidence and a revisit condition rather than an independent runtime replacement.
An installed interpreter satisfying `3.14` is not evidence of freshness. Keep
exact tool pins/locks after verification; family changes require separate review.
Record compatibility exceptions with evidence and a revisit condition. Pass this
rule to adopters through the instructions fragment and Python engineering policy.

Generic dependency maintenance belongs in gz-skills. Route authorized updates to
`gzs-update-dependencies` and dependency-risk reviews to
`gzs-dependency-risk-audit`; keep this starter's material as policy and binding
guidance. Do not add a competing local maintenance skill or generic freshness
reporter. The pinned gz-skills v0.8.0 supplies freshness-only review and
starter/template/plugin inventory through `gzs-update-dependencies`; review mode
leaves pins and environments unchanged. Preserve this starter's approved Python
family and retired-tool decisions over upstream profile defaults.

The routine standard is Ruff check/format, ty, unittest (never pytest), and
pre-commit running those checks. Favor strict, reviewed lint rules. On-demand
hygiene selects Ruff C901 (cyclomatic ceiling 20), cognitive ceiling 15 using
the user-selected gzkit CPython AST approach after qualification, and Lizard
(cyclomatic scores and aggregates). Complexipy remains only a defect reproducer,
not acceptance authority. The shared cognitive candidate is not yet installed.
The remaining selections include
Interrogate, Vulture, Bandit, branch/statement
coverage through unittest, Cosmic Ray mutation testing, deptry, pip-audit and
Import Linter, plus cohesion as a downstream class-analysis requirement. The
selected on-demand tools form an adopter minimum independent of the helper's
needs; cohesion pins and runtime verification remain adopter-owned. No starter
installation or cohesion compatibility proof is implied. Run applicable deeper
analysis at adoption/release acceptance and on demand, outside routine hooks
and routine CI. Record gaps as UNKNOWN; do not claim strict acceptance with
required missing/failed/stale evidence. Keep the approved routine
pre-commit set limited to Ruff check/format, ty and unittest. C901 is enabled only
in explicit hygiene commands, not routine Ruff selection. The new complexity
policy retires Xenon and Radon. The on-demand `tools/engineering/complexity_check.py` implements
function/module/overall ceilings of 20 under the reviewed `lizard-functions-v1`
contract. Read `docs/engineering/ccc-contract.md`; this is an explicit rebaseline, not exact
Radon equivalence. Syntax/discovery errors fail closed.
Record legacy baselines that may only shrink. Cosmic Ray 8.7.0 has a bounded
Windows/Python 3.14.8 unittest proof; read
`docs/evidence/2026-10-18-cosmic-ray.md` for its baseline exit-code limitation.
Inspect structured worker/test outcomes; exit zero alone is insufficient. The reviewed
routine Ruff selection is E4/E7/E9/F/I/UP/B/SIM/RUF. Ruff, ty and pre-commit are
pinned in dev; complexipy/Lizard/Cosmic Ray remain in hygiene. Utility ownership and
remaining deeper-tool verification remain open. Preserve existing project
authorities while completing required Astral reconciliation.

Validate pins and both catalogs after a bundle change. Use unittest, not pytest.
Test consequential adoption behavior at the public helper seam. Preserve existing
project files, explicit profile choices, and native manager state. A config file
or successful manifest validation cannot prove fresh-session skill discovery.
Report unverified host behavior and Backplane pre-release limitations explicitly.

Checks: `uv sync --locked --all-groups`, `uv run --locked pre-commit run --all-files`,
`uv run --locked skills-first-starter validate`, `uv build --no-sources`, and
`uv run --locked python tools/verify_distribution.py`. The routine hooks run only
Ruff check/format, ty and unittest. Run the checker CLI tests explicitly after
analyzer changes: `uv run --locked --group hygiene python -m unittest discover -s tools/engineering -p "test_*.py" -v` (counting-contract, portability, cognitive-qualification and consumer-gate regressions).
Refresh wheel resource copies with `uv run --locked python tools/package_resources.py`
after changing their five authoritative inputs, including the update skill;
unittest detects drift.
No plugin installation, GitHub issue mutation, tag, or release publication is
implied by editing this repository. Follow the user's actual authorization.

Strong Python/tool preferences belong to this starter and its project binding.
Keep gz-skills and SP agnostic; SP-BP should remain agnostic as well. Do not
propagate these choices into upstream plugins.

## Git synchronization ritual

When the user requests Git sync, follow this repository-owned procedure whether
or not gz-skills is installed or discoverable. An available upstream workflow
may assist; its absence does not excuse skipping these steps. Follow the user's
requested branch/PR scope. A local commit alone is not a completed sync.

1. Read project instructions and the current handoff. Inspect branch, worktree,
   staged/unstaged changes and upstream. Fetch the intended remote and inspect
   divergence before integrating changes. Preserve unrelated work; resolve
   relevant conflicts without destructive resets or force pushes.
2. Review the complete intended diff, including new files. Reconcile metadata,
   locks, catalogs and packaged copies when affected. Update changelog/handoff
   for meaningful behavior, policy, verification results and unfinished work.
   Stage only the reviewed scope; do not sweep unrelated files into the commit.
3. Use the checkout's required uv version and managed Python. If machine uv
   differs, use `uv tool run --from uv==<required-version> uv ...`; nested hooks
   must resolve the same uv. Run the documented repository gate above and
   applicable changed-tool/analyzer checks. Keep the four routine hooks intact;
   do not bypass failing checks. For documentation-only changes, reuse checks
   already passed on the same relevant inputs rather than inventing tests.
4. Commit the reviewed changes with the normal hooks enabled. Push the intended
   branch using an ordinary push. If the remote advanced, fetch, reconcile and
   rerun affected checks before retrying; never overwrite remote work.
5. Verify remote branch SHA equals the intended local commit and observe CI for
   that exact SHA through completion. A prior commit's green run is insufficient.
   Fix failures within scope and repeat affected verification. If observation is
   unavailable, report CI as unverified rather than calling the sync fully
   verified. Recheck the final SHA after any evidence follow-up commit.
6. Confirm local/remote alignment and inspect the remaining worktree. Report
   branch/commit, push status, exact-commit CI link/result and any remaining
   changes or blockers. Preserve material results in the existing handoff or
   evidence record; do not create an endless chain of CI-receipt-only commits.

Report Git synchronization, release acceptance and publication separately.
Sync neither runs every deeper release analysis nor waives missing required
evidence. Known deferred work stays explicit. Do not tag, publish, install
plugins, or modify dependent repositories as an incidental sync action.

## Starter tooling maintenance

Maintain this repository's own execution environment, not only adopter guidance.
Perform a read-only freshness review before preparing each starter release, at
scoped tool upgrades and during quarterly on-demand maintenance. Use discovered
`gzs-update-dependencies` in review mode, following
`docs/engineering/python.md#periodic-dependency-freshness-review` and
`docs/adoption.md#maintaining-the-adopted-stack`. If the skill is unavailable,
follow those documented procedures directly and report that limitation.

Inventory `.python-version`, uv/uv_build, dev and hygiene groups, uv.lock,
pre-commit/CI execution pins and pinned GitHub Actions, plus SP, gz-skills and
deferred SP-BP. Compare the latest stable releases across tooling families;
keep the explicitly approved Python/embedded-host families distinct. Review new
tool families instead of using an old range to declare currency. Installed versions, passing tests and a valid
lock do not establish freshness. Distinguish release age from abandonment.

Keep a dated receipt in `docs/evidence/` with current/latest versions or SHAs,
official evidence, compatibility findings, adopt/defer decisions, owner/revisit
for exceptions and remaining UNKNOWNs. Link the receipt from release preparation;
identify retained pins explicitly rather than describing unreviewed tooling as
current. Stale, missing or unverifiable required freshness evidence blocks
release/adoption acceptance. The starter maintainer owns this decision; invoking
gz-skills does not discharge it. A receipt must name the actual candidate inputs
and be refreshed for each release. Review mode leaves pins, locks and environments unchanged.

When an update is authorized, reconcile affected metadata, lock, Python/tool/CI
pins and guidance together through the owning tools. Plugin changes also update
both catalogs; regenerate changed wheel resources. Run the documented repository
gate and changed-tool compatibility checks on the actual pinned interpreter.
Preserve rollback and record results before claiming the update is verified.
Keep exact pins between scoped updates. Scheduled dependency scans and update
PRs are permitted for this repository's standard and X-Plane/XPPython3 baselines;
keep their Python families, dependency declarations, locks and verification
separate. Missing baseline inputs are coverage gaps, not successful scans.
Require review and applicable checks before merge; do not automatically merge,
publish releases or update native plugin/cache installations. Add no maintenance
hook or competing maintenance skill/reporter. Adopters choose whether to use
starter updates, independent upstream updates or both; no adopter schedule is
imposed. See `docs/baseline-policy.md#scheduled-dependency-scanning`.
Publication follows the user's actual release authorization.

When designing features or reviewing dependencies, assess concrete Python 3.14
gains over 3.13 using the Python policy's versioned opportunity guide. Record
benefits, compatibility risks and adopt/defer decisions; do not treat a runtime
pin as sufficient guidance or add machinery without a project need.
