# C/C/C contract: lizard-functions-v1

The starter's on-demand checker uses pinned Lizard 1.24.3, not Radon/Xenon.
Three ceilings are fixed at 20: each function score, each module's arithmetic
mean of function scores, and the overall function-weighted mean. Values of 20
pass; greater values fail. Means are never rounded before comparison. This
retains C's numeric boundary, not Radon's exact rank/scoring implementation.

Count functions, async functions, methods and nested functions once each using
Lizard's native scores. Nested bodies have their own score; do not synthesize
class scores. Class-body, module-level and lambda code do not enter these means;
complexipy's independent script check covers readability at module level.
Lizard counts Boolean decisions but does not add a point for assert itself.
Use its reviewed algorithm for branches, Boolean expressions, comprehensions
and match; do not translate Ruff or cognitive scores into this population.
Differences from the former measurement are explicit rebaseline decisions.

Use original source directly, without syntax rewriting or Radon emulation.
The reviewed discovery boundary rejects unsupported inline function suites such as `def f(): return 1`.
All AST function locations must match analyzer discoveries; unsupported or
ignored definitions are measurement errors, not omitted denominator entries.
Fix such parser limitations upstream or review another analyzer version; do not
rewrite application code solely to satisfy this checker. Generated-code
suppression that hides functions also fails discovery. CLI warning forgiveness
does not waive measured scores.

Scope is explicit relative files/directories within a supplied root. Duplicate
paths count once. Source symlinks and escaping/missing scopes fail. Directory
walking excludes hidden directories, plugins, archives, virtual environments,
cache and out/output/outputs trees. Supply source only; never protected inputs.
Reports contain file hashes, original line identities, measurements and errors.
No Python files is a scope error. A valid module with no functions reports mean
null and contributes no denominator; an entirely function-free scope reports
null maximum/overall mean and zero measured functions. No synthetic zero scores.

Compile/parse, decoding, missing-tool/version and discovery errors produce exit
2 and status error; partial results never pass. Ceiling violations produce exit
1 and status failed; clean measured scopes produce exit 0. Legacy violations
remain failures, not waived passes. With equal ceilings and populations, maximum
already bounds the means; retain all three independently reported checks.

From a reviewed starter checkout, use an unused temporary REPORT_DIR:

```bash
uv run --managed-python --python 3.14.9 --group hygiene python tools/engineering/complexity_check.py --root PROJECT_ROOT --paths src --output REPORT_DIR/ccc.json
uv run --managed-python --python 3.14.9 --group hygiene python -m unittest discover -s tools/engineering -p 'test_*.py' -v
```

The checker does not run Ruff/complexipy or import application code. Run those
independent hygiene checks too, even after a C/C/C failure. No baseline snapshot
can turn an absolute failure into success; compare identities/scores separately
for a ratchet. Changes to versions/counting require reviewed fixture and corpus
revalidation and a new contract version if semantics change. No hooks, routine
CI gates, schedules or SP-BP activation are implied.
