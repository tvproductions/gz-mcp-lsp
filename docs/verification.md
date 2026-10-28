# Initial scaffold verification — October 9, 2026

The initial source passed these local checks on Python 3.13.15:

- Thirteen unittest cases covering preview/no-write, idempotence, preservation
  of existing instructions/configuration, disabled/foreign plugin conflicts,
  gzkit separation, symlink destinations, legacy skill copies, profile preservation,
  malformed settings, immutable pins, and matching catalogs.
- Ruff 0.15.18 lint and formatting checks.
- Bundle validation against independently resolved published upstream revisions.
- Skill Creator frontmatter/name validation for `adopt-skills-stack`.
- Claude Code strict marketplace validation: no errors or warnings.

Codex CLI 0.160.0 recognized the local marketplace through command-scoped
configuration. Its read-only plugin listing did not return this bundle's
available entries, including with network access. No plugin add or global
configuration mutation was performed. This is a native-loading verification
gap, not a passing installation receipt. Complete the fresh-session Codex
installation proof before claiming the bundle is loaded or project-scoped
native operation is verified.

No application projects were migrated or operational records accessed. Backplane
remains a pre-release published commit. End-to-end Claude operation, OpenCode,
combined-stack runtime conformance, update/rollback automation, and the FDAU pilot
are not established by these local tests. CI provides the separate Python-version
matrix; report its actual result rather than assuming these local checks prove it.

## Backport and front-door update — October 9, 2026

Nineteen unittest cases passed on Python 3.13.15, including deferred Backplane
configuration, preservation of existing enabled Backplane state, front-door
preservation/duplicate discovery, and bounded read-only structural assessment.
Both starter skills passed Skill Creator validation; Ruff lint/format and bundle
validation passed. The three upstream revisions and native catalogs are unchanged.

No target application was restructured or plugin installed. The new front door
is authored and staged by the helper; fresh-session native discovery is still
unverified. The backport assessment is a starting inventory, not evidence that
an application's structure or behavior has been audited.

## Python 3.14 and uv — October 9, 2026

User narrowed the starter runtime and CI target to Python 3.14 only. The project
now records `>=3.14,<3.15`, a `.python-version` of `3.14`, and a uv lockfile.
Local commands and GitHub CI use uv; Ruff remains pinned to 0.15.18.
All nineteen unittest cases, bundle validation, and Ruff lint/format checks passed
using uv-managed CPython 3.14.6. Earlier multi-version CI results above remain
historical evidence. The new single-version workflow has not yet run on GitHub.
SP-BP remains deferred; native loading and fresh-session discovery are unchanged.

Final patch verification: uv 0.13.0 and uv-managed CPython 3.14.8 now pass
all nineteen tests, bundle validation and Ruff lint/format checks. Changes remain
local; the updated GitHub workflow and native discovery remain unverified.

## Python engineering guidance — October 9, 2026

Root AGENTS and the reusable `skills/python-engineering/SKILL.md` now specify
required Python 3.14 engineering policy and on-demand hygiene, including the
user-selected Cosmic Ray mutation tester. README no longer leaves the Python
baseline to each adopter. SP-BP is explicitly an expected addition to the target
stack, with its existing disabled pin and readiness boundary unchanged.

On uv-managed CPython 3.14.8: nineteen unittest cases, bundle validation, Ruff
lint/format and diff whitespace checks passed. The new skill passed Skill
Creator frontmatter/name/completeness validation. These checks do not prove
agent behavior or native discovery. No helper behavior, dependency pins, native
installation or application structure changed in this guidance update.

ty and pre-commit enforcement, expanded strict Ruff rules, utility ownership,
existing-project policy adoption and Cosmic Ray's pinned Python 3.14 synthetic
unittest proof remain outstanding; see ROADMAP.md. Changes remain local.

## Expanded Python hygiene selections — October 9, 2026

The user approved deptry, pip-audit and Import Linter as on-demand additions.
Routine pre-commit selection remains Ruff check/format, ty and unittest; routine
hook enforcement remains unimplemented. Guidance keeps uv as the resolver and
uses a pinned export for pip-audit without dependency resolution or automatic
fixes. No deeper tools were added to hooks, CI or project dependencies.

Focused synthetic Xenon probe: uv-managed CPython 3.14.8, Xenon 0.9.3 and Radon
6.0.1 parsed generic function/type-alias syntax, template strings and match.
The generic function's one if yielded complexity 2; three non-default match
cases yielded complexity 4. A simple source passed all C/C/C ceilings, and a
21-if function was rejected above C. This does not establish complete Python
3.14 syntax or semantic support. It is evidence against treating older release
metadata alone as proof that Xenon cannot work on 3.14. Latest PyPI release
checked: 0.9.3 (October 21, 2024); documented test range still ends at 3.12.
Sources: https://pypi.org/project/xenon/ and https://github.com/rubik/xenon.

The new selections, their full compatibility proofs and remaining tool-policy
questions are tracked in ROADMAP.md. Cosmic Ray compatibility remains unverified.

## Ruff and complexipy replace Xenon — October 9, 2026

The user authorized Python 3.14 evaluation and replacement if suitable, with
on-demand hygiene and the existing routine pre-commit selection unchanged.
Ruff 0.15.18 and complexipy 8.0.1 now form the pinned `hygiene` dependency group.
No runtime dependency was added. C901 is selected only in explicit hygiene
commands; routine Ruff selection and CI were not expanded by this change.

