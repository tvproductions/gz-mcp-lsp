# Cognitive engine consumer boundary

Status: consumer preparation shipped in 0.7.1. The maintainer confirmed on
October 26 that the shared engine is coming from gzkit, without a promised date,
and explicitly directed release without waiting. This starter contains
no scorer, private fork or extraction project. No new dependency is installed.
The cognitive exception remains active for 0.7.0 and 0.7.1. Issue #1 remains
open and unscheduled; engine availability is not a prerequisite for this release.

The current upstream scorer at gzkit commit
`05f6e3db2fa7fd0ffb6795b86263e90a33d056e7` still has blob
`bfff5db7014f6000eb35a870f852f9a6c81da50a`, identical to the previously reviewed
source with incomplete loop/match discovery. A repository search did not locate
a separately released engine. This is an observation, not proof that no future
package will exist. Do not depend on the entire gzkit application to obtain it.

## Prepared consumer contract

The provisional fixture contract `gzkit-cognitive-v1` records the selected metric
already described in the [assessment](../evidence/2026-10-24-gzkit-cognitive-extraction.md).
It is a consumer fixture identity, not an upstream package or release name.
Reconcile the actual incoming API and immutable version before selecting it.

- A scoring function accepts source text and a filename, returning located
  records with `name`, `line` and `score`. It never executes application code.
- Scored units are functions with no enclosing function, including methods and
  definitions under any module/class statement container. Names retain class
  qualification; duplicate names at different lines remain separate units.
- Nested functions, lambdas and local classes fold into the enclosing unit.
  They are not separate denominator entries. This population differs from
  complexipy/Lizard and must not be silently compared as an identical metric.
- Established structural, hybrid, boolean-sequence, comprehension-filter,
  guard, default/decorator and recursion increments are retained in fixtures.
  This starter supplies no implementation of those scoring rules.
- Compiler-invalid Python must raise SyntaxError rather than report no functions.
  Locations/scores must be actual nonnegative integers (locations start at one),
  not bools, floats or string coercions. Missing/duplicated units fail discovery.

The 42 source fixtures include tuple and keyword conditionals, module loops,
loop-else, match, methods under class match, nested definitions/classes,
duplicates, async constructs, elif versus else-if, signatures, recursion,
comprehension guards, Python 3.14 template/generic syntax, valid function-free
modules, 15/16 boundaries and invalid source/context. Expected counts are stated
independently; no candidate engine generates its own expected scores. Small
adapted upstream metric examples retain MIT attribution in NOTICE.

The fixture suite is scoped to CPython 3.14. It establishes neither Python 3.12
nor embedded X-Plane compatibility. Those need applicable grammar fixtures and
actual runtime/host evidence before an upstream selection is adopted there.

## Commands after the upstream candidate is available

First review the official release, ownership/license, API and supported runtimes.
Select the exact engine in the applicable hygiene group through uv, regenerate
its lock and verify its installed provenance. Replace `UPSTREAM_MODULE` below
with that actual module; it is a placeholder, not a currently available package.

```powershell
uv run --locked --group hygiene python -m tools.engineering.cognitive_qualification --engine UPSTREAM_MODULE:score_cognitive --output QUALIFICATION_JSON
uv run --locked --group hygiene python -m tools.engineering.cognitive_check --engine UPSTREAM_MODULE:score_cognitive --root . --paths src tests tools --output CORPUS_JSON
```

The CLI requires installed distribution/version metadata and records the actual
engine source hash. It rejects an unversioned fixture adapter. The source gate
repeats qualification before measurement and independently inventories function
identities with CPython AST traversal across all statement fields. It reads
original source with tokenize.open, reuses the existing confined/symlink-safe
scope selection, and preserves file hashes and source lines. It does not rewrite
syntax, use a fallback scorer, or import application modules.

The consumer owns ceiling 15: a measured 15 passes and 16 fails. Exit 0 means a
complete qualified measurement passes; 1 means ceiling violations (or failed
standalone engine qualification); 2 means missing engine/provenance, rejected
qualification in the corpus gate, source/discovery/scope/output errors. Partial
measurements cannot pass. Valid modules with no scored units have a null maximum;
missing/empty source scopes fail. No synthetic zeros or baseline waivers.

The 16 consumer regressions use explicit fixture-answer adapters to test
comparison, discovery and failure handling. Their success is not a scorer
qualification result. The real source corpus has not been cognitively measured
with a new engine. Keep existing failed evidence and the release exception.

## Completion still required

Once gzkit provides the candidate, pin/qualify it, run the actual corpus, compare
qualified names/population/scores with the retained historical evidence, and
review every violation without changing thresholds. Record exact engine version,
source hashes, counting semantics, runtime, findings and owned legacy baselines.
Remove the exception only after genuine qualification and required checks pass.

Run the full repository gate plus explicit analyzer regressions and verify CI
for the eventual engine implementation commit. Keep deeper analysis outside the
four routine hooks and routine CI. The user authorized publication of consumer
preparation as 0.7.1; gzkit changes, engine adoption and plugin installation remain
separate work. Do not turn the lack of an upstream delivery date into a release hold.
