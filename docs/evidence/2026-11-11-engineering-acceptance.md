# T12 engineering acceptance — 2026-11-11

T12 resumed from `ee2e86e84af24559b288ece169fac728093c23c8` on the clean primary
`main` checkout, following the [handoff](../handoff.md). This is bounded execution
of the [approved T12 brief](../superpowers/plans/2026-10-28-reference-parity.md#t12-full-affected-input-engineering-acceptance-and-plan-reconciliation).
**Strict G5/E3/E4 and terminal acceptance remain incomplete. T13 is not executed.**
The first unpublished product remains 0.1.0 under [ROADMAP.md](../../ROADMAP.md);
no new capability, public contract change, tag or release is selected here.

## Changes and review

Four project-owned Import Linter forbidden-import contracts now enforce:

- SDK access stays at the MCP boundary. All fourteen non-composition runtime
  modules are checked, including indirect imports, against `mcp`.
- Navigation/diagnostics use the existing Session/Documents seams. Direct raw
  transport, transaction, SDK composition and subprocess imports are forbidden.
  Indirect transport through those seams is intentional; this contract does not
  claim that Session is a newly introduced abstract port.
- Filesystem transactions cannot depend, directly or indirectly, on semantic
  operations, document coordination, MCP or LSP transport/process ownership.
- The edit planner cannot reach transaction or protocol effects, directly or
  indirectly. Its existing Workspace coordinate utility remains usable; this
  import check alone cannot prove absence of arbitrary stdlib filesystem calls.

All four contracts pass and individually reject an injected forbidden import in
an outside-checkout disposable source copy (exit 1 each); restoration returns
four kept/zero broken (exit 0). No ignores or weakened ceilings were introduced.

The five existing Lizard violations were corrected by extracting existing
responsibilities: snapshot identity/version validation, journal-plan binding,
raw symbol/diagnostic argument validation, ty pattern/environment validation,
and fake-peer initialization. The independent stage reviewer found no concrete
defect or material contract gap. Review traced duplicate/identity/version error
precedence, journal validation order, strict bool/int predicates and early
configuration/applyEdit/initialize sequencing. This is the bounded T12 diff
review, separate from T13's whole-milestone review.

## Deeper findings

Scopes are the actual `src`, meaningful `tests`, and inherited `tools/engineering`
where specified; none is a published-starter measurement. Raw command output,
coverage data, native transcripts and disposable probe scripts remain ignored
under `.superpowers/sdd/2026-10-28-reference-parity/t12/`.

| Check | Observed result / scope |
| --- | --- |
| Ruff C901 | PASS: `src tests tools/engineering`, ceiling 20 |
| Lizard 1.26.0 | PASS: same scopes; 648 functions, maximum 20, weighted mean 3.1944444444444446, no discovery error; all function/module/project ceilings 20 |
| Analyzer utilities | PASS: 29 unittest regressions, including fail-closed cognitive consumer controls; these do not qualify an engine |
| Import Linter 2.16 | PASS: four contracts and four failing injected controls |
| deptry 0.25.1 | PASS: 18 runtime files; no missing/unused/transitive dependency issue |
| pip-audit 2.10.1 | PASS: exact hashed all-group uv export, no known vulnerabilities; package count in JSON receipt |
| Bandit 1.9.4 | Nine LOW findings, reviewed below; no higher severity |
| cohesion 1.2.0 | Measured all runtime classes; responsibility review below; no invented score floor |
| Interrogate 1.7.0 | Presence measurement and review below; no new coverage floor selected |
| Vulture 2.16 | Candidates reviewed below; no deletion or blanket whitelist |
| Cognitive ≤15 | UNKNOWN: no installed, independently qualified shared engine; complexipy cannot supply passing authority |

Bandit's eight assertions are internal narrowing/invariant checks, not the
only checks on untrusted data: diagnostics validates a report before related
processing; transaction authority rejects absent state before opening it;
transport failure sets its error before signalling; mutation middleware validates
the tagged fields before tool dispatch. The subprocess import belongs to the
one-child session adapter with an explicit executable and argument vector, no
shell. Retain the visible LOW findings without `nosec` or changing severity.
This review does not assert absence of other security defects.

Cohesion's zero scores on Config/Limits, Snapshot/identity, contexts, cached
reports and plan values reflect immutable data carriers. Async service methods
are incompletely represented by this metric (for example Documents, Diagnostics,
Session and Mutations); their percentages cannot establish poor cohesion or
async design correctness. Transactions owns one recovery/commit state machine,
RpcClient one framed connection, Documents one generation/admission coordinator.
These responsibilities justify retaining the classes; no score-driven split.

Vulture's runtime mutation tool functions are SDK decorator registrations,
exercised by catalog and installed mutation tests. The additional src+tests
candidates are synthetic semantic fixture declarations/call-result bindings,
unittest `asyncTearDown`, and SDK-decorated contract fixtures. They are intentional
external consumers/test inputs, not deletion candidates. Interrogate measures
presence, not correctness: public module/tool/contract docstrings describe the
saved-file, UTF-16 and recovery boundaries, while many internal adapter methods
lack docstrings. Record that maintenance debt; no tool-default threshold becomes
a project gate and no filler docstrings are added solely for a score.

## Cognitive external condition

Rechecked starter [issue #1](https://github.com/tvproductions/gz-skills-first-starter/issues/1):
OPEN, unscheduled. Current gzkit `src/gzkit/complexity/cognitive.py` has changed
from historical evidence (blob `ff28e8ad83c5a68ed748a2de39296b21b45579a9` at
inspection), but the repository still packages the whole `py-gzkit` application.
No separately versioned shared engine was found in that source/package boundary.
This is a bounded observation, not proof that no candidate exists elsewhere.
Do not install the whole lifecycle or create a private scorer to replace missing
qualification. Owner: project/starter maintainer, dependent on gzkit's shared
engine delivery. Revisit when an immutable engine distribution/API is available;
then install, independently qualify with all 42 fixtures and measure the actual
corpus at ceiling 15. E3/E4 and G5 remain unaccepted until then.

## Coverage and bounded product mutation

Coverage 7.17.2 executed the existing 186-test suite on final runtime/ty inputs
(exit 0, one Windows-only skip), then appended the three new result tests.
It measures 2,371/2,720 statements (**87.1691%**) and 737/990 branches
(**74.4444%**), combined **83.7736%**, with zero excluded lines. This is parent
process coverage: clean installed CLI children and crash subprocesses are
functionally asserted but not instrumented by this run. Consequently CLI and
`__main__` show zero measured coverage; this does not mean they were unexecuted.
Consequence-sensitive gaps remain in malformed diagnostic/related-report paths,
planner metadata/limit denials, configuration exclusions, and exceptional POSIX
recovery/syscall failures. Existing fault/crash tests cover important members of
those classes, but this measurement does not prove every branch. No inherited
coverage percentage was adopted as a gate.

Cosmic Ray 8.9.0 mutated the actual `results.py` in a disposable source copy,
verified import origin and exact source restoration. The bounded scope has
13 mutants; baseline unittest passes. The initial diagnostics/navigation/symbol
suite killed eight and left five: `>` changed to `==`, `>=`, or `is`, ASCII
escaping enabled, and nonfinite JSON enabled. These are contract-test gaps.
Three focused tests now independently assert inclusive budget equality and
oversize rejection, actual Unicode JSON byte length, and NaN/infinity rejection.
The final probe adds `tests.test_results` to that same suite: **13 killed,
zero survived, zero timeout/tool-error/pending**. This supplies real negative
controls for the new tests; no runtime change was needed. This bounded result
is not a whole-product mutation score. Exact mutant identities are in the JSON
receipt; all source bytes were restored and checkout source was never mutated.

## Current host evidence

Actual codex-cli **0.167.1**, default model **gpt-6.1-sol**, macOS arm64, installed
runtime-only adapter outside the checkout, managed Python **3.14.10**, official
MCP **2.3.0**, and pinned ty **0.0.101** were exercised through stdio app-server.
The host profile is ephemeral; native/user configuration and caches remain intact.
Official [app-server documentation](https://learn.chatgpt.com/docs/app-server#mcp-server-elicitation-requests)
and generated 0.167.1 schemas define the protocol used by the probe.

A fresh actual model turn invokes all seven reads with caller-supplied exact
positions, waiting sequentially for each response. Independent fixture assertions
check complete shared declaration source/identifier range, three exact package
call sites and no decoy, hover text, clean diagnostics, document symbol identity,
two ambiguous workspace symbols, and member implementations at lines 4/9/14.
Both disabled mutation tools return MUTATIONS_DISABLED with recursive file
hashes unchanged. A second operator-enabled ephemeral thread previews/applies
rename and edit. Native approval decisions are accept/decline/accept/accept/accept;
the declined apply leaves every file unchanged. Accepted writes match the complete
expected file-byte map; fresh definition source contains the new identifier and
edited expression. These are programmatic actual-host decisions, not GUI or
human-click evidence, and preview plan identity is not authenticated consent.
Normal unsubscribe/EOF returns app-server exit 0; user configuration hash is
unchanged. Fault/timeout evidence is recorded separately in the JSON receipt.

Two private probe corrections remain visible in the raw evidence: an initial
turn started before MCP startup finished and invoked no tools; a parallel trial
returned one honest ty `-32801` error and queried incorrect invented fixture
coordinates for two tools. Those trials are not passing semantic evidence. The
passing trial waits on actual host inventory and uses independently checked
fixture positions sequentially; it adds no adapter replay or readiness sleep.

## Acceptance traceability

The following records observed evidence for each required row. Fresh local
unit/installed results are distinct from native and hosted platform evidence.
All references are tracked synthetic fixtures and named unittest modules.
The synchronization response owns the exact final candidate's three-platform CI;
prior commit CI does not certify these refactors. G5 remains incomplete even
when routine checks pass because cognitive qualification is required.

| Row | Observed evidence and boundary |
| --- | --- |
| P1 | `test_source_text`, `test_navigation`, `integration.test_navigation`, installed full-read test; complete declarations/range distinction/external source checks; native shared declaration assertion |
| P2 | Navigation unit/direct-ty/installed comparison and exact expected calls/imports; native three-package call-site assertion |
| P3 | `test_diagnostics`, `integration.test_diagnostics`; full/unchanged/repair/dependency/related identities; native current clean report |
| P4 | Navigation hover variants, exact/Unicode input checks and installed hover; native original signature text |
| P5 | `test_edit_plan`, `test_mutations`, installed mutation/recovery tests; native zero-write preview, denied apply, exact rename and fresh semantics |
| P6 | Planner byte/overlap/newline/UTF-16 controls and installed edit tests; native exact edit byte map |
| S1 | `test_forwarded_position_is_exact`, direct-ty/installed consumer queries, native exact identifier arguments; no full-range inference |
| S2 | `test_symbols` hierarchy/flat/limits/catalog and installed symbols; native document symbol assertion |
| S3 | Symbol duplicate/URI-only/resolve/empty-workspace/generation tests and installed search; native ambiguity assertion |
| S4 | Supported/empty/unsupported implementation tests, installed actual ty override fixture, native exact member locations |
| S5 | P4's real hover text retained; no parsed machine-type API |
| S6 | Diagnostic dependency/repair tests, mutation commit/sync-failure tests and native post-write definition source |
| C1 | SDK contract, MCP composition, installed stdio catalog/schema/error/cancellation tests; native all-nine-tool use |
| C2 | Eleven transport tests cover Unicode framing, malformed lengths/JSON/IDs, concurrent writers/replies, admission and callback failure |
| C3 | Session early requests/initialize-once/applyEdit-denied tests and Documents negotiated synchronization tests |
| C4 | Transport timeout/cancel/EOF tests, session startup/death cleanup, cancelled commit/recovery tests; current native faults separately recorded |
| C5 | Session timeout/stderr/reap/idempotency tests, generation reaping, installed EOF/startup recovery; current native faults separately recorded |
| D1 | `test_documents` open/change/close, workspace lease, single-slot document read, drain/exclusion/cancellation and manifest ownership tests |
| D2 | Documents two-reader/stale/restart tests; installed unopened-file/config/new/deleted/renamed scope tests |
| D3 | Workspace URI/UTF-16/alias/symlink/nonregular tests, source extraction AST mapping, planner and filesystem identity denials |
| W1 | Disabled/claimed-approval/stale/expiry tests and native disabled/declined apply hash checks |
| W2 | Pure whole-edit/resource/version/alias denials and untrusted rename target-set test |
| W3 | Planner overlap/adjacency/coincident insertion, strict positions, UTF-16 and stage limits |
| W4 | Filesystem parent/target identity, symlink/hardlink and state-lock tests; mutation read-drain/timeout/exclusion tests; claimed POSIX lanes only |
| W5 | Replace-index fault/rollback tests, external-conflict lockout and installed recovery fixtures |
| W6 | Crash-transition subprocess tests, installed lifespan startup restore/conflict/corrupt/disabled controls; Windows unsupported control is not POSIX recovery evidence |
| W7 | Lost-response/replay/expiry/restart durable receipt tests through installed CLI |
| W8 | Exact bytes/modes and sync-failure distinction tests; native renamed/edited fresh declaration source |
| H1 | Fresh macOS actual model/installed adapter semantic assertions on current inputs above |
| H2 | Fresh native actual-host preview/deny/accept, complete byte maps and disabled denials above; programmatic approval boundary retained |
| H3 | Current native timeout/death/EOF receipt plus retained T11 historical host evidence; no SDK proof substituted |
| E1 | Managed interpreter/tool provenance, locked all-group sync, four unchanged hooks; final exact-commit CI reported with synchronization |
| E2 | Source-independent sdist→wheel, outside-source distribution verification and runtime-only installed stdio scenarios |
| E3 | Measured deeper tools and reviewed findings above; **UNKNOWN** qualified cognitive; strict engineering acceptance incomplete |
| E4 | Current execution-host discovery plus November 11 configured-source reconciliation; cognitive **UNKNOWN**; overall required row remains incomplete |
| E5 | Existing license/attribution and public synthetic fixtures retained; local macOS POSIX proof, exact-commit hosted Linux/macOS/Windows gate and skip inventory remain separate observations |
| STOP | NOT RUN; T13 is outside this bounded session and G5 remains incomplete |

Current native fault probes each establish a real installed adapter/ty connection
in an ephemeral host thread, then kill ty, kill the adapter, suspend ty to trigger
the host's 2-second tool timeout, or close parent stdin. All four preserve recursive
workspace hashes, reap both observed adapter/ty PIDs, and exit app-server 0.
No dead request was replayed. This adds current-runtime H3 evidence rather than
reusing T11's older runtime selections. Private processes/paths are not published.

Interrogate's final presence measurement is **119/284 (41.9%)** runtime objects;
165 lack docstrings. Its explicit `--fail-under 0` is measurement-only, not a new
project threshold or a claim to pass the tool's default 80% floor. That default
would fail. Raw LOW Bandit candidates and reviewed Vulture candidates remain
visible; analysis success is not the same conclusion as zero raw findings.

The first full hook invocation overlapped runtime editing and failed two installed
mutation cases after 581.610 seconds: edit apply returned PROTOCOL_ERROR and
restart receipt replay returned RECOVERY_REQUIRED. That moving-input run is not
final-candidate acceptance and is retained rather than relabeled a pass. Both
cases passed unchanged in a focused 23.458-second rerun and in the later complete
coverage execution. No root cause is claimed solely from high system load or
this timing correlation; no timeout, assertion or recovery guard was weakened.
The settled-tree final gate is recorded separately.

## Astral and execution reconciliation

| Acceptance | Evidence / conclusion |
| --- | --- |
| A01 | Base commit, bounded T12 scope and unchanged 0.1.0 release target above; rollback via ordinary Git reversal, no external data migration |
| A02–A03 | Existing src packaging, uv_build 0.13.7, console entry point and outside-source installed origin checks |
| A04–A05 | Central pyproject configuration; managed CPython 3.14.10 arm64, Ruff py314 and ty 3.14, no application environment overrides added |
| A06 | November 11 maintenance owns freshness; this stage retains its pins rather than inferring freshness from a lock |
| A07–A08 | Supported uv 0.13.6, locked all-group sync, exact installed package versions and unchanged routine tool selection |
| A09 | Four routine hooks retained; 189 tests pass with one Windows-only skip; normal commit and exact-commit CI must still pass on settled inputs |
| A10 | Runtime dependency remains official mcp 2.3.0; no declaration/lock change; wheel metadata independently checked |
| A11–A13 | Source-independent sdist-to-wheel and outside-source installed import/entry point/typing/inventory tests; installed CLI functional suites separate from packaging |
| A14–A16 | N/A: single package, no uv workspace/private source/native extension/container deployment |
| A17 | Hashed locked all-group export consumed only by pip-audit, 99 exact packages, no skips/advisories |
| A18 | Reviewed deeper findings/coverage above; cognitive UNKNOWN with named owner/external condition; native host proof separate |

Intent-to-scope and scope-to-plan comparison: the approved nine-tool scope and
write boundary are retained; T12 adds only engineering contracts, bounded
refactoring, tests and evidence. No new capability, schema or runtime dependency
is introduced. The specified engineering measurements and per-row reconciliation
are observed; cognitive closure is **Missing**, so G5 is not PASS. T13 remains
out of scope. The T12 task helper could not parse the approved `T12` heading
because it requires `Task 12`; its brief was extracted manually without rewriting
the approved plan. Execution followed the handoff's primary-main instruction.

Fresh native discovery observes 20 unique project gz-skills 0.10.1 entries and
zero errors. `codex plugin marketplace upgrade skills-first-starter --json`
selects only the project marketplace and returns zero errors/no changed roots.
The global app-server marketplace API did not recognize the project-only Git
entry; the project-scoped native CLI supplied the successful refresh. Existing
November 11 full-source/native-ref reconciliation remains its separate receipt.

The settled-runtime 189-test hook run passed all tests (428.759 seconds), but
pre-commit correctly rejected the invocation because documentation was edited
while it ran. This is not an aggregate PASS. Finish all edits before the normal
commit hook rerun; the final response records that settled-tree result and
exact-commit CI without a receipt-only follow-up commit.
