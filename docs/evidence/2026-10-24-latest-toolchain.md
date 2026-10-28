# Latest-tooling ownership and catch-up — October 24, 2026

Scope: the unreleased 0.7.0 candidate. The user's instruction requires the
starter to own latest-tooling acceptance and insist that adopters do the same;
gz-skills remains the reusable workflow, not the owner of this decision.

The [before-change review](2026-10-24-tooling-freshness.md) records the stale
released 0.6 selections. The [current structured receipt](2026-10-24-latest-toolchain.json)
records live PyPI observations, selected/installed versions, actual executing uv,
current source-input hashes and explicit acceptance blockers. It is a dated
observation, not an evergreen latest claim.

## Executed updates

- The user confirmed the N-1 Python policy: ordinary GZ projects stay one stable
  minor behind, currently 3.14. Actual managed interpreter and CI selection are
  the latest 3.14 patch, 3.14.9. This is distinct from latest-tooling policy.
- uv/uv_build 0.13.5, Ruff 0.17.2, ty 0.0.91, complexipy 8.1.0 and Lizard 1.24.3.
  Pre-commit 4.7.0 and Cosmic Ray 8.7.0 remain latest observed releases.
- setup-uv v10.3.2, with its exact tag commit verified. Checkout v7.0.1 retained.
- SP v7.0.1 tag dereferenced to its full commit in bundle and both catalogs;
  gz-skills remains v0.8.0. Backplane has no published release and stays disabled
  at its previously reviewed snapshot, not relabeled as latest development HEAD.
- `uv lock --upgrade` refreshes compatible transitive resolutions, followed by
  locked all-group sync. New exact pins remain stable between scoped reviews.

This does not upgrade machine-global uv or native plugin caches. It is not a
full transitive currency/vulnerability audit or native SP workflow proof.

## Compatibility review and observed checks

Ruff 0.16/0.17 breaking-change notes were reviewed. The project declares its
Python target and reviewed rule selection explicitly, so changed defaults do not
silently select hundreds of extra rules or a different runtime. Existing routine
scope remains checked; broader rule-selection changes need a separate baseline
review before 0.7 release. No rule suppression or threshold relaxation was added.
The setup action targets GitHub-hosted Ubuntu. The later
[sync record](2026-10-24-git-sync.md) records successful exact-commit remote CI;
local tests alone do not establish that result.

Observed on managed Python 3.14.9 / uv 0.13.5, macOS arm64:

- Four routine hooks pass: Ruff check/format, ty and 39 adoption tests.
- Thirteen explicit analyzer tests pass, including the new negative control that
  proves cognitive qualification rejects complexipy's keyword-conditional defect.
- C901 passes at 20; Lizard passes its 20/20/20 contract, 113 functions,
  maximum 16 and overall mean 3.327433628318584, with no errors/violations.
  The original boundary/discovery fixtures still pass under Lizard 1.24.3.
- Bundle/both catalogs, resources, source-independent sdist-to-wheel build and
  isolated installed CLI/resource checks pass.
- Cosmic Ray 8.7.0 passes its bounded synthetic proof on Python 3.14.9: two killed
  and two surviving mutants, restored source, and structured baseline/timeout/
  launch-error controls. See [the receipt](2026-10-24-python-3.14.9-cosmic-ray.json).
- Complexipy qualification intentionally FAILS: nine keyword-argument conditionals
  score zero. The [assessment](2026-10-24-complexipy-assessment.md) and
  [receipt](2026-10-24-complexipy-qualification.json) own that result. Passing tests
  prove rejection works, not that this analyzer is qualified.

## Adoption and release consequence

The latest-tooling rule is passed through AGENTS, baseline/engineering policy,
the adopter fragment and native update guide, and their packaged copies. An old
range/pin does not discharge freshness. Required stale/unknown evidence blocks
strict adoption/release acceptance. Explicit host/compatibility exceptions must
stay owned, evidenced, dated and conditional/noncurrent. Each release needs a
fresh official-source review tied to the actual candidate inputs.

**Strict acceptance is BLOCKED**, despite current selected tool versions and a
passing routine/artifact gate. Cognitive replacement/independent qualification,
remaining wider baseline/host proofs are not established here. Routine remote
CI subsequently passed as recorded in the synchronization evidence.
This is a new adoption-policy minor, not a claim that the released 0.6 contract
changed in place. Version 0.7.0 remains unreleased; no tag, release publication
or real-adopter migration is performed. The later user-requested
[Git synchronization record](2026-10-24-git-sync.md) owns commit/push and CI status.
