# gz-mcp-lsp

Read README.md, AGENTS.skills-first.md and current revision evidence at
`docs/evidence/2026-10-28-design-revision.md` before work; initialization evidence
at `docs/evidence/2026-10-28-initialization.md` remains historical. The adopted starter
engineering policies in `docs/engineering/`, `docs/baseline-policy.md` and
`docs/versioning.md` remain authoritative. Historical starter implementation
instructions do not make its helper part of this product.

## Current boundary

The user approved the revised plan on 2026-11-01 and directed execution of T0â€“T13
within its linked specification. Implement all six reference tools (definition,
references, diagnostics, hover, rename_symbol, edit_file) and the three bounded
semantic extensions under the approved contracts and acceptance gates.
Read `docs/superpowers/specs/2026-10-28-semantic-navigation-design.md`,
`docs/discovery/reference-parity.md`, `docs/discovery/acceptance-matrix.md` and
`docs/superpowers/plans/2026-10-28-reference-parity.md`. They are approved execution
artifacts; see `docs/evidence/2026-11-01-execution.md` for approval, progress and
remaining acceptance gaps. Resume through docs/handoff.md, one bounded stage
per session; T11 is implemented; T12 measurements and current native evidence are recorded,
but strict G5 remains incomplete pending shared cognitive qualification. T13 is not run.
On November 14 the user directed pre-1.0 consumability discussion/design for PyPI,
GitHub releases, GitHub Pages and Read the Docs, with a version of at least 0.2.0
and cognitive qualification retained as an open gap. Resume that discussion from
the handoff; do not stop independent readiness work at the unavailable engine or
claim strict G5 passed. Metadata remains 0.1.0 until the bump is implemented.
The user expects version advancement at completed backlog boundaries; the starter
is handling its own shared policy correction separately. No starter changes,
new publication implementation, tag or release follows from this handoff request.
Earlier planning-only receipts remain historical.

Use adopted Superpowers for feature design and gz-skills gzs-router for portable
engineering selection. The user explicitly selected lite through gzs-project-setup.
Keep Backplane disabled; preserve native manager caches and unrelated defaults.
Use the project update-gz-template skill for starter maintenance. No gzkit lifecycle.
Project issues/PRs and review documents are the current planning authority.

## Product constraints

Independent Python implementation using the official MCP Python SDK at its
MCP boundary. One workspace, one ty process, stdio only. Six-tool functional parity
includes diagnostics and guarded rename/edit; canonical navigation uses exact URI
and identifier position, retaining full/selection range distinction. Mutations are
disabled by default in the proposed runtime and require bounded operator authority,
preview/apply and recovery evidence. No unsolicited LSP applyEdit, execute-command,
code actions, generic filesystem management, request-time installation, hosted
infrastructure, general LSP framework or second language server.
No private source or project data in this public repository.

## Engineering and configuration

Python 3.14 family; exact verified managed patch 3.14.10 in `.python-version` and CI.
uv >=0.13.6 (CI tests 0.13.8), project-owned lock, src packaging and uv_build.
Centralize Python/tool metadata in pyproject.toml. Application settings will be project-owned JSON;
**no environment-variable-based application configuration**. This explicit product
rule overrides inherited suggestions for environment overrides. Native host config
retains its own format. No Makefile. unittest only, never pytest.

Preserve routine Ruff selection E4/E7/E9/F/I/UP/B/SIM/RUF and ceilings: C901 20,
qualified cognitive 15, Lizard function/module/overall 20. C901 and deeper checks
remain outside routine hooks/CI. Cognitive qualification is unresolved upstream;
complexipy is an unqualified comparison tool, never passing cognitive authority.
Freshness, configuration, native discovery, Python acceptance and product
capability acceptance are separate conclusions. Missing evidence stays UNKNOWN.
Required missing/failed/stale results block strict adoption/release acceptance.
Do not replace policies with copied upstream profile defaults.

## Gate

```bash
uv sync --locked --all-groups
uv run --locked pre-commit run --all-files
uv build --no-sources
uv run --locked python tools/verify_distribution.py
```

The four hooks are Ruff check, Ruff format, ty and unittest. The unittest hook
runs tests/, including distribution, protocol, semantic/installed integrations
and pure edit-planning tests. T0-T11 are implemented; runtime mutations remain
disabled by default and unsupported on Windows. The final sync response records
T11's exact-commit three-platform CI; T12/T13 strict acceptance remains pending.
Inherited utility tests remain outside routine CI and run explicitly:
`uv run --locked --group hygiene python -m unittest discover -s tools/engineering -p 'test_*.py' -v`.
Verify relevant effective configuration, interpreter/tool provenance and artifacts
outside the checkout. Use the separate published starter checkout for helper
validation/configuration/status, with its own supported uv; never relabel product HEAD
as a starter revision. Product runtime has no starter dependency.

