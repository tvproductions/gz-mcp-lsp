# Gzkit cognitive scorer: shared-package assessment

The user selected gzkit's cognitive approach and asked whether it should become
a tiny external project. Recommendation: extract one independently versioned
scoring engine for gzkit and other GZ projects, including this starter. Do not
maintain a private starter fork or depend on the entire gzkit application.
This is an assessment and proposed boundary, not an extraction or publication.

## Inspected source and ownership

Review is pinned to gzkit commit
`a32243e21ec0c7ab24dbf45b5600f4fa524dd6f3`:

- [Scorer](https://github.com/tvproductions/gzkit/blob/a32243e21ec0c7ab24dbf45b5600f4fa524dd6f3/src/gzkit/complexity/cognitive.py):
  `score_cognitive(source, filename)` returns named, located function scores.
  It imports no gzkit internals; Pydantic is its only external dependency.
- [Tests](https://github.com/tvproductions/gzkit/blob/a32243e21ec0c7ab24dbf45b5600f4fa524dd6f3/tests/complexity/test_cognitive.py):
  27 unittest cases cover scoring rules, scored units, parse failures and CLI.
- [Consumer policy](https://github.com/tvproductions/gzkit/blob/a32243e21ec0c7ab24dbf45b5600f4fa524dd6f3/src/gzkit/governance/trust_audits/complexity_ceiling.py)
  already separates ceilings and baselines from scoring.
- The upstream MIT license and copyright must accompany any extraction.

Scoped searches of accessible tvproductions repositories and gzkit issues/PRs
did not locate a separately published cognitive package or extraction proposal.
That is a search observation, not proof that none exists elsewhere.

## Executed feasibility and qualification checks

The [structured receipt](2026-10-24-gzkit-cognitive-extraction.json) records exact
source/test blobs, fixtures, corpus hashes and results. Unchanged upstream source
and all 27 upstream tests ran in a disposable namespace on Python 3.14.9 with
Pydantic 2.14.1. All tests passed; neither gzkit's checkout nor starter dependencies
were changed for this experiment.

Both nine-condition tuple and keyword-argument fixtures score nine, covering
the keyword-argument blind spot independently reproduced in complexipy.
However, functions defined under module-level loops and `match` cases are
silently omitted. These functions have no enclosing function and belong to the
declared scoring population. Generic discovery qualification therefore fails.
Fix traversal and retain these negative controls before accepting a shared release.

On the current starter's `src/`, `tests/` and `tools/`, the scorer reports 102
units, maximum 13 and none above 15. Independent AST discovery finds no missing
units in that corpus. This provisional observation does not erase the failing
holdouts or establish whole-language scoring correctness.

## Proposed package and adoption contract

1. Extract source-to-score logic, immutable result records and the upstream tests.
   Keep Python 3.14 support explicit. A stdlib dataclass could remove Pydantic
   from the core; preserve gzkit's existing public model through an adapter if
   callers rely on its validation/serialization behavior.
2. Publish a documented, versioned metric contract: scoring rules, function
   discovery, qualified names/locations, nested-definition folding and error
   behavior. The existing algorithm folds nested functions into their enclosure;
   its population is not interchangeable with complexipy or Lizard.
3. Keep an optional small CLI with structured output. Parse/read/discovery
   failures must be explicit failures, never successful empty measurements.
   Prove supported statement containers and supported Python grammar with
   independent holdouts before qualification.
4. Keep thresholds, source-scope selection, legacy baselines, waivers and release
   governance in each consumer. This starter retains cognitive ceiling 15;
   importing a scorer does not import gzkit's lifecycle or baselines.
5. Have gzkit and the starter consume the same released engine with exact tested
   selections. Update through the latest-tooling review. A metric/population
   change requires explicit contract review and rebaseline, not silent comparison
   with historical scores. Use SemVer to make these compatibility decisions clear.
6. For brownfield adoption, inventory the whole declared source scope, prove
   discovery, record old/new measurements separately, fix violations or record
   explicitly owned shrinking legacy baselines, and rerun the release gate.
   Greenfield adoption starts with the qualified engine and ceiling directly.

No new repository, dependency, gzkit change, issue or release was created.
The starter's strict cognitive acceptance remains blocked pending a qualified
implementation and integration; this assessment does not claim that work done.
