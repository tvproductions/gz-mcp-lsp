# Dependency and plugin update — 2026-10-31

## Scope and decisions

The user requested updates after an explicit freshness review. Applied
gzs-update-dependencies in update mode, the repository's quality/sync ritual,
and gzs-change-review for the bounded diff. OpenAI Docs supplied native manager
and app-server contracts. No runtime implementation or design approval is implied.
Rollback base: product commit `3d6a869cd8cc1d20d20efa7984d88403f769409b`.

The user also directed that the product not launch at 0.0.0. Product metadata,
uv-generated lock identity, README artifact example and synthetic distribution
fixtures now use the initial development version 0.1.0. This is an unreleased
version selection; no runtime launch, tag or release publication occurs.

| Surface | Before | Selected/current stable target | Source |
| --- | --- | --- | --- |
| ty | 0.0.93 | 0.0.95 | [Release](https://github.com/astral-sh/ty/releases/tag/0.0.95) |
| filelock | 4.2.4 | 4.2.6 | [PyPI](https://pypi.org/project/filelock/) |
| multidict | 7.2.0 | 7.2.1 | [PyPI](https://pypi.org/project/multidict/) |
| nodeenv | 1.11.0 | 1.12.0 | [PyPI](https://pypi.org/project/nodeenv/) |
| platformdirs | 4.13.5 | 4.14.2 | [PyPI](https://pypi.org/project/platformdirs/) |
| python-discovery | 1.6.4 | 1.9.0 | [PyPI](https://pypi.org/project/python-discovery/) |
| virtualenv | 21.14.13 | 21.15.2 | [PyPI](https://pypi.org/project/virtualenv/) |
| setup-uv | 10.3.2 / `07a047e608db84b3d8c06cd9a7c7dcc9c355c18e` | 10.3.3 / `68559e99cc807c1eb7e9238fd43a15bba460eec2` | [Release](https://github.com/astral-sh/setup-uv/releases/tag/v10.3.3) |
| gz-skills | 0.8.0 / `75bcd11ee9371ecff1a7b3432d2af29d4bdbb788` | 0.8.3 / `d6acc26e28ca1c4f43e5bb46d8973021d7d006c3` | [Release](https://github.com/tvproductions/gz-skills/releases/tag/v0.8.3) |

The [JSON receipt](2026-10-31-dependency-update.json) inventories every external
locked package plus uv and uv_build, recording old/current/latest versions,
source URLs, retain/update decisions and the lock digest. All 77 package/tool
selections match current stable PyPI releases. The initial review encountered
invalid Python specifiers in ancient release files for three packages; querying
their newest stable artifacts resolved that probe limitation without changing
constraints or treating malformed old metadata as compatibility evidence.

Python stays managed 3.14.10, support `>=3.14,<3.15`, uv/uv_build stay 0.13.6,
Ruff stays 0.17.3 and pre-commit stays 4.7.0. Python 3.15.2 is newer upstream;
retain the explicit 3.14 family policy. All other declared hygiene pins remain
current. No missing tool from the adopted lite policy was identified; the
unqualified cognitive-engine requirement remains unresolved below. Generic
skill defaults do not reintroduce Radon, Xenon, pytest or environment-based
application settings.

The seven Python changes were resolved by uv 0.13.6 using targeted
`--upgrade-package` selections, never by editing uv.lock. No packages or dependency
edges were added or removed. Only ty changes a direct requirement; the other six
are transitive development/hygiene dependencies. Runtime dependencies remain
empty. The 76-package resolution includes the local product and 75 external
packages. A second `uv lock` produced an identical lock digest.
uv also refreshed grimp 3.18's artifact inventory with 12 newly published
CPython 3.14 Linux wheels, including free-threaded variants, uploaded October 30.
Every added URL and SHA-256 matches authoritative PyPI 3.18 metadata; no previous
artifact was removed or changed. This metadata refresh changes neither its version
nor the project's selected interpreter variant. The JSON receipt retains the
added artifact details.

## Independent plugin reconciliation

Starter [v0.7.1](https://github.com/tvproductions/gz-skills-first-starter/releases/tag/v0.7.1)
remains adopted at `27594dbaec853e6bde037b0aaf3f0427a3f053f9`.
Superpowers remains released v7.0.1 at
`2ce8aa15d05bd57213e6f746f953aafb7ded7a8b`. Both match current stable releases.
checkout remains v7.0.1 at `3d3c42e5aac5ba805825da76410c181273ba90b1`.
Backplane has no published release; its development HEAD is
`0dabbc0327b8dcc7e472b7a5781cb5ce660a225f`, distinct from retained deferred
`d0eeee829c491da02351e793544aa16ad96461bf`. Keep it disabled; newer main does
not establish readiness or authorize adoption.

Reviewed gz-skills 0.8.1–0.8.3 release notes and the four-commit comparison from
0.8.0. Changes clarify router fallback, complete quality-gate discovery, Git-sync
revalidation after reconciliation and project workflow precedence; setup and
portability scripts receive corrections. Git-sync skill metadata reaches 1.0.0,
independent of bundle 0.8.3. ty 0.0.95 includes type-checker corrections and LSP
hint-edit fixes. setup-uv 10.3.3 uses Astral's release-manifest mirror with GitHub
fallback and fixes version-specifier/cache behavior; CI retains exact uv/Python
pins and disabled caching.

Updated bundle.json, both native catalogs, the component provenance lock and the
instructions fragment together. The starter identity/version is unchanged.
README and the Python skill guide distinguish this project's independent
selection from the original starter's 0.8.0 baseline; historical measurements
remain historical with follow-up links.

The existing `skills-first-starter` marketplace name now selects this product's
Git repository on `main`, whose catalog retains immutable full component SHAs.
This follows the adopted procedure for a project-specific component selection
ahead of the shared starter. The branch selects the project-owned catalog;
component revisions never float. A fresh checkout must refresh that marketplace
before installing components. No second marketplace identity, copied upstream
skills, private local paths or shared-starter edits were introduced.

Native Codex installation used a command-scoped local marketplace override to
exercise the reviewed catalog before publication, followed by native
`plugin add gz-skills@skills-first-starter`. This installed 0.8.3; all 44 skill
files byte-match the clean v0.8.3 checkout at its resolved release commit.
Fresh independent app-server `skills/list` with `forceReload` observes 20 gz-skills
and 15 Superpowers skills plus the project update skill, with no discovery errors.
An outside-project scope observes none of these. Backplane remains absent.
Native install enabled its user default; native `config/value/write` restored
the existing false default immediately. All user marketplace/plugin defaults
match the pre-update snapshot. Native managers own cache changes; no manual cache
editing or deletion occurred.

The configured Git source refresh and exact-commit hosted CI are post-publication
observations reported in the final handoff; the local-catalog probe alone does not
prove either. This running conversation's originally loaded skill catalog is not
claimed to have changed in place. Claude/OpenCode discovery was not rerun.

## Verification and limits

Observed locally on managed CPython 3.14.10 / uv 0.13.6:

- `uv sync --locked --all-groups`: passed.
- `uv run --locked pre-commit run --all-files`: all four hooks passed; five
  distribution guard tests, no semantic tests.
- `uv build --no-sources`: source distribution and wheel built.
- `uv run --locked python tools/verify_distribution.py`: archive identity and
  isolated installed import outside the checkout passed.
- `uv run --locked --group hygiene python -m unittest discover -s tools/engineering -p 'test_*.py' -v`:
  all 29 utility regressions passed; no cognitive-engine qualification claim.
- `uv lock --check`, a second unchanged `uv lock`, and
  `uv pip list --outdated --python .venv/bin/python --format json`: passed;
  outdated result `[]`.
- `uv export --frozen --all-groups --no-emit-project` to an external requirements
  file, then strict pip-audit with `--disable-pip --require-hashes --no-deps`:
  all 75 external packages audited, zero known vulnerabilities and zero skips.
  The JSON receipt retains the results. pip-audit emitted redundant-flag guidance
  for `--no-deps`; this did not skip resolution evidence or change hashes.
- Effective Ruff settings retain Python 3.14, line length 100, routine selection
  E4/E7/E9/F/I/UP/B/SIM/RUF and C901 ceiling 20 outside routine selection.
  ty reports 0.0.95 and the environment's interpreter/tool provenance remains
  project-owned. An initial diagnostic put `--show-settings` at Ruff's top level;
  corrected `ruff check --show-settings` succeeded and did not change files.
- Project bundle/component lock/native-catalog agreement, lite profile, disabled
  Backplane and preserved global defaults passed explicit comparisons.
- The separate clean published starter checkout still validates with its own
  uv 0.13.5. Its own 0.8.0 component selection is intentionally unchanged;
  product HEAD is never labeled as starter provenance.

The bounded change review compared against the rollback commit, including
dependency edges, artifact metadata, host source selection, provenance and scope.
The independent reviewer reported no retained defect finding and identified the
same-version grimp metadata refresh, which is now explicitly recorded above.
Git-source refresh is still an operational dependency until publication. No
production source or analyzer behavior changed. No new
tests, thresholds, CI gates, schedule, tag or release were introduced.

The Python 3.14 opportunity review retains the current support/idiom policy:
annotation introspection, concurrency and filesystem API changes require a
demonstrated consumer and behavior validation. None is needed for this metadata
update; runtime modernization remains outside scope. Current versions do not
prove every 3.14 feature is supported by each analyzer.

[Cognitive integration issue #1](https://github.com/tvproductions/gz-skills-first-starter/issues/1)
remains open. The real shared engine is not installed or qualified; complexipy
remains a defect reproducer. Product implementation/semantic/actual Codex
acceptance remains unapproved and unrun. These gaps continue to block strict
adoption/release acceptance independently of this successful scoped update.

Rollback uses the prior reviewed manifest/lock/catalog/config from the base
commit, uv 0.13.6 locked sync and the native manager to reinstall the prior
gz-skills SHA. Restore the starter Git source/ref and verify discovery; preserve
unrelated native defaults. No destructive reset, force push or cache deletion
is part of rollback.
