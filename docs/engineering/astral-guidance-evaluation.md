# Astral guidance evaluation and bounded proposal

Implementation update: the user subsequently authorized addressing these findings.
The [acceptance contract](astral-acceptance.md), [worked migrations](astral-migrations.md)
and [starter receipt](../evidence/2026-10-18-astral-acceptance.md) now implement
the evaluated scope. The original proposal below is retained as historical context.

Follow-up: the [uv documentation deep dive](uv-deep-dive.md) and its disposable
Projects proofs qualify this proposal. Review those findings before selecting
implementation, particularly uv execution/configuration, workspace root kind
and source-independent release builds. The user's direction is maximum Astral
alignment, with applicable recommendations adopted and departures evidenced.

Evaluated October 18, 2026 against starter commit
`1c107649154b9e62f87be6416f929b8c76234151` and current official Astral
documentation. Status: proposal for review, not a new adoption requirement or
an implemented conformance checker. This continues the
[preserved assessment](../handoffs/2026-10-18-astral-guidance-evaluation.md)
without changing its historical wording.

The baseline is explicit and covers the core workflow well. Its main weakness
is repeatable adopter acceptance: requirements reach the adopter, but there is
no consolidated record connecting each requirement to observed evidence and
remaining migration work. Stronger wording alone would not close that gap.

## Requirement trace and evidence limits

The [alignment contract](astral-alignment.md), [Python policy](python.md) and
[baseline policy](../baseline-policy.md) own requirements. The
[adopter fragment](../../templates/AGENTS.skills-first.md) passes them through;
it points to the reviewed starter checkout rather than copying the full policy.

| Existing requirement | Written authority and adopter path | Concrete verification | Available evidence and limit |
| --- | --- | --- | --- |
| Packaged `src/` layout, installed imports and CLI entry points | Alignment: Package structure; fragment opening | Inspect backend/package layout, run unittest against installed imports, exercise installed CLI outside checkout | Starter has `src/`, uv_build and isolated CLI checks; no adopter migration proof |
| uv_build for pure Python; evidenced alternative for a concrete build need | Alignment: Package structure; fragment opening | Inspect build declaration, execute build and inspect distribution contents | Starter pins uv_build; compiled/custom-build adopters need their own backend proof |
| Central Python metadata/configuration and distinct dependency groups | Alignment: Configuration and environments; project configuration contract; fragment opening | Inventory root/member/nested configuration, source overrides, tool discovery and command overrides | Starter declarations are centralized; no complete effective-configuration receipt is recorded for adopters |
| Managed Python, selected family, verified current patch and exact pins | Python: Latest stable within the selected family; fragment maintenance section | Check official releases during authorized setup/maintenance, actual interpreter, `.python-version`, tool targets and CI | Historical starter receipts exist; this evaluation does not refresh dependency freshness or host runtime proof |
| Committed lock and locked routine execution | Alignment: Configuration and environments; fragment opening | `uv lock --check`, locked sync and routine commands; inspect lock diff | Starter hooks/CI use locked execution; lock consistency does not establish latest releases |
| Reviewed Ruff rules, ty and unittest; same routine gate locally/hooks/CI | Alignment: Checks and governance; Python: Routine engineering; fragment routine section | Compare command scope/configuration, run four hooks, verify hook installation and exact-commit CI | Starter four-hook contract and successful CI exist; adopter enforcement remains separately observed |
| Built artifacts, resources and installed behavior | Alignment: Package structure; fragment opening | Build sdist/wheel, inspect expected files, install wheel into clean environment outside checkout and exercise public behavior | Starter verifier checks resources and CLI behavior; it is specific to this helper, not a generic adopter verifier |
| Compatible workspace boundaries and explicit member dependency edges | Alignment: Workspaces; fragment opening | Inspect member declarations, selected root/member commands, shared lock; independently install/test members | Written guidance and partial TOML example exist; no worked workspace acceptance receipt |
| Required reconciliation with preserved behavior and evidenced exceptions | Alignment: Existing projects must reconcile; adoption workflow and backport guide; fragment opening | Record source-to-target mapping, before/after seam results and rollback; owner/evidence/revisit for exceptions | Helper tests prove preservation/configuration behavior; no completed adopter reconciliation is established |

