# Parity, semantic and interoperability acceptance gates

Design revision 2, 2026-10-28. **Execution is partial; the full milestone is NOT ACCEPTED.**
Prerequisite wording reconciled 2026-11-01 against the
[October 31 update receipt](../evidence/2026-10-31-dependency-update.md);
no runtime row or human decision is accepted by this correction.
Execution details corrected 2026-11-01 in the
[targeted plan audit](../evidence/2026-11-01-plan-execution-corrections.md):
T4 supplies production hover/early host feasibility, generation coordination and
platform lanes; full capability and host acceptance remain required.
The [second-review correction audit](../evidence/2026-11-01-plan-second-review-corrections.md)
assigns production startup recovery, workspace-wide generation leases and T0's
dependency-policy negative control. These are future checks, not accepted results.
Implementation was approved on 2026-11-01. This matrix defines required evidence;
all unexecuted runtime rows remain NOT RUN. T4 supplies partial G1 evidence on
Windows/Linux and the early Codex checkpoint; full P4/H1-H3 and macOS remain
unaccepted. See [T4 evidence](../evidence/2026-11-01-documents-hover.md) and the
[host receipt](../evidence/2026-11-01-codex-feasibility.md).
T5 adds local Windows/Linux P1/P2/P4/S1/S5 development evidence in the
[navigation receipt](../evidence/2026-11-01-navigation.md). Cross-platform/native
host completion and all later capabilities remain gated.
T6 adds local Windows/Linux P3/S6 diagnostic development evidence in the
[pull-diagnostic receipt](../evidence/2026-11-01-diagnostics.md); full native and
platform acceptance remains incomplete.
The [specification](../superpowers/specs/2026-10-28-semantic-navigation-design.md)
and [plan](../superpowers/plans/2026-10-28-reference-parity.md) are approved for execution.

For every future row retain: project commit, immutable fixture identity, Python/SDK/
ty/host versions, command or native session, expected and observed results, exit
code, source hashes and redacted artifacts. PASS requires observed assertions;
FAIL/UNKNOWN/required skips prevent acceptance. Mock, real-ty, installed-distribution
and Codex-host receipts are separate. Upstream source inspection is not a Python PASS.

## Reference parity and semantic correction

| ID | Observable assertions | Boundary / planned owner task |
| --- | --- | --- |
| P1 | Imported call resolves correct shared declaration; complete function/class/constant source, nested/decorated/async/multiline cases; full and identifier ranges distinct; empty result and explicit external/unavailable source; decoy never selected | Unit extraction + actual ty + MCP; T5 |
| P2 | Three expected cross-package call sites and independently listed imports; include_declaration both ways; same-name decoys absent; stable ordering and context; direct ty and adapter normalized locations agree | Actual ty + MCP; T5 |
| P3 | Error diagnostics with exact URI/range/severity/code/message; repair yields fresh empty full result; unchanged resultId only with same generation/cache; dependency edit changes consumer diagnostics; no pull result discarded, no sleep/push-empty shortcut | Fake reports + actual ty + MCP; T6 |
| P4 | Hover kind/content/range and type/signature text preserved; MarkedString/MarkupContent/list/null normalization; invalid/Unicode inputs rejected or mapped correctly | Production path at T4; full unit + actual ty + MCP acceptance at T5 |
| P5 | Preview writes zero bytes; approved apply changes shared definition/imports/calls across files and excludes decoys; changes/documentChanges/versioned edits handled; prepareRename supported/error/unsupported; replay and zero-occurrence/no-op truthful | Planner/filesystem fault tests + actual ty + MCP; T7–T9 |
| P6 | Exact replacement, multiline insertion/deletion, zero-length insertion, EOF append, full file deletion; UTF-16/non-BMP/CRLF/mixed newline/trailing newline/no trailing newline; same-result text no_op; invalid/overlap/stale/outside targets change zero bytes | Pure tests + real filesystem + MCP, then semantic freshness; T7–T9 |
| S1 | Transport spy records the exact caller identifier position, never declaration start or a hard-coded offset; real fixture identifier query resolves consumer calls while unrelated same-name queries do not; record keyword control independently | Unit + direct ty + adapter + Codex; T5/T11 |
| S2 | document_symbols returns nested hierarchy, distinct selectionRange/full range, flat form without invented selection; result limits/unsupported methods explicit | Fake variants + actual ty + Codex; T10/T11 |
| S3 | workspace_symbols search retains duplicate names; URI-only/unresolved result honest; resolve capability honored; caller explicitly selects location before follow-up semantic query; empty workspace needs no invented document URI/didOpen, search and resolve share one generation lease and discard results on change | Workspace lease T4; fake variants + actual ty + Codex T10/T11 |
| S4 | implementations resolves subclass/member override fixtures; empty/unsupported distinct; no code-lens/execute-command tool accidentally exposed | Actual ty + MCP + Codex; T10/T11 |
| S5 | Type info conveyed through real hover data; no guessed machine type derived by parsing markdown | P4 actual ty/host evidence; T5/T11 |
| S6 | Diagnostics and post-write semantics describe current generation; no unsafe partial-success or silent mutation | P3, W1–W8, D1–D3; T6–T9 |

