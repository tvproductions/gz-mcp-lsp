# Project handoff — 2026-11-13

## Resume point: T12 cognitive qualification; stop before T13

Observed at **2026-11-13 18:00 UTC**, on **main in the primary checkout**, from
product base `53b3841af1d6050cd58e97418689a3796c89b808`. The user requested a fresh
handoff and Git synchronization after the complete dependency migration and the
separate upstream starter correction. The final synchronization response identifies
this save point's exact commit, hosted CI and remote alignment; do not create a
CI-receipt-only follow-up commit.

**T0–T11 are implemented. G5/T12 remains incomplete. T13 is NOT RUN.** The first
permissible next action is to check the [shared-engine owning issue](https://github.com/tvproductions/gz-skills-first-starter/issues/1)
and its workflow for an independently versioned candidate. The issue was observed
OPEN/unscheduled at this handoff. No qualified shared engine is selected or
installed here. Owner: project/starter maintainer; external prerequisite: an
available versioned engine/API that can pass the 42 independent qualification
fixtures and the actual corpus at cognitive ceiling **15**.

If a candidate exists, verify ownership, release/API and installed provenance,
then run the qualification and corpus gates documented in
[the consumer contract](engineering/cognitive-integration.md). Recheck acceptance
inputs affected by that candidate. Expected result: a complete qualified
measurement, or explicit failed/unknown evidence. If the prerequisite is still
unavailable, preserve UNKNOWN and stop; do not repeat completed T12 work merely
to rediscover the same condition. No substitute scorer, whole-gzkit lifecycle
dependency, threshold waiver or early T13 acceptance is authorized.

## Completed dependency migration

The [November 13 receipt](evidence/2026-11-13-dependency-update.md) and
[complete inventory](evidence/2026-11-13-dependency-update.json) record the
latest-stable review, before/after selections, compatibility and verification.
No product runtime source or test assertion changed in this maintenance unit.

| Input | Current selection |
| --- | --- |
| Python execution/support | Managed CPython **3.14.10**, build **20261110**; `>=3.14,<3.15` |
| uv execution/CI target; compatibility floor | **0.13.8**; **>=0.13.6**, no upper bound |
| uv_build | **0.13.8** |
| Official MCP SDK | **2.3.0** |
| ty / Ruff | **0.0.103** / **0.17.5** |
| Coverage / complexipy | **7.17.3** / **9.0.0** |
| stevedore, used by Bandit/Cosmic Ray | **5.10.0** |
| Adopted published starter | **0.9.0**, `3f76acf0038b030bf5abd85ce4a419e890d3e420` |
| Independent plugins | Superpowers **7.0.2**, gz-skills **0.10.1**, disabled Backplane **0.2.0** |
| Pending unpublished product | **0.1.0**, existing bounded [first-release scope](../ROADMAP.md) |

All 101 locked registry packages plus uv and the isolated backend matched the
latest stable registry releases at the recorded check. A second upgrade resolution
had no version churn; the installed outdated query was empty. The existing action
SHAs remain current. No native cache, global uv/Python default, application
configuration mechanism or plugin activation changed. Lite remains selected.

Complexipy 9.0.0 now gives the independently expected **9** for both tuple and
keyword-argument conditional canaries. Preserve the historical 8.3.0 failure;
the new focused compatibility result is **not shared cognitive qualification**.
Its comparison scope still reports `verify_archives` at 18. No threshold or
acceptance authority was changed to accommodate the new scoring semantics.

## Starter-wide correction is upstream and finished

The user ruled that dependency maintenance must fully migrate to the **most
current stable versions**, including newer families, and rejected fixing this
only through a local product default. The correction was made in the starter
itself and pushed to its upstream **main** as
[`d82e1b8c785043845a23f52fd4e51dbd57fba921`](https://github.com/tvproductions/gz-skills-first-starter/commit/d82e1b8c785043845a23f52fd4e51dbd57fba921).
Its [exact-commit CI](https://github.com/tvproductions/gz-skills-first-starter/actions/runs/43436348970)
passed both standard and X-Plane baseline jobs. The starter checkout was clean,
with local/remote SHA alignment and ahead/behind 0/0. **No further starter work
is underway or required by this handoff.**

The mandatory rule is front-loaded in its README and maintainer/adopter
instructions, carried through policy/maintenance guides and packaged copies,
and applies to every adopter in both lanes. A bare `gzs-update-dependencies`
invocation executes migration and verification; review-only requires an explicit
check/assessment/no-changes request. Python N-1/embedded-host policy, product
contracts, thresholds and demonstrated compatibility exceptions remain binding.

This is an upstream source correction included in pending starter **0.10.0**,
not a new published release or automatic adopter migration. This product retains
its recorded published **0.9.0** adoption and independent plugin pins. Do not
relabel product HEAD or unpublished starter main as adopted starter provenance,
repeat the starter edits, modify native caches or activate Backplane.

## Verification and limits

The November 13 candidate passed the full local four-hook gate, source-independent
sdist/wheel build and outside-checkout installed verification before this handoff
refresh. The fresh frozen-tree gate and exact-commit hosted result for this save
point are reported by the final synchronization response.

Observed on the current package set:

- **189 product tests pass**, including installed MCP/ty navigation, diagnostics,
  mutations and crash/startup recovery; macOS arm64 skips the one Windows-only
  unsupported-write rejection. Windows's established 26 POSIX-only exclusions
  do not become passing Windows write evidence.
- **29 analyzer regressions pass**. Ruff C901 passes at 20; Lizard retains its
  counting contract with 648 functions, maximum 20, weighted mean
  3.1944444444444446 and passing 20/20/20 ceilings.
- Coverage measures **87.1691% statements / 74.4444% branches**, zero exclusions,
  parent process only. Child behavior is functionally tested separately.
- Exact hashed all-group export plus resolver/backend audits **101 applicable
  selections**, zero skips and zero known vulnerabilities. This is distinct
  from the 103 universal inventory selections.
- Bandit retains nine LOWs, no MEDIUM/HIGH findings or analyzer errors. Cosmic
  Ray's changed stevedore consumer passes disposable two-killed/two-survived
  controls; it is not a new product mutation-coverage claim.
- Independent bounded review found no consequential defect in the maintenance
  diff. No hook, safety rule, deadline, test assertion or ceiling was weakened.

The [November 11 T12 receipt](evidence/2026-11-11-engineering-acceptance.md) retains
import-contract negative controls, reviewed deeper findings and bounded product
mutation evidence. Its actual Codex model/approval/failure proof used ty 0.0.101;
it is **not reissued as current-ty 0.0.103 native acceptance**. Fresh native host
proof and affected acceptance evidence must be established before terminal
acceptance. Local installed tests and green CI cannot waive G5/E3/E4 or T13.

## Reproducing the selected local environment

Run the project commands through `uv tool run --from uv==0.13.8 uv ...`, with
nested hooks resolving that same uv. The existing `.venv/pyvenv.cfg` identifies
an outside-checkout project-specific managed-Python installation. Preserve its
installation-root setting in `UV_PYTHON_INSTALL_DIR` throughout commands and
nested hooks when reproducing build 20261110. This is package-manager provisioning,
not environment-based application configuration. Omitting that location can
cause uv to recreate the environment against the older shared managed build;
resynchronize **all groups** before checking. Do not replace shared defaults.
The local installation and raw temporary probe files are not promised to exist
in another workspace; a new clone must provision its own managed environment
from the pinned metadata and lock.

Required gate, after consistent executable/interpreter selection:

```text
uv sync --locked --all-groups
uv run --locked pre-commit run --all-files
uv build --no-sources
uv run --locked python tools/verify_distribution.py
```

The four hooks remain Ruff check, Ruff format, ty and unittest. Analyzer utility
tests stay separate and were already rerun for this migration. No blanket
rerun of deeper T12 analysis is needed without changed inputs or new concerns.

## Authorities and workspace boundary

Resume through the approved [specification](superpowers/specs/2026-10-28-semantic-navigation-design.md),
[plan](superpowers/plans/2026-10-28-reference-parity.md),
[acceptance matrix](discovery/acceptance-matrix.md),
[execution record](evidence/2026-11-01-execution.md), and current receipts above.
[T11 evidence](evidence/2026-11-01-codex-acceptance.md) retains its original
installed/native/platform observations; historical stopping statements do not
supersede this resume point.

Continue only on main in the primary product checkout. A separate linked
`implementation/reference-parity` worktree at `fc3fb7d` was observed and left
untouched; it is not this session's execution target or cleanup scope. The save
point contains the complete dependency/configuration/evidence/handoff unit;
unrelated histories and native state are preserved.

Use gh for GitHub and git for repository operations. No tag/release, new product
capability, second server, generic filesystem operation, application environment
override, Windows write enablement or Backplane activation is authorized. After
G5 closes, a later bounded session may proceed to the already approved T13 review
and deliberate stop; this handoff itself grants no additional authority.
