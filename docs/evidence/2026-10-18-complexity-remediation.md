# Complexity remediation — October 18, 2026

The user requested the next backlog item after Astral alignment. Scope is the
next repository-local code item: recorded helper complexity debt. Fresh-session
host adoption proofs remain open and are not inferred from this verification.
All preceding uncommitted 0.4.0 alignment work is retained. No version, dependency,
analyzer contract, threshold, routine hook or CI change follows from this refactor.

## Behavior and structure

`project_config` separates plugin-source activation checks and missing-table
rendering from preservation of the existing TOML bytes. `configure` separates
root/discovery checks, candidate generation, write planning and rollback-aware
application. The write primitive still creates absent files exclusively and
replaces existing configuration through a sibling temporary file. All candidates
are checked before any write; each destination is checked again when applying.
Failure restores completed writes in reverse order. Existing error messages,
file ordering, preview/apply/status output and managed content are preserved.

Four public-helper tests were added and passed against the pre-refactor helper:
failed replacement preserves the original and removes its temporary file;
a later write failure restores both newly created and replaced files; a
concurrent later file survives while prior writes roll back; and disabled
alternate plugin sources remain intact with repeat adoption a no-op. They pass
again against the refactor. Existing tests cover UTF-8/line-ending preservation,
profiles, legacy/duplicate discovery, symlinks, provenance and conflicts.

The full scan also found pre-existing cognitive complexity 19 in the checker
scope resolver. Extract `scope_path` validation from discovery without changing
paths, excluded trees, symlink handling, error messages or native scoring. New
CLI coverage checks parent escapes, absolute/excluded paths and explicit symlink
scopes. The eleven checker CLI tests and portability regression pass. No source
normalization or measurement suppression was introduced.

## Measurements

Measured with managed Python 3.14.8 on Windows, Ruff 0.15.22, complexipy 8.0.1
and Lizard 1.24.1. The current pre-refactor helper already differs slightly from
the October 9 source; retain its historical scores rather than relabeling them.

| Function / measure | Current pre-refactor | After |
| --- | --- | --- |
| `configure`, Ruff cyclomatic | 21 | 3 |
| `configure`, cognitive | 56 | 4 |
| `project_config`, Ruff cyclomatic | 10 | 2 |
| `project_config`, cognitive | 28 | 1 |
| `source_files`, cognitive | 19 | 2 |
| Extracted `scope_path`, cognitive | Part of `source_files` | 10 |
| Full-scope Lizard maximum | 30 | 16 |
| Full-scope Lizard overall mean | 3.7037037037037037 | 3.306122448979592 |
| Full-scope measured functions | 81 | 98 |
| Full-scope cognitive maximum after | — | 14 |

The same explicit Lizard scope, `src tests tools`, has zero violations and zero
measurement errors after remediation. Function extraction and regression tests
change the population; averages are reported for visibility rather than treated
as equal-population proof. Maximum scores and absolute pass/fail checks establish
conformance. No ceiling was raised and no failure was waived by a new snapshot.

Receipts retain source hashes and measured identities:

- [Helper before](2026-10-18-configure-before.json) and
  [helper after](2026-10-18-configure-after.json).
- [Lizard before](2026-10-18-starter-ccc-before.json) and
  [Lizard after](2026-10-18-starter-ccc-after.json), under `lizard-functions-v1`.
  The checker hash changes because scope validation was extracted; native
  scoring, discovery rules and thresholds are unchanged and contract-tested.
- [Full cognitive scan after](2026-10-18-starter-cognitive-after.json), including
  script-level scores. Paths are relative Windows paths in these local receipts.

The pre-refactor Lizard receipt fails with exit 1 and one violation. The
intermediate full cognitive scan exposed the existing scope-resolver violation;
the final scan passes. Original October 9 receipts and the preceding Astral
alignment receipt remain unchanged.

## Verification and limits

Passed: 35 routine adoption unittest tests; twelve explicitly invoked analyzer
tests; Ruff check/format; ty; all four approved pre-commit hooks; bundle and both
catalogs; locked sync/lock consistency; wheel built from sdist; isolated installed
CLI validation, preview/apply/status/idempotence and missing-provenance refusal.

All three independent complexity checks passed on `src tests tools`:

```text
uv run --locked --group hygiene ruff check --select C901 --ignore-noqa src tests tools
uv run --locked --group hygiene complexipy src tests tools --max-complexity-allowed 15 --no-ignore --snapshot-ignore --check-script
uv run --locked --group hygiene python tools/engineering/complexity_check.py --root . --paths src tests tools --output REPORT.json
```

These remain on-demand checks, outside hooks and CI. The unchanged six-line
root compatibility launcher delegates to the installed package and is outside
this explicit analyzer scope. Python 3.14's new copy/move APIs would alter the
write/overwrite/metadata contract without a demonstrated benefit here; preserve
existing exclusive creation and replacement. Concurrency, compression, template
strings and annotation introspection add no value to this decomposition and
remain deferred. No new runtime API or dependency is needed.

Local results do not establish remote CI, macOS/Linux execution, native skill
loading, Backplane readiness or downstream application conformance. Publication,
plugin installation and adopting-repository changes were not performed.
