# Authorized dependency and template update — 2026-11-11

## Authority, scope and rollback

The user requested `update all` after a read-only freshness review. Update all
project-managed Python packages/tools, the adopted starter and independent
plugin selections. Preserve Python `>=3.14,<3.15`, exact managed 3.14.10, lite,
four hooks, all complexity ceilings, JSON-only application settings, disabled
Backplane and existing native activation scope. No release publication or new
product capability is included. Rollback is product commit `397d48d` with its
old manifest, uv lock, starter/component records and host settings.

The [complete inventory](2026-11-11-dependency-update.json) records 101 registry
packages plus the resolver and isolated build backend, before/after versions,
authoritative version URLs and native source comparisons. Python, MCP 2.3.0,
pre-commit 4.7.0, Bandit 1.9.4, cohesion 1.2.0, complexipy 8.3.0, deptry 0.25.1,
Interrogate 1.7.0, pip-audit 2.10.1 and Vulture 2.16 remain current and unchanged.
No additional product ecosystem, container, submodule or vendored binary exists.
The two synthetic fixture manifests carry no separate dependency graphs. Local
hooks have no independent revisions; CI runner families are retained.

## Selected updates

| Input | Before | Selected |
| --- | --- | --- |
| uv execution/CI and uv_build | 0.13.6 | 0.13.7 |
| Ruff | 0.17.3 | 0.17.4 |
| ty | 0.0.95 | 0.0.101 |
| Coverage | 7.17.0 | 7.17.2 |
| Import Linter | 2.15 | 2.16 |
| Cosmic Ray | 8.7.0 | 8.9.0 |
| Lizard | 1.24.3 | 1.26.0 |
| Starter | 0.7.1 / `27594dbaec853e6bde037b0aaf3f0427a3f053f9` | 0.9.0 / `3f76acf0038b030bf5abd85ce4a419e890d3e420` |
| Superpowers | 7.0.1 / `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b` | 7.0.2 / `22f0b463e7a5e579904dd6211a520321035526f7` |
| gz-skills | 0.8.3 / `d6acc26e28ca1c4f43e5bb46d8973021d7d006c3` | 0.10.1 / `4c836e3db6d43c495863a2090daaea56585a6ea9` |
| Backplane, still disabled | prerelease `d0eeee829c491da02351e793544aa16ad96461bf` | 0.2.0 / `0b18e34e65379e729d8fece97151a1bb8604b461` |

Regenerated `uv.lock` using uv 0.13.7; 21 locked packages changed, including
15 transitive selections. No generated lock was edited by hand. Use the current
uv through `uv tool run --from uv==0.13.7 uv ...`; nested hooks resolve the same
0.13.7 executable. The project floor remains >=0.13.6, independently of CI's
tested version. No global machine-tool installation was replaced.

The immutable interpreter-metadata source remains intentional provisioning
provenance for the unchanged latest 3.14.10 patch; its retention is not a claim
that an old uv release is latest. Python 3.15.2 remains outside the selected N-1
family. Current SDK introspection tests preserve Python 3.14 deferred annotation
behavior; no unrelated stdlib/idiom rewrite is warranted by this update.

