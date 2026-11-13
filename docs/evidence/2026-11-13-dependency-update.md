# Latest-stable dependency migration — 2026-11-13

## Authority and scope

The user directed complete migration to the most current packages during
dependency maintenance, including newer stable families. They also directed the
starter itself to make this requirement explicit for all adopters, rejecting a
product-local default-mode adjustment. The separate starter development checkout
owns that policy correction; it is now pushed to upstream main as
[`d82e1b8c785043845a23f52fd4e51dbd57fba921`](https://github.com/tvproductions/gz-skills-first-starter/commit/d82e1b8c785043845a23f52fd4e51dbd57fba921),
with [passing exact-commit CI](https://github.com/tvproductions/gz-skills-first-starter/actions/runs/43436348970).
The starter checkout is clean and synchronized; no further starter changes are
pending. This product still adopts published starter 0.9.0.
No unpublished starter revision is substituted into product provenance.

Rollback is product commit `53b3841af1d6050cd58e97418689a3796c89b808`.
The [complete inventory](2026-11-13-dependency-update.json) records before,
selected and latest stable versions for 101 locked registry packages plus the
resolver and isolated build backend. All 103 selections match official live
registry releases, with no yanked selection or Python-3.14 metadata exclusion.
The installed outdated query returns an empty list. No other product ecosystem,
container, submodule or vendored binary was found; the two synthetic fixture
manifests have no independent dependency graphs. Hooks have no separate tool pins.

## Migration

| Input | Before | Selected |
| --- | --- | --- |
| uv execution/CI and uv_build | 0.13.7 | 0.13.8 |
| Ruff | 0.17.4 | 0.17.5 |
| ty | 0.0.101 | 0.0.103 |
| Coverage | 7.17.2 | 7.17.3 |
| complexipy | 8.3.0 | 9.0.0 |
| stevedore, used by Bandit/Cosmic Ray | 5.9.1 | 5.10.0 |
| CPython managed build, same 3.14.10 patch | 20261026 | 20261110 |

Official release information: [uv](https://github.com/astral-sh/uv/releases/tag/0.13.8),
[Ruff](https://github.com/astral-sh/ruff/releases/tag/0.17.5),
[ty 0.0.102](https://github.com/astral-sh/ty/releases/tag/0.0.102) and
[0.0.103](https://github.com/astral-sh/ty/releases/tag/0.0.103),
[Coverage](https://coverage.readthedocs.io/en/7.17.3/changes.html),
[complexipy](https://github.com/rohaquinlop/complexipy/releases/tag/9.0.0),
[stevedore](https://pypi.org/project/stevedore/5.10.0/).
ty's intervening diagnostic rule renames have no corresponding configured rule
names in the product; real semantic tests still verify observable results.
Ruff retains its selected routine rules and C901 ceiling. Coverage fixes repeated
function-name JSON reporting; statement/branch totals are independently recorded.

Regenerated the lock with uv 0.13.8; five locked packages changed. The backend
remains an isolated exact build requirement, outside runtime dependencies.
A second full upgrade resolution has no version churn. Python support remains
`>=3.14,<3.15`, with exact 3.14.10 in the version file and CI. Official
[Python releases](https://www.python.org/downloads/source/) still list 3.14.10
as latest in that approved N-1 family; newest upstream 3.15.2 is separate.
Refreshed the immutable download-metadata source to uv commit
`3d97a6aad5ad989c1b4fc89406d54f0dce370b72`. Verification uses its managed
20261110 build in an outside-checkout project-specific installation. Shared
Python installations and the machine-default uv 0.13.6 remain unchanged.

Commands run through `uv tool run --from uv==0.13.8 uv ...`. The task-local
`UV_PYTHON_INSTALL_DIR` points to the isolated managed installation and is
inherited by nested hooks. This is package-manager provisioning, not application
configuration. Keep that setting consistent when reproducing this exact build;
the project uv compatibility floor remains >=0.13.6 without an upper bound.

## Changed-tool verification

- Managed CPython 3.14.10, uv 0.13.8, actual imported tool versions and nested
  executable provenance are observed. All-group synchronization passes.
- All 189 product tests pass under Coverage 7.17.3, with one Windows-only skip
  on macOS arm64. Actual installed MCP/ty read, mutation and recovery tests run.
  Parent-process coverage is 87.1691% statements and 74.4444% branches, with
  zero exclusions; subprocess behavior is tested separately, not counted as
  measured child coverage.
- All 29 analyzer utility regressions pass. Ruff C901 passes at 20. Lizard
  retains `lizard-functions-v1`: 648 functions, maximum 20, weighted mean
  3.1944444444444446, with all 20/20/20 ceilings passing.
- Complexipy 9.0.0's focused compatibility probe passes; both independent tuple
  and keyword-argument conditional fixtures score the expected 9. Preserve the
  historical 8.3.0 failure. Version 9 changes scoring/populations and output;
  this is comparison evidence, **not** qualified shared cognitive authority.
  Its bounded source comparison reports `verify_archives` at 18, unchanged
  source with newly measured semantics; no threshold, suppression or acceptance
  claim is changed.
- Bandit executes through stevedore 5.10.0 with the same nine LOW findings and
  no MEDIUM/HIGH findings or analyzer errors. Cosmic Ray's disposable consumer
  controls pass with two killed/two survived and restored source; this is not
  a new product mutation-coverage claim.
- The all-group exact hashed export plus uv/uv_build audits 101 applicable
  selections with zero skips and zero known vulnerabilities. Platform markers
  explain the difference from the 103 universal inventory selections. No second
  dependency resolver or audit fix mode is used.

The first gate attempt recreated the environment with the shared interpreter
because the task-local install location was not propagated, dropping hygiene
imports; its ty failure is retained as setup evidence. Its 189 tests passed,
but concurrent documentation edits also invalidated the hook snapshot. The
corrected all-group environment passes ty and the fresh coverage run above.
An initial coverage export mistook a same-prefix test log for parallel data;
renaming probe artifacts and rerunning the export removes that warning.
No product code, test assertion, safety rule or timeout was weakened.

The full frozen-tree four-hook gate, source-independent sdist/wheel build and
outside-checkout distribution verification passed before the fresh handoff. The
user subsequently requested a fresh handoff and Git sync, authorizing the normal
product commit/push ritual. The final synchronization response records the fresh
candidate gate, exact commit, hosted CI and remaining worktree. No tag/release
publication is authorized.

## Retained boundaries

Starter 0.9.0 and its full SHA, independently selected Superpowers 7.0.2,
gz-skills 0.10.1 and disabled Backplane 0.2.0 remain latest stable releases.
Both catalogs and host activation agree with those selections. Checkout v7.0.1
and setup-uv v10.3.3 still resolve to the existing immutable action SHAs.
No native plugin/cache change or fresh native-discovery acceptance is claimed.

Python 3.14's deferred annotation semantics remain covered by SDK contract tests;
the [versioned guidance](https://docs.python.org/3.14/whatsnew/3.14.html) does not
justify unrelated executor, compression, template-string or filesystem rewrites.
The existing guarded filesystem behavior is preserved.

The [shared-engine issue](https://github.com/tvproductions/gz-skills-first-starter/issues/1)
remains open and unscheduled. G5/E3/E4 and T12 strict acceptance remain incomplete;
complexipy's fixes do not override the required shared-engine contract. Earlier
native Codex receipts retain their dated ty versions; fresh current-ty native
model/approval and hosted platform acceptance are not inferred from local tests.
T13 is not run. The pending unpublished product stays 0.1.0 within its approved
bounded first-release scope; this maintenance adds no public capability or schema.
No tag/release, Backplane activation or broad starter adoption is performed.