## Protocol, workspace and lifecycle

| ID | Required evidence | Task |
| --- | --- | --- |
| C1 | SDK initialize/protocol version negotiation, tools/list schemas/annotations, tools/call success/error, cancellation and stdout purity; first production hover at T4, nine final tool names, no extra executor tools | T3/T4/T9/T10/T11 |
| C2 | Byte counts with non-ASCII; fragmented/coalesced frames; missing/duplicate/negative/oversized lengths, invalid JSON/IDs, simultaneous writers, out-of-order replies, unknown/late IDs; bounded memory/admission | T2 |
| C3 | Callbacks active before initialize; initialized exactly once; UTF-16 and text sync/diagnostic capabilities matched; workspace/configuration cardinality; unsolicited applyEdit always rejected | T3/T4 |
| C4 | Timeout/cancel really unblocks waiter; late response safe; EOF/child death fails all pending calls; no mutation replay; startup failure no child leak | T2/T3/T8 |
| C5 | Parent EOF/signals, duplicate cleanup, shutdown timeout, stderr flood, terminate/kill/reap and generation restart keep ≤1 live ty; active commit protected or recovered | T3/T8/T11 |
| D1 | didOpen once/version 1, negotiated change versioning/ranges, didClose eviction/shutdown; before/after generation checks; snapshots same bytes as semantic coordinates; workspace leases need no document and document reads consume one shared slot; contexts pin one generation/client, invalidated waiters drain before restart, read admission and commit exclude each other with bounded waits and no leaks | T4/T9/T10 |
| D2 | Real ty query after unopened consumer change/create/delete/rename and project-config change reflects fresh disk after rescan/restart; no indexed-ready sleeps; two readers across a change/restart cannot publish old-generation success, hang or start a second live child; change during request yields STALE_DOCUMENT | T4/T5/T6/T11 |
| D3 | URI spaces/Unicode/percent aliases, containment by components, traversal/remote authority/NUL/query/fragment denial, symlink/hardlink policies, nonregular inputs, unknown external outputs metadata-only; Python AST byte-column versus UTF-16 mapping | T1/T4/T5/T8 |

## Mutations and recovery

| ID | Required evidence | Task |
| --- | --- | --- |
| W1 | Disabled mutations, missing/expired/wrong workspace/session token, changed policy and denied host approval all cause zero target writes; preview always zero writes; annotations conservative even for preview | T7/T9/T11 |
| W2 | Entire WorkspaceEdit validated before staging/commit; one denied/external/resource-op/version-conflicting target rejects all; no duplicated URI aliases or unsupported edit shape applied | T7/T9 |
| W3 | Overlap and coincident inserts rejected, adjacent edits legal; fractional/bool positions invalid; UTF-16 surrogate split cannot corrupt bytes; stage count/size caps fail before write | T1/T7 |
| W4 | Parent/target replaced by symlink, hardlink, identity or mode change between preview and commit is denied; directory-relative no-follow operations on each claimed write platform; state lock excludes adapter concurrent commits; active reads drain before preflight, timeout writes nothing, no restart or new reads during commit | T8/T9 |
| W5 | Inject failure before first replace → unchanged; after replace N → all before-images restored and verified; restore failure/external content conflict → RECOVERY_REQUIRED with per-file truthful status and mutation lockout | T8 |
| W6 | Subprocess crash at every journal/replace/receipt boundary; installed CLI's production lifespan invokes recovery before mutation admission, pending recovery admits none, corrupt/conflicting state locks real preview/apply with RECOVERY_REQUIRED; disabled/unsupported startup never restores source; no automatic reapply; recovery artifacts private, local and source-free in logs | T8 recovery engine; T9 production lifespan/installed stdio proof |
| W7 | Lost commit response/retry returns durable committed receipt without applying twice, including across server restart; expired previews remain distinguishable from retained receipts | T8/T9 |
| W8 | Exact verified after-bytes/modes, durable receipt and LSP sync/invalidation before claiming committed; sync failure does not claim rollback of already committed files; subsequent reads fail or start fresh session | T8/T9/T11 |

