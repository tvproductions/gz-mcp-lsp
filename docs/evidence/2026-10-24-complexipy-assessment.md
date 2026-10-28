# Complexipy qualification — October 24, 2026

Result: **not qualified as sole cognitive-acceptance evidence**. Latest available
complexipy 8.1.0 reproduces a meaningful traversal blind spot. Updating to the
latest package does not repair this finding. The cognitive ceiling remains 15;
no threshold or historical evidence has been rewritten to manufacture a pass.

## Source and independently reproduced finding

Gzkit's [dated October 23 technical assessment](https://github.com/tvproductions/gzkit/blob/a32243e21ec0c7ab24dbf45b5600f4fa524dd6f3/docs/governance/harbor-ro9-astral-toolchain.md)
records its retirement of complexipy, including conditional-expression
under-counting, Windows snapshot-key differences and missing quiet-mode
diagnostics. Its governance and replacement implementation are not adopted or
copied into this starter.

This starter independently tested invented fixtures on managed Python 3.14.9
and complexipy 8.1.0. Nine conditional expressions in a tuple score 9. The same
nine expressions in keyword argument values score 0. The source fixtures,
versions, API/CLI observations and source hashes are retained in
[the qualification receipt](2026-10-24-complexipy-qualification.json).

For example, the branch in `return 1 if x else 0` scores 1, while nesting that
same expression inside `return dict(value=1 if x else 0)` is missed. The
nine-expression controls establish that this is a traversal-context difference,
not simply a lower count applied uniformly to the same construct.

## Starter response

The existing `evaluate_complexity.py` now includes tuple and keyword controls,
records the failed cognitive canary, emits `compatibility: failed` and exits 1.
The new public-CLI regression proves that this defect cannot receive a passing
qualification result. That regression injects the faulty scoring, so a future
upstream fix will not be penalized for eliminating the defect. Routine tests can
pass while confirming that an analyzer
is correctly rejected; their success does not qualify the analyzer itself.

Complexipy remains pinned at the latest version for evaluation. Its reported
scores are provisional observations, not proof that cognitive acceptance passes.
The qualification failure blocks an unqualified strict release/adoption claim
until a qualified replacement, upstream fix or independent evidence satisfies
the actual cognitive requirement. Existing C901/Lizard checks remain separate
cyclomatic measurements and cannot substitute for cognitive proof.

The Windows snapshot issue was not reproduced on this Mac. The starter's
existing analysis commands use `--snapshot-ignore`, so do not infer that the
reported snapshot failure is active here. Quiet-mode diagnostic absence is a
separate observability concern; it is not evidence that every nonzero exit is
incorrect. Preserve those distinctions when reviewing an upstream fix.

Next review: a bounded cognitive-scoring contract and candidate qualification,
including calls/keywords, defaults/decorators, nested functions/lambdas,
comprehension filters, match guards, syntax errors, discovery and output/exit
behavior. Compare fixture and actual corpus results before selecting a
replacement. No gzkit lifecycle, implementation or numeric baseline is imported.