Official release reviews: [uv](https://github.com/astral-sh/uv/releases/tag/0.13.7),
[Ruff](https://github.com/astral-sh/ruff/releases/tag/0.17.4),
[Cosmic Ray](https://github.com/sixty-north/cosmic-ray/releases/tag/release/v8.9.0),
[Lizard](https://github.com/terryyin/lizard/releases/tag/1.26.0).
Ruff's SIM102 correction applies to the retained rule set. ty 0.0.100 changes
diagnostic rule identities; the final target advanced to 0.0.101 when it appeared
on [PyPI](https://pypi.org/project/ty/0.0.101/) during verification. Its
[official changelog](https://github.com/astral-sh/ty/blob/ac02f737a976359e730dd18ad02e10318cfa0cbc/CHANGELOG.md)
adds bug fixes and workspace-watch fallback. The binary reports commit
`ac02f737a`. GitHub's latest-release endpoint still reported 0.0.100 during
publication; that lag does not override the non-yanked stable registry release.
Import Linter 2.16 is verified through PyPI; its GitHub latest-release endpoint
returned 404, so no GitHub release receipt is invented.

`actions/checkout` v7.0.1 at `3d3c42e5aac5ba805825da76410c181273ba90b1`
and `astral-sh/setup-uv` v10.3.3 at
`68559e99cc807c1eb7e9238fd43a15bba460eec2` still match their official latest
stable tag commits. No action update was needed.

## Starter and native reconciliation

The clean separate published 0.9.0 checkout's HEAD, tag and template manifest
agree. Its locked helper `version` and `validate` pass using its supported uv.
Generated candidates only in a disposable directory. Reviewed old/current/target
content and reconciled the instructions fragment, update skill, baseline,
engineering/adoption guidance, versioning and both component catalogs.
New upstream-only evidence links point to that exact starter revision rather
than presenting upstream receipts as product measurements.

Adopt the released scope/activation safeguards, three-host guidance, explicit
release-scope accounting and Python policy ownership corrections. Preserve the
product-owned marketplace source on main, immutable independent component SHAs,
product uv floor, cohort of hygiene tools, no application environment overrides,
lite and duplicate-source exclusion. `status` from the pristine starter reports
its expected managed-source conflict: this product intentionally uses its own
catalog and independent newer component pins, plus customized instructions.
No force-overwrite or helper conformance claim is made.

The native manager already held the target version directories. Compared each
entire cached tree against a GitHub archive of its published full SHA: all
236 Superpowers, 115 gz-skills and 542 Backplane files match byte-for-byte;
no missing, differing or extra files. This establishes source-content identity,
not merely a version label. No shared cache was edited or plugin reinstalled.
The user's configuration hash remains unchanged. After pushing maintenance
commit `1f8b16e`, `codex plugin marketplace upgrade skills-first-starter --json`
completed with no errors. The native manager's installed source refs match all
three selected full SHAs and retain enabled/enabled/disabled scope for
Superpowers/gz-skills/Backplane. Fresh project discovery still reports 20
gz-skills 0.10.1 entries with zero duplicates/errors. Outside discovery remains
20 standalone 0.8.3 entries, and user configuration is byte-unchanged. No plugin
reinstallation or activation change was needed. This closes the observed source
mismatch, not changed-runtime native model/approval acceptance.

## Verification and retained acceptance gaps

The initial full gate on ty 0.0.100 exposed a test setup leak: after correctly
checking a 50 ms mutation drain timeout, the test left that deadline active for
an unrelated filesystem-backed read. The traceback identifies the final read's
`Documents.generation` acquisition. Restore the original Config in `finally`
after the same WORKSPACE_BUSY assertion; no runtime timeout or write-safety rule
changes. The focused test passes afterward. Initial branch/statement coverage
on ty 0.0.100 also completed 186 tests with one expected Windows-only skip and
90% combined coverage; this is not final-ty coverage evidence.

Lizard 1.26.0 gives identical source hashes, function locations and scores to
1.24.3 on 70 Python files. Only then update its exact-version guard. All 29
utility tests pass, including positive/boundary/negative counting cases,
unsupported-discovery cases and cognitive harness controls. No counting
semantics or 20/20/20 ceiling changed, so `lizard-functions-v1` is retained.

Observed deeper checks on the actual product scope:

| Check | Result and limit |
| --- | --- |
| Ruff C901, src/tests/tools/engineering | PASS, retained ceiling 20 |
| Lizard, final source population | FAIL: five existing functions exceed 20; 638 functions, maximum 27, weighted mean 3.2288, no discovery errors |
| Cosmic Ray 8.9.0 | PASS disposable compatibility controls; two killed/two survived, source restored; not product mutation coverage |
| deptry | PASS, 18 runtime files scanned |
| pip-audit | PASS: all 103 exact, hashed package/tool selections, zero skips, zero known vulnerabilities |
| Import Linter | FAIL: no product contracts configured; explicit T12 work, no claim of boundary enforcement |
| cohesion | CLI runs on actual src classes; data-only classes score zero by construction; findings need T12 responsibility review |
| Interrogate | FAIL its tool-default 80% threshold: 40.6%; no new project gate introduced |
| Vulture | Four 60%-confidence candidates; two MCP-decorated tools and two inspection properties require consumer review, not deletion |
| Bandit | Nine LOW findings: eight assertions and subprocess import; no higher-severity finding; T12 trust-boundary review remains required |
| Cognitive scoring | UNKNOWN: qualified shared engine unavailable; complexipy remains a defect reproducer |

The five Lizard findings are `edit_plan.plan_workspace_edit` 25,
`filesystem._record` 27, `mcp_api._strict_arguments` 26,
`workspace._check_ty_roots` 24 and `tests/support/fake_lsp.main` 22. The
unchanged old/new measurements prove these are pre-existing findings. Do not
raise ceilings, broaden suppressions or substitute complexipy as cognitive
authority. Starter [issue #1](https://github.com/tvproductions/gz-skills-first-starter/issues/1)
remains open. Owner: project maintainer, with shared-engine qualification dependent
on upstream availability; revisit during T12 before strict acceptance.

Final-ty unittest execution passed all 186 discovered tests with one expected
Windows-only skip. Ruff check/format and ty check pass. An intermediate hook run
correctly rejected documentation edited concurrently with its passing tests;
the rerun on a frozen full diff passes all four hooks. Normal commit hooks also
passed. `uv build --no-sources` and the outside-source distribution check
pass on the final dependency set. All 103 final exact selections audit cleanly
with no skips. `uv pip list --outdated` reports no installed outdated packages.
Second resolution of the refreshed lock is unchanged; final lock validation passes.

Independent review against `397d48d` found and corrected the project uv floor/CI
wording and the product-versus-starter Lizard command context. Its focused
timeout test and diff checks pass; no introduced runtime defect was found.
Maintenance commit `1f8b16e28c452e1367e666e02963b750a6a4ec81` was pushed to
main with a clean, aligned worktree.
[Exact-commit CI](https://github.com/tvproductions/gz-mcp-lsp/actions/runs/43035668745)
passed all four hooks, build and distribution checks on Linux x86_64, macOS arm64
and Windows AMD64. All discovered 186 tests; expected skips were 1/1/26 for
Linux/macOS/Windows. This completion is preserved with the user's subsequent
explicit handoff request, not a self-generated CI receipt commit chain.
Passing routine checks cannot waive the
retained engineering findings or establish fresh native model/approval behavior
for the changed runtime. T12/T13 and strict adoption/release acceptance remain
unfinished. This maintenance belongs to the existing unpublished **0.1.0** scope
recorded in [ROADMAP.md](../../ROADMAP.md); no tag or release is published.
