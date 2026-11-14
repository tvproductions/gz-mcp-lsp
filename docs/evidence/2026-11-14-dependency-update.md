# Dependency update — 2026-11-14

## Scope and selections

The user authorized applying the updates after the freshness review. Rollback
is product commit `e2c084ff818dc77f37d8aa7b8292bebd579a125c`. This maintenance
changes no runtime source, test assertion, public configuration or capability.
The pending unpublished product remains **0.1.0** within its existing first-release
scope. At the dependency-update checkpoint, no commit, push, tag, release or
Backplane activation was performed. The user subsequently authorized Git
synchronization through `gzs-git-sync`; the final synchronization response records
the save point's exact commit, full gate, hosted CI and remote alignment.

| Input | Before | Selected |
| --- | --- | --- |
| ty | 0.0.103 | 0.0.104 |
| Grimp, through Import Linter | 3.19 | 3.20 |

The [complete inventory](2026-11-14-dependency-update.json) compares all 101 locked
registry packages plus uv and the isolated backend with fresh official PyPI
metadata. All 103 selections match the latest published releases, are unyanked,
and permit Python 3.14.10 in their metadata. This is version/metadata evidence,
distinct from executing every package on every supported platform. Platform
markers exclude `httpx2-jsfetch` and `pywin32` from this macOS installation.

Retain managed CPython **3.14.10**, standalone build **20261110**, uv/uv_build
**0.13.8**, the uv compatibility minimum **>=0.13.6**, MCP SDK **2.3.0**,
Ruff **0.17.5**, the lite profile and all existing analysis ceilings. Python
**3.15.2** is the newer upstream family; the approved N-1 family stays 3.14.
No other dependency ecosystem, container, submodule or vendored product binary
was found. The two synthetic fixture manifests have no dependency graphs;
local hooks have no independent tool revisions.

## Compatibility and owning tools

[ty 0.0.104](https://github.com/astral-sh/ty/releases/tag/0.0.104) corrects type
narrowing, union simplification and implicit unhashability, plus import-alias
completion behavior. The existing installed semantic tests exercise the selected
language server. Its beta API remains a compatibility risk requiring verification;
the unchanged 0.0.x version shape does not promise stability.

[Grimp 3.20](https://github.com/python-grimp/grimp/blob/v3.20/CHANGELOG.rst)
improves graph-query performance and adds optional package-oriented direct-import
queries. It permits Python >=3.11 and satisfies Import Linter 2.16's `grimp>=3.19`
requirement. Grimp remains a transitive hygiene dependency.

Used verified uv 0.13.8 before resolution. Updated the direct ty pin and ran
`uv lock --upgrade`; only ty and Grimp changed. A second full upgrade resolution
left the lock byte-identical. `uv sync --locked --all-groups` installed the
selected graph. The installed outdated query returned `[]`.

All commands and nested hooks selected the same uv 0.13.8 executable. The
task-local managed-Python installation-root setting preserved build 20261110;
this is tool provisioning, with no application environment configuration.
Shell DNS and native certificate lookup initially failed. Commands through the
available host execution path used the existing certifi trust bundle while
retaining TLS verification. All GitHub release/ref/issue checks in the update
used `gh`; no credential or global trust setting was changed.

Python 3.14's deferred annotations remain exercised by the existing SDK schema
contract tests. No concrete maintenance need justified changing executor,
compression, template-string or guarded filesystem APIs. Retaining those
implementations preserves their behavioral and recovery contracts.

## Verification

- Full all-group synchronization and four-hook gate pass: Ruff check, Ruff
  format, ty, and **189 tests**, with one Windows-only skip on macOS arm64.
  Installed real-ty navigation, diagnostics, mutations and recovery run in this
  suite; Windows write support is not established by macOS evidence.
- All **29** analyzer utility regressions pass.
- Import Linter keeps all **four** project contracts. An outside-checkout clean
  source copy passes; four separate injected forbidden imports each fail the
  intended contract with exit 1. These controls exercise Grimp 3.20 through its
  actual consumer without modifying product source.
- Source-independent sdist-to-wheel build and outside-checkout installed
  distribution verification pass. Final artifacts are rebuilt after the evidence
  refresh; the final response reports that final artifact check.
- Exact hashed all-group export plus uv/backend audit covers **101 applicable
  selections**, with zero skips and **zero known vulnerabilities**. The first
  audit attempt rejected missing hashes on the two supplemental tool entries;
  adding their official registry hashes made the corrected audit pass. No
  resolver substitution, audit fix mode or quality-rule weakening was used.

The bounded independent review found no consequential defect in the complete
package, lock, documentation and evidence diff. Prior deeper measurements remain
dated evidence; unchanged analyzer inputs do not justify reissuing them as fresh
measurements.

## Independent source and acceptance conclusions

Fresh `gh` release and tag-object queries confirm all selected full SHAs:
starter **0.9.0**, Superpowers **7.0.2**, gz-skills **0.10.1**, disabled Backplane
**0.2.0**, checkout **v7.0.1** and setup-uv **v10.3.3**. The JSON inventory records
each exact revision. No newer published starter policy was adopted; pending
unpublished starter work is separate from product provenance. Native plugin
caches, activation and unrelated machine tools were preserved. Source-pin
freshness does not re-establish native discovery or host acceptance.

The [shared-engine issue](https://github.com/tvproductions/gz-skills-first-starter/issues/1)
is still open without a milestone. No qualified cognitive engine is installed or
selected. Complexipy remains a comparison tool; G5/T12 strict acceptance is
incomplete. Earlier native Codex receipts retain their original ty versions;
fresh current-ty model/approval proof and exact-commit platform CI are not inferred
from this local gate. **T13 is not run.**
