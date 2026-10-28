# Complexity evaluation: Python 3.14

Run the `tools/engineering/evaluate_complexity.py` explicitly after a reviewed
tool upgrade, from the starter root using its `hygiene` group. This is a
compatibility probe, not a hook, CI gate or application refactor command.
Provide an output path in a task-specific temporary directory:

```bash
uv run --managed-python --python 3.14.8 --group hygiene python tools/engineering/evaluate_complexity.py --output REPORT_DIR/evaluation.json
```

The probe checks generic functions and type aliases, template strings and match;
cyclomatic 20/21 boundaries; cognitive 15/21 nesting boundaries; invalid syntax
failure; and the starter, tests and probe's measured scores. It does not rewrite code
or baselines. Lizard scores, each source module mean and the overall
function-weighted mean are also recorded; these are an approximation baseline,
not a final C/C/C enforcement or exact Radon-equivalence proof. Its output distinguishes tool compatibility from source violations.
Scores and file hashes permit comparison with the saved October 9 baseline.

Cyclomatic 20 keeps the former C rank's numeric boundary. Cognitive 15 uses
complexipy's documented default as a readable-code ceiling. The nested fixture
shows why both are useful: six nested conditions yield Ruff 7 but complexipy 21.
Five nested conditions yield cognitive 15. Flat branches at cyclomatic 20 can
still fail cognitive 15; the pair is intentionally stricter on some structures.
This is not exact Xenon equivalence. Test bodies retain the same ceilings;
record baseline violations rather than widening test thresholds.

Sources: [Ruff C901](https://docs.astral.sh/ruff/rules/complex-structure/),
[complexipy usage](https://complexipy.com/usage-guide/),
[metric comparison](https://complexipy.com/comparison-with-ruff/).

Lizard 1.24.1 is the selected additional analyzer. Verify score boundaries and
function discovery with its Python API, not CLI display parsing. The focused
probe does not prove complete support for modern constructs or replacement of
Radon maintainability/raw metrics. See [Lizard](https://github.com/terryyin/lizard).

## cob_reports comparison corpus

The [October 9 source-only comparison](../evidence/2026-10-09-cob-reports-complexity-parity.json)
uses 88 tracked source files with current local edits. All 621 legacy
function/method locations matched Lizard; 585 scores matched exactly. One
individual 20-boundary verdict changed, but cognitive 15 caught that function.
Combined exploratory checks retained all 43 legacy failing functions and added
31 failures among previously passing functions. Ruff alone found eight.
Module violations changed from eight to twelve because classes/nested functions
and scores change the populations. This supports Lizard-backed three-part
aggregation plus independent Ruff/complexipy checks; it does not establish
universal equivalence or install a final gate. Settle the counting contract and
invented-fixture proof before adopting or relaxing any thresholds.

The [settled contract](ccc-contract.md) and `tools/engineering/complexity_check.py` now
implement the three-part gate. Earlier pending statements above describe the
comparison stage. Use the checker for enforcement, the probe for compatibility.