The reproducible skill-local probe passed on uv-managed Python 3.14.8. Generic
functions, type aliases, template strings and match were parsed. Cyclomatic
20 passed and 21 failed; cognitive 15 passed and 21 failed. A six-level nested
fixture measured Ruff 7/complexipy 21, showing why the second metric is useful.
Invalid syntax returned failure. The probe itself meets both ceilings.

Selected ceilings: Ruff cyclomatic 20, retaining the former C rank's numeric
upper boundary, and complexipy cognitive 15, its documented default. Different
counting rules prevent claiming exact Xenon equivalence. Former module and
whole-project cyclomatic averages are retired by this explicit policy change;
complexipy's module-level script analysis is not the old average calculation.

The [saved evaluation and baseline](evidence/2026-10-09-complexity-evaluation.json)
includes versions, source hashes and per-function measurements. Existing source
findings remain failures: configure is 21/57; project_config is 10/28. Tests and
the new probe have no over-limit findings. No app source was refactored, threshold
raised or finding suppressed. Future baseline comparisons must track individual
function identities/scores, not only totals. No automatic ratchet gate was added.

Nineteen unittest cases, bundle validation, routine Ruff lint/format, diff
whitespace and engineering-skill validation passed. These do not mean complexity
is clean. Run the skill's explicit commands for the on-demand findings. The
probe is focused compatibility evidence, not complete Python 3.14 grammar proof.
SP-BP remains an expected addition, deferred and disabled. Changes remain local.

## Latest tool selection supersedes the two-tool policy

The user selected Ruff + complexipy + Lizard and retirement of Xenon/Radon.
Lizard 1.24.1 is pinned in the hygiene group. The earlier receipt remains
historical; the three-tool receipt records Lizard's scores and source averages.
The intended C/C/C approximation, exact counting contract and aggregate gate
remain pending. No routine pre-commit or CI complexity checks were added.
Dependency freshness review is documented on demand; no scheduler was created.
Preferences remain starter-owned, with agnostic SP/gz-skills and expected,
agnostic, deferred SP-BP. No upstream plugin implementation changed.

The [three-tool receipt](evidence/2026-10-09-three-tool-complexity-evaluation.json)
passed on uv-managed Python 3.14.8 with Ruff 0.15.18, complexipy 8.0.1 and
Lizard 1.24.1. Lizard scored the flat boundary fixtures 20 and 21, and discovered
all three modern-syntax fixture functions. Source averages are measurements,
not final aggregate-gate proof. Existing starter source violations remain visible.

## Settled C/C/C implementation — October 9, 2026

This supersedes earlier pending-contract statements. The explicit on-demand
Lizard checker implements `lizard-functions-v1`: function/module/overall
ceilings 20/20/20, nested functions counted independently, no synthetic class
scores, native assertion semantics, undefined empty means, and fail-closed
syntax/discovery errors. Use native Lizard measurements without syntax adapters; unsupported inline
suites fail discovery instead of disappearing from the measurement. Read the Python skill's ccc-contract
reference and run its CLI explicitly. Ruff and complexipy remain independent
checks; routine pre-commit and CI selection are unchanged. SP-BP remains expected,
deferred and disabled. No cob_reports tool configuration or app code changed.
The source-only cob_reports receipt reports 649 functions, maximum 100, overall
mean 7.14946, 42 function and 12 module failures, zero tool errors; this is
verified enforcement with visible legacy debt, not a clean corpus.

Final operator refinement: no Radon/Xenon emulation or source normalization.
Original source and native Lizard scores govern; inline suites missed by Lizard
produce a discovery/tool error. Ten on-demand CLI contract tests, routine Ruff
lint/format, and the nineteen adoption tests pass. Final receipts are
`docs/evidence/2026-10-09-cob-reports-ccc-v1.json` and
`docs/evidence/2026-10-09-starter-ccc-v1.json`; both retain absolute complexity
failures without tool errors. The final approach was shared in gzkit issue #1183.
Changes remain local/uncommitted; no hooks, CI complexity gates or SP-BP changes.

## October 18 Astral alignment migration

See [the scoped migration receipt](evidence/2026-10-18-astral-alignment.md) for
the 0.4.0 package/tool/policy migration, 31 routine adoption tests, eleven
explicit analyzer tests, four passing local hooks, type/lint/format checks,
bundle/catalog validation and isolated installed-artifact verification on
managed Python 3.14.8 / Windows. This supersedes historical current-state
statements above about absent ty/pre-commit enforcement. GitHub-hosted CI and
fresh-session native loading remain separate unobserved proofs.

## October 18 complexity remediation

See [the before/after assessment](evidence/2026-10-18-complexity-remediation.md).
All three on-demand complexity checks now pass across `src tests tools` under
unchanged limits and scoring contracts: Lizard maximum 16 and overall mean
3.306122448979592 across 98 functions, zero violations/tool errors; cognitive
maximum 14. Latest routine verification has 35 adoption tests; explicit analyzer
verification has twelve tests. Historical failures and the earlier alignment
receipt remain intact. Fresh-session host proofs and remote CI remain open.