Every major including 1.0.0 requires a new PRD. Use SemVer for the eventual
CLI, configuration, schemas and behavior. No tag/release publication without
explicit authorization. Initialization is not release acceptance.

## Git synchronization

Use `gh` for GitHub reads and authorized writes, including `gh api`; use `git`
for repository operations, fetch and push. Prefer this CLI workflow over GitHub
connectors/browser automation unless the user requests otherwise.

Follow the starter's preserved Git synchronization ritual in
`docs/STARTER-AGENTS.md#git-synchronization-ritual`: inspect/fetch and review the
complete diff, run the gate with supported uv resolved consistently in nested
hooks, commit without bypass, push without force, observe exact-commit CI, and verify local/remote SHA
alignment. Report remaining gaps independently of Git sync. Keep changelog and
initialization evidence current. Do not manufacture CI receipt-only commit chains.

## Release planning and version advancement

PRDs guide major releases; selected work and requirements drive minor releases;
fixes drive patch releases. Follow the canonical starter policy at
https://github.com/tvproductions/gz-skills-first-starter/blob/main/docs/versioning.md#plan-releases-from-their-governing-work
and this project binding. Every major, including 1.0.0, requires a newly written
PRD defining that major's outcomes, requirements and acceptance criteria.

Before implementation planning, identify the release scope served by the work.
Keep a current release-scope record in this project's existing backlog, roadmap
or release authority: actual last published version/tag/revision (or evidence of
no prior release), proposed next version, governing PRD/requirements/fixes,
included completed and remaining work, deferred work, compatibility impact and
acceptance gates. Reconcile completed changes into that record before closeout.
Missing scope/version evidence blocks release-preparation acceptance. Do not
silently shrink approved scope or include the entire future backlog in one release.

Apply SemVer to the complete selected scope since the published baseline.
After 1.0, incompatible contracts require major, compatible requirements/capability
or public deprecations require minor, and compatible fixes require patch. During
0.x, requirements/capability and incompatible changes require minor; compatible
fixes require patch. Multiple tasks in one release share its pending version.
An initial unpublished 0.1.0 may cover an explicitly selected first-release scope;
review scope growth instead of using unpublished status to avoid release accounting.
Keep metadata/runtime mirrors, affected lock metadata and changelog aligned when
the pending version is selected. Preserve published versions/tags, independent
product/template/plugin versions and existing release gates. These instructions
do not authorize publication or enable deferred Backplane.

### Required version decision checks

At requirements intake, planning and closeout, agents MUST derive the pending
target from the actual published baseline and the complete pending scope.
Identify the new major PRD, selected minor requirements or commitment corrected
by a patch. A ticket labeled fix cannot turn new requirements into patch work.
Use the highest required increment and reset lower components: 1.4.2 becomes
1.4.3 for fixes, 1.5.0 for compatible requirements, or 2.0.0 for a breaking
major guided by a newly written PRD. During 0.x, requirements drive 0.4.2 to
0.5.0; compatible fixes drive 0.4.3. Reuse an adequate pending target rather
than incrementing once per task. Reconcile version mirrors and changelog in
the same authorized change; do not ask the maintainer to choose routine numbers.

Require a finite release outcome, included requirements, exclusions and an
acceptance gate, including for the initial 0.1.0. Assign future requirements
to later minor bundles. Preserve approved scope; ask only for unresolved
product decisions. Missing required PRD, scope or consistent version evidence
blocks the applicable planning and closeout claims as well as release preparation.
Report published baseline -> pending target, governing source, compatibility,
version agreement, completed/remaining/deferred work and publication status.
A selected target does not assert readiness or authorize publication. Use the
canonical policy's required-version-decision-procedure; keep the record in
existing project authorities rather than creating another tracker.

### Historical November 1, 2026 local release-accounting review

This historical review predates the November 14 readiness direction in ROADMAP.md
and docs/handoff.md; that newer scope and at-least-0.2.0 direction remain current.

Development metadata is 0.1.0; no local release tags or GitHub releases were found
on 2026-11-01. The approved reference-parity plan and docs/handoff.md retain the
T0-T13 acceptance scope (T11 implemented; T12/T13 pending at audit). Keep that
first-release scope explicit in ROADMAP.md; do not infer a minor bump from task
count. The inherited docs/versioning.md describes the starter, not this product
release history. Future work outside the selected first-release requirements needs
a separate release disposition.

Reviewed source: starter base commit
`8d090f88bf45b9a755808a62c1445beeb005daff` plus the authorized, uncommitted
0.8.1 clarification. This is development guidance, not a published template
upgrade. Reviewed `docs/versioning.md` SHA-256:
`960cc4052cb87696980be23a393553079f254ac8105240dbcbac5244a52c4460`;
`templates/AGENTS.skills-first.md` SHA-256:
`0383bc3330756600b2d9e0ae2393af0143836b7e6bc3b5b8d407e39f361b51b4`.
No adoption lock, component pin, plugin activation or product version is changed.
