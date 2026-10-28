# Initialization and design discovery receipt — 2026-10-28

## Conclusions and authorized boundary

Repository initialization/configuration and initial design discovery are complete.
**Strict starter/Python adoption acceptance remains incomplete**, and no semantic
capability is implemented or accepted. This distinction does not waive missing
gates. Human design review is required before runtime work. No release/tag was
created. Version 0.0.0 is an unreleased product scaffold marker.

The user explicitly chose lite and confirmed project trust during this session.
The initial assignment authorizes public template creation, product scaffolding,
native plugin setup and discovery, documentation and verification. It explicitly
excludes MCP/LSP runtime implementation. Superpowers brainstorming was applied as
initial discovery; the draft has not received user approach selection or approval.
A fresh builder reviewer found no consequential questions beyond the proposal's
explicit human-review decisions. No implementation plan was invoked.

## Tactical: repository and starter provenance

- gh 2.103.3 authenticated as ahuimanu; active tvproductions membership role admin.
  Target lookup established absence before creation. Credential values were not
  recorded in project files.
- `gh repo create tvproductions/gz-mcp-lsp --public --template tvproductions/gz-skills-first-starter`
  created [the public repository](https://github.com/tvproductions/gz-mcp-lsp).
  GitHub templateRepository identifies tvproductions/gz-skills-first-starter.
  Generation completed asynchronously: the first clone appeared empty; fetch
  subsequently obtained generated initial commit
  `288bee7c3c9e4f99035f648b1f5f2ccfb830c8d8`. No blank-repo approximation or
  manual source transplant was used.
- Latest published starter verified via gh as
  [v0.7.1](https://github.com/tvproductions/gz-skills-first-starter/releases/tag/v0.7.1),
  published 2026-10-27. Annotated tag object
  `0562a205f918007aaee53b3dce49d24e30bd3c6f` resolves to commit
  `27594dbaec853e6bde037b0aaf3f0427a3f053f9`. GitHub reports the tag unsigned;
  release publication and commit identity were verified, not a cryptographic signature.
- GitHub template generation uses the default branch; observed starter main was
  `ec0d3c43d4d70445adbb58d03c06adbf076004a2`. Compared with v0.7.1, it changed
  only ROADMAP.md, the 0.7.1 release receipt and starter session handoff (49 added,
  two deleted lines). Packaging/bundle pins were unchanged. The provenance lock
  correctly records the separately adopted released commit, not generated app HEAD.
- Separate clean `/tmp/gz-mcp-lsp-starter-v0.7.1` checkout matched the release SHA.
  Read README, AGENTS, adoption-0.5, adoption-workflow/adoption, project configuration,
  structure, Python/Astral policies, acceptance matrix and Python 3.14 opportunity guide.
  The runbook retains some older 0.6 examples; used verified 0.7.1 metadata/pins.
- The separate starter requires uv 0.13.5; machine uv 0.13.6 initially refused its
  exact version gate. Used documented `uv tool run --from uv==0.13.5 uv ...`,
  without changing machine uv. Locked all-group sync, version, validate and the
  four starter hooks passed. Preview was inspected, then configure --apply and
  status passed; after product adaptation status still reports configured with
  no pending files, runtime_readiness unverified as designed.
- Product `.codex/config.toml`, `.skills-first/bundle.lock.json`,
  AGENTS.skills-first.md and project update skill were written by the reviewed
  helper. Root AGENTS links and binds them. gzs-project-setup inspect/initialize/
  select recorded the user's lite choice using its two-field JSON schema.
- Product identity/packaging reconciled directly in copied pyproject, as required;
  no deletion to rerun uv init. Removed starter helper implementation/resources,
  helper tests, redundant resource generator and X-Plane baseline/job. Original
  material remains in initial Git history and upstream. Retained engineering
  policies, tools, notice/license, native catalogs and exact provenance. Original
  README/AGENTS context is preserved as docs/STARTER-README.md and STARTER-AGENTS.md.
  These historical documents do not certify product behavior.
- MIT retained after bounded license review. Isaac Phi/project attribution is in
  README/NOTICE and [license review](../discovery/licenses.md); no reference code copied.
- Public issue/PR templates, contribution/security guidance, routine CI and
  Dependabot configuration adapted. Private vulnerability reporting enabled and
  verified through gh (`enabled: true`). No release/publishing workflow added.

## Actual toolchain and freshness

Host: macOS 26.6.2 arm64; Git 2.54.0 (Apple Git-157), Codex CLI 0.165.0.
Machine default Python was 3.14.9; this was not accepted as the project runtime.
Managed project interpreter observed as CPython 3.14.10, arm64, base installation
under uv's cpython-3.14.10-macos-aarch64-none. `.venv/bin/python`, Ruff and ty
all resolved inside the project environment.

[Official Python release](https://www.python.org/downloads/release/python-31410/)
and download index verified 3.14.10; retain approved 3.14 family although 3.15
exists. Pin and CI agree at 3.14.10, metadata >=3.14,<3.15, Ruff py314, ty 3.14.
The immutable starter-supplied uv managed-download metadata source was retained.

Product selections verified against official PyPI JSON and applicable GitHub
releases: uv/uv_build 0.13.6, Ruff 0.17.3, ty 0.0.93, pre-commit 4.7.0;
all direct hygiene tools plus cohesion recorded in
[tool-freshness JSON](2026-10-28-tool-freshness.json). Lock regenerated by uv,
never hand edited; exact locked all-group sync resolved 76 packages. complexipy
updated to 8.3.0 as a reproducer only; it is not qualified cognitive authority.
ty remains pre-stable 0.0.x as inherited policy allows; review stable availability
at the next scoped maintenance/implementation review. No alternative family or
old installed patch was silently substituted.

CI actions remain reviewed immutable releases: checkout v7.0.1
`3d3c42e5aac5ba805825da76410c181273ba90b1` and setup-uv v10.3.2
`07a047e608db84b3d8c06cd9a7c7dcc9c355c18e`; latest release tags checked through gh.
Routine CI has only four engineering checks and build/artifact verification;
no deeper hygiene gate or release publication.

## Native plugin installation and discovery

See [sanitized native receipt](2026-10-28-native-discovery.json).

1. Initial native inventory found neither target plugin/marketplace. Project
   config alone was ignored before trust; native add reported plugin not found.
   After user trust confirmation, wrote only this project's native trust decision
   through schema-verified app-server config/value/write, then retried native add.
2. Skill names appeared, but actual marketplace cache HEAD was the older
   `c0a6945b2170e1cf5bee3e80738916f5b62d13a5`; Superpowers was 7.0.0. This was
   not accepted as correct revision discovery. Native
   `codex plugin marketplace upgrade skills-first-starter` refreshed to the
   configured released SHA; native add then selected Superpowers 7.0.1.
3. Compared complete installed skill-file trees with clean pinned upstream
   checkouts: Superpowers v7.0.1 at
   `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b`, 84 files, zero byte differences;
   gz-skills v0.8.0 at `75bcd11ee9371ecff1a7b3432d2af29d4bdbb788`, 44 files,
   zero byte differences. Actual marketplace HEAD matches adopted starter SHA.
4. Native add enabled the two new user defaults. Corrected those two entries
   to false using native config/value/write; retained project true values.
   Fresh independent app-server processes, initialize/initialized, config/read
   and skills/list forceReload show SP/gzs/project update skill enabled here and
   none of those starter identities outside the project. No upstream cache edited
   or skill trees copied into this repository. Unrelated plugin defaults preserved.
5. Backplane remains explicitly disabled and absent from discovered skills.
   No published release exists; latest observed development HEAD
   `c0a0a487ef8c9d9f2d8b4167ff7f307a300b7dd5` differs from retained deferred
   `d0eeee829c491da02351e793544aa16ad96461bf`. Neither proves adoption readiness.

**Freshness gap:** gz-skills latest is
[v0.8.3](https://github.com/tvproductions/gz-skills/releases/tag/v0.8.3),
`d6acc26e28ca1c4f43e5bb46d8973021d7d006c3`. Reviewed its release/compare metadata:
router/setup clarifications, portability/quality changes and stable Git-sync
metadata. Retained the released starter's reproducible 0.8.0 selection to avoid
silently rewriting its managed provenance/canonical catalog. This is a pending
independent plugin update/reconciliation, not a current-version claim or accepted
freshness exception. Owner: project maintainer; revisit at design review before
implementation/adoption acceptance. SP latest 7.0.1 matches selected version;
Backplane updates remain deferred independently.

Discovery is CLI/app-server proof, not current-conversation dynamic skill reload,
full desktop-UI workflow certification or Backplane lifecycle proof. Applied
installed Superpowers using-superpowers/brainstorming and gz-skills router/setup/
update-dependencies/quality-gate guidance within the user's explicit task boundary.

## A01–A18 acceptance record

PASS is scoped to observed scaffold behavior. UNKNOWN/FAIL blocks strict adoption;
N/A identifies an absent trigger rather than a future promise.

| ID | Result | Observed evidence / open work |
| --- | --- | --- |
| A01 | PASS | Empty initial root; direct template-generated initial commit retained; independent product identity and design-only scope; rollback by reverting reviewed product adaptation, preserving provenance |
| A02 | PASS (scaffold) | src/gz_mcp_lsp importable from clean noneditable wheel; no runtime CLI exists or is claimed; future entry point awaits review |
| A03 | PASS | uv_build 0.13.6; source-independent sdist→wheel build succeeds |
| A04 | PASS (local scope) | Root pyproject authority; ancestor scan found no parent uv/Ruff/ty/project settings; no competing root files or relevant execution environment overrides; Ruff show-settings/show-files and ty -vv confirm analyzed scope/target; other hosts unverified |
| A05 | PASS | Actual managed CPython 3.14.10 and environment/tool paths; exact pin/metadata/CI targets align |
| A06 | UNKNOWN / incomplete | Direct Python tools and action releases checked; newer gz-skills requires reviewed reconciliation, no accepted exception; cognitive selection unavailable |
| A07 | PASS | uv lock --check, exact locked all-group sync; product environment only; uv-generated lock |
| A08 | PASS | Ruff 0.17.3, ty 0.0.93, pre-commit 4.7.0; effective Ruff selection, type target; five distribution guard unittest tests pass |
| A09 | PARTIAL | Hooks installed and run; local/hooks/CI commands aligned. Hosted exact-commit result is verified during final synchronization and linked in the final report; no prior-run substitution |
| A10 | PASS | No adapter runtime dependencies yet; dev/hygiene separated; starter helper removed from lock/distribution; intended MCP SDK dependency remains proposal |
| A11 | PASS | uv build --no-sources builds sdist then wheel using pinned backend; archives inspected by verifier |
| A12 | PASS (scaffold) | Fresh temporary env outside source; wheel installed with declared dependencies (none); isolated -I import origin/version checked; no MCP behavior claim |
| A13 | N/A | Application scaffold, no supported public library API; py.typed included and wheel presence verified, no consumer typing claim |
| A14 | N/A | Single package, no uv workspace/parent membership; future semantic test fixtures do not imply a product workspace architecture |
| A15 | N/A | No private/special runtime package sources or credentials; managed Python download metadata provenance retained separately |
| A16 | N/A | No container/native/dynamic/host deployment or standalone executable; pure Python build only |
| A17 | N/A | No exported requirements or standalone application script/tool environments; temporary uv 0.13.5 runner is separate starter validation |
| A18 | UNKNOWN / incomplete | Deeper evidence below; qualified cognitive engine unavailable, no strict acceptance; product semantics and host/OS integration remain pending |

## Verification and required deeper analysis

Routine observed: `uv sync --locked --all-groups`; installed pre-commit;
`uv run --locked pre-commit run --all-files` (four hooks); `uv build --no-sources`;
`uv run --locked python tools/verify_distribution.py`. Five guard tests check
valid archives, wrong product identity, unintended runtime requirements, starter/
development payloads and source-environment leakage. Clean wheel import succeeds.
An earlier empty tests directory produced Python 3.14 unittest exit 5 and was not
counted as a pass. Distribution guards now provide meaningful scaffold checks.
No runtime tests exist, and no private regression fixture was executed.

An initial inherited analysis probe failed because its explicit scope still named
removed starter source files. Rebound it to product distribution verifier and its
own test scope; all 29 inherited engineering utility tests subsequently passed.
No analyzer thresholds changed. Utility tests run explicitly outside routine CI.

| Analysis | Scope/result | Interpretation |
| --- | --- | --- |
| Ruff C901 | src, tests, distribution verifier; passed ceiling 20 | No semantic implementation measured |
| Lizard contract | src + distribution verifier; 3 functions, max 10, mean 5.333; passed | lizard-functions-v1 ceiling 20; no Radon equivalence claim |
| Cognitive | Selected shared engine not installed/qualified; complexipy 8.3.0 synthetic qualification failed: keyword-condition score 0, expected 9 | UNKNOWN shared-engine acceptance / FAIL alternative qualification; module CLI works as `python -m tools.engineering.cognitive_check`; direct script import issue is not treated as successful execution |
| cohesion 1.2.0 | src has no classes; invented external Counter fixture CLI scored 100% | Product class analysis N/A; bounded CLI/runtime compatibility observed |
| Interrogate | src/tests/verifier: 100%, default 80% minimum passed | Presence only, docs manually reviewed; no imported project coverage target |
| Vulture | src/tests/verifier: no candidates | No runtime adapter dead-code claim |
| Bandit | src/tests/verifier: two LOW findings B404/B603 in distribution verifier | Reviewed subprocess import/call: explicit argument arrays for project-owned build verification, no shell or request inputs; no suppression added |
| Coverage.py | Five unittest guard tests: verifier 55% branch/statement combined | Packaging main path separately executed, no percentage gate invented; empty package not imported in unit run warning; not semantic coverage |
| Cosmic Ray 8.7.0 | Inherited bounded synthetic qualification: compatibility passed, 2 killed/2 survived | Failure-baseline, launch-error and timeout controls retained in receipt; not mutation testing of nonexistent runtime |
| deptry | src: one file, no dependency issues | No runtime dependency graph yet |
| pip-audit | Local all-group environment: no known vulnerabilities found; local product unindexed | No future SDK dependency audit or absence-of-vulnerability guarantee |
| Import Linter | One source module, zero dependencies, zero contracts | No directional architecture proof until modules exist; contracts await reviewed runtime |

Required FAIL/UNKNOWN/stale evidence blocks strict adoption/release acceptance.
No cognitive exception is silently borrowed from the starter maintainer. Owner of
remaining product decisions and acceptance is tvproductions/project maintainer;
revisit at design review and before implementation/release acceptance.

Sanitized analyzer receipts are retained alongside this record: Lizard, complexipy
qualification, Cosmic Ray qualification and Bandit. They describe explicit
scaffold/synthetic scopes, not future product-runtime acceptance.

## Operational: initial proposal and risks

[Draft architecture/capability matrix](../superpowers/specs/2026-10-28-semantic-navigation-design.md)
proposes official MCP SDK v2.3.0, narrow independent stdlib LSP transport, lifecycle,
document/URI synchronization and semantic boundaries. All capabilities remain
proposals. Official ty docs support the six candidate methods, including
implementation; live negotiated capabilities and synthetic behavior must prove
support. Reference v0.1.1 defect mechanism confirmed by source inspection; direct
private column-4 observation is user-provided, not rerun or copied.

Main judgment calls: initial tool subset, stdlib client versus evaluated library,
UTF-16 coordinate contract, saved-file consistency/unopened file changes, external
dependency target policy, limits/errors/truncation, ty provisioning/support and OS
coverage. Synthetic future fixtures must include three consumers and same-name
negative controls, and distinguish import references from call sites. No automatic
SDK/ty dependency installation or runtime subprocess probe was performed here.

## Strategic and release disposition

A reusable semantic navigation capability can support additional agents/servers
through narrow protocol and semantic boundaries, after evidence for each. Avoid
turning the initial adapter into a code manipulation framework. Strategic value
is trustworthy positions and lifecycle/consistency behavior, not tool count.

Public contract is not accepted yet; planned CLI/JSON/result schemas are proposals.
This initialization is development scaffolding, not a SemVer release bundle.
Every major including 1.0.0 requires a newly written PRD; none is claimed here.
Release eligibility: NO (design unapproved, runtime absent, freshness/cognitive
acceptance open). Human review is next. No runtime work proceeds automatically.