The starter's [migration receipt](../evidence/2026-10-18-astral-alignment.md)
is historical evidence. Live remote verification found `main` and `origin/main`
equal at the evaluated commit and its
[CI run successful](https://github.com/tvproductions/gz-skills-first-starter/actions/runs/39143457492).
That does not establish another project's conformance, hook installation or
host discovery. This evaluation inspected documents, configuration and verifier
code; it did not run an adopter pilot or a cross-platform migration.

## Evaluation of the five gaps

1. **Acceptance evidence: confirmed, highest priority.** The adoption workflow
   requires reconciliation and the backport guide supplies a mapping table, but
   neither supplies a complete requirement/evidence/result record. Propose one
   ordinary Markdown acceptance section in the adopter's existing planning or
   handoff authority. It should distinguish completed configuration, remaining
   Python reconciliation and separately observed native host discovery.
2. **Worked migrations: confirmed, with narrower scope.** Existing prose and
   workspace snippets are useful but are not complete before/after migrations.
   Provide one invented application migration first, followed by typed-library
   and workspace variants. Each needs preserved behavior, changed imports and
   entry points, data/resource handling, exact commands, expected results and
   rollback. No real-project pilot is implied.
3. **Effective configuration: confirmed, with tool-specific treatment.**
   Ruff selects the nearest configuration and does not implicitly merge parent
   settings; explicit `extend` differs. A user fallback applies when no project
   config is found. ty merges user and project settings, with project precedence
   and array merging; `ty.toml` wins over same-directory `pyproject.toml`.
   Command-line settings can override both tools. A common instruction to
   "inspect nested config" is insufficient. See [Ruff configuration](https://docs.astral.sh/ruff/configuration/)
   and [ty configuration](https://docs.astral.sh/ty/configuration/).
4. **Build/deployment applicability: partially confirmed, lower priority.**
   Basic artifact verification is already required. Plain `uv build` builds an
   sdist and then its wheel, so the starter's existing command plus isolated
   wheel verifier already covers that path. The missing guidance concerns
   source independence and applicable deployment variants, not a universal
   requirement to add another build tool. See [building distributions](https://docs.astral.sh/uv/concepts/projects/build/).
5. **Documentation drift: confirmed.** Python policy's Routine engineering
   section says the expanded Ruff selection is undecided, while alignment policy
   and pyproject already select `E4/E7/E9/F/I/UP/B/SIM/RUF`. Replace that sentence
   with a reference to the approved selection during implementation; preserve
   historical evidence. No rule-family decision is needed to correct it.

## Applicability boundaries

| Case | Treatment in proposed guidance |
| --- | --- |
| Ordinary pure-Python application/library | Existing baseline applies: packaged `src/`, uv_build, locked execution, reviewed gate and installed-artifact evidence |
| Typed library | Verify `py.typed` in the wheel and the supported public typing surface; do not impose library-only marker checks on every CLI |
| Interconnected compatible packages | Apply workspace contract if using a workspace; membership does not declare dependencies or prevent imports from another member's dependencies |
| Conflicting environments or Python families | Keep independent environments with documented dependency boundaries; do not force a shared workspace resolution |
| Published/distributed package with development source overrides | Verify intended distribution dependencies separately from local overrides; record how workspace/path dependencies will be supplied |
| Deployed application | Verify the actual deployment artifact/environment; document non-editable installation where applicable rather than forbidding editable development installs |
| Private indexes | Document source selection and authentication references when used; never require credentials/private infrastructure for ordinary examples |
| Compiled extensions or required custom build behavior | Use the documented alternative-backend decision and evidence; uv_build supports pure Python only |
| Host-controlled runtime | Preserve the XPPython3 exception and validate the embedded host separately; a standalone uv run is insufficient |

These boundaries follow [project creation](https://docs.astral.sh/uv/concepts/projects/init/),
[build backend guidance](https://docs.astral.sh/uv/concepts/build-backend/),
[workspace limitations](https://docs.astral.sh/uv/concepts/projects/workspaces/)
and [editable installation guidance](https://docs.astral.sh/uv/concepts/projects/sync/#editable-installation).
The starter deliberately narrows choices Astral permits; “Astral alignment” does
not imply every starter preference is an Astral mandate.

## Proposed bounded implementation

Deliver this as related documentation work under the existing backlog authority:

1. Add `docs/engineering/astral-acceptance.md` with the requirement matrix and a
   reusable record: project/revision, requirement and authority, applicability,
   command/scope, actual result, evidence, open work, and exception
   owner/revisit condition. Use PASS/FAIL/UNKNOWN plus reasoned not-applicable;
   distinguish accepted exceptions from unqualified conformance. Unresolved
   required rows prevent a claim of complete baseline adoption.
2. Add an invented application migration example plus typed-library/workspace
   variants. Link them from acceptance, adoption workflow and backport guidance.
   Validate commands against the selected pinned tools in disposable projects;
   do not claim examples are verified before that execution exists.
3. Add tool-specific effective-configuration inspection to acceptance. Review
   relevant environment overrides without recording secret values. Compare
   analyzed files and representative settings across root/member paths and
   local/hooks/CI. Correct the stale Ruff sentence and link the new acceptance
   entry from the adopter fragment; regenerate its packaged resource copy.
4. Add the applicability table and source-independent build/deployment guidance.
   Keep application-specific verification scripts project-owned. Add no generic
   conformance CLI, maintenance workflow, routine hook or CI gate.

Pinned CLI help was inspected with uv 0.13.1, Ruff 0.15.22 and ty 0.0.89.
Useful proposed inspection commands, run from the target project root, are:

```text
uv lock --check
uv run --locked --managed-python python --version
uv run --locked ruff check --show-files .
uv run --locked ruff check --show-settings src/example_app/__init__.py
uv run --locked ty check -vv
```

The example path must be replaced with actual representative files in each
configuration scope. Ruff settings for one file do not prove whole-project
coverage. ty verbose output is supporting evidence, not a promised complete
settings dump: combine it with discovered configuration and CLI/environment
inspection. ty's `--config-file` accepts a ty-format file, not pyproject;
do not recommend `ty check --config-file pyproject.toml`. These inspection
commands do not replace the project's four routine checks or artifact tests.

Acceptance of this documentation work should require: every current mandatory
alignment requirement mapped; all three example paths actually executed on the
pinned interpreter; no claim of unsupported platform/host coverage; correct
links and generated resources; the starter's documented quality checks passing;
and no expansion of helper behavior or baseline tool selection.

The proposal clarifies existing commitments. If implementation adds obligations
or changes the adoption contract, assess it separately under
[versioning policy](../versioning.md) for a bundled minor during 0.x. Do not
preselect a version, publish a release, or create a major-release PRD for this
evaluation. Python 3.14 opportunity review: this documentation/evidence work
needs no new runtime API; defer additional machinery without a product need.

## Evaluation save-point verification

After writing this proposal and its handoff/roadmap/changelog links, local
Windows checks passed: locked all-group sync, the four routine pre-commit hooks,
bundle and both catalogs, sdist-to-wheel build, isolated installed CLI/resource
verification and `git diff --check`. This validates the documentation save point;
the proposed migration examples and adopter acceptance procedure remain unbuilt
and untested. The changes are uncommitted; no new CI run or publication is
claimed for them.