Cross-file atomicity against crashes/external readers is **not claimed**. The accepted
boundary must be reviewed: no target write on validation failure; ordinary failures
restore or explicitly require recovery; noncooperating external writers are not
silently overwritten. If this boundary is rejected, W5/W6 cannot pass by relabeling
partial application as success: redesign precedes implementation.

## Host and engineering acceptance

| ID | Required evidence | Task |
| --- | --- | --- |
| H1 | Fresh Codex session discovers actual installed Python adapter, invokes every read tool through actual ty, returns semantically asserted JSON; record executable origin and launch command, not just tools/list; early installed hover feasibility is prerequisite evidence only | Early T4 checkpoint; full T11 acceptance |
| H2 | Disposable write-authorized Codex workspace: rename/edit preview then host-approved apply changes exact expected files; denied invocation leaves hashes unchanged; operator-disabled config cannot be bypassed; early hover approval/denial proves only host interaction availability | Early T4 feasibility; full mutation evidence at T11 |
| H3 | Host timeout/adapter failure/ty death/EOF close processes; no orphan; actual host transcript and resulting bytes captured/redacted; noninteractive SDK integration cannot substitute for Codex host proof | T11 |
| E1 | CPython 3.14.10/tool pins and lock match effective local/hooks/CI; Ruff check/format, ty and unittest all pass, no pytest or extra hygiene hooks | T0–T12 |
| E2 | uv build --no-sources sdist→wheel, inventories/notices/typing/entry point/dependency metadata; outside-source clean runtime env imports installed package and runs actual stdio scenarios, no dev dependency masking | T0/T11 |
| E3 | Applicable C901 (20), qualified cognitive (15), Lizard (20 function/module/overall), cohesion, Interrogate, Vulture, Bandit, statement/branch coverage, bounded Cosmic Ray, deptry, pip-audit and Import Linter; reviewed findings/scopes and no imported score floors | T12 |
| E4 | Verify recorded gz-skills 0.8.3 reconciliation: source/catalog/provenance, configured Git-source refresh and execution-host native discovery agree through proper workflows; cognitive engine installed and independently qualified or strict acceptance remains incomplete | T0/T12 |
| E5 | License/dependency review and Isaac Phi attribution retained; public synthetic fixtures only; Linux x86_64/macOS arm64 write evidence separate, Windows x86_64 reads and unsupported-write rejection measured; inventory platform skips, no missing ty/required POSIX safety test skipped as acceptance, unsupported Windows writes disabled | T0/T4/T8/T11/T12 |
| STOP | All P/S/C/D/W/H/E required rows accepted, material decisions closed, evidence linked, no required skipped/unknown gate; record terminal milestone and stop with no release/additional server/capability work | T13 |

T0 observed SDK compatibility and packaging evidence in the
[runtime-input record](../evidence/2026-11-01-runtime-inputs.md). These do not pass
semantic/host rows. Current Windows native discovery has duplicate/global scope
FAIL despite matching source bytes; E4 remains incomplete.

Current engineering evidence from initialization is historical scaffold evidence.
This design change does not convert it into runtime acceptance. Cognitive qualification
remains unresolved under the recorded evidence. gz-skills reconciliation was completed
in the October 31 update; execution-host verification and configured Git-source refresh
evidence remain required at T0/T12. Prior-host discovery does not certify another host.
These work packages have explicit closure requirements and are not indefinite removals
from the milestone.


## November 11 current-input reconciliation

The [T12 receipt](../evidence/2026-11-11-engineering-acceptance.md#acceptance-traceability)
maps every row above to current unit/installed/native observations and preserves
platform exclusions, tool findings and evidence limits. November 11 maintenance
supersedes the historical duplicate/global native-discovery finding above for
this execution host; current native behavior is independently remeasured.
G5/E3/E4 remain incomplete because qualified cognitive scoring is unavailable.
STOP/T13 remains NOT RUN; row coverage alone is not terminal acceptance.
