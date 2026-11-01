# Reference Parity and ty Semantic Navigation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver accepted six-tool functional reference parity, corrected semantic targeting, the three specified ty navigation extensions and actual Codex interoperability, then stop.

**Architecture:** Official MCP Python SDK stdio adapter over narrow semantic operations, document/workspace identity, independent JSON-RPC transport and a single ty lifecycle owner. Rename and edit share pure planning and a guarded filesystem/recovery boundary; no general LSP framework.

**Tech Stack:** Managed CPython 3.14.10, uv/uv_build 0.13.6, Ruff 0.17.3, ty 0.0.95, pre-commit 4.7.0, unittest; proposed runtime mcp 2.3.0 and stdlib.

Prerequisites reconciled 2026-11-01 against the
[October 31 update receipt](../../evidence/2026-10-31-dependency-update.md).
Functional design, task completion state and pending approval are unchanged.
Execution details corrected 2026-11-01: production hover at T4, explicit generation
coordination, platform verification lanes and early Codex feasibility. See the
[targeted correction audit](../../evidence/2026-11-01-plan-execution-corrections.md).
Second-review corrections assign production startup recovery, separate workspace
generation leases from document snapshots, and order T0's negative control before
guard/dependency changes. See the [second-review audit](../../evidence/2026-11-01-plan-second-review-corrections.md).

**Spec:** [Revision 2 specification](../specs/2026-10-28-semantic-navigation-design.md), [pinned parity matrix](../../discovery/reference-parity.md), [acceptance matrix](../../discovery/acceptance-matrix.md).

**STATUS: APPROVED FOR EXECUTION on 2026-11-01. T0 runtime-input work is complete with named acceptance gaps; T1 is complete; T2 is complete; T3 is complete; T4 implementation/early host checkpoint is verified with named platform gaps; T5 is complete; T6 is complete; T7 is complete; execution stops at this stage boundary. T8-T13 are pending.**
Approval: the user stated "plan is approved, proceed" after review of this plan and
its linked specification. Execute the stated contracts; required evidence and
strict acceptance are not waived. See [execution evidence](../../evidence/2026-11-01-execution.md).
The earlier planning-only boundary is superseded by that approval. Historical
review/audit receipts retain their original observations. Execution uses the
approved behavioral schemas, guarded recoverable writes, rescan/restart consistency
and OS boundary; runtime and engineering acceptance require observed evidence.

## Global Constraints

- Python 3.14 family, selected managed CPython 3.14.10; uv/uv_build 0.13.6, Ruff 0.17.3, ty 0.0.95, pre-commit 4.7.0, unittest, src packaging and project lock.
- Official MCP SDK candidate mcp 2.3.0 (`2118f14f8a19bc158d8a1cf90af58d85d187f849`); ty candidate 0.0.95 matches pyproject.toml/uv.lock. T0 records its source revision and executable provenance; the former 0.0.93 SHA does not identify this candidate. Test/review these inputs; do not float latest during tests.
- Go baseline v0.1.1 (`46e2950b7969334780675e7797e13f140d2d42ac`), assessed main `e4395849a52e18555361abab60a060802c06bf50`; independent implementation, no copied source/tests/media.
- One canonical workspace, one live ty process, MCP/LSP stdio only, saved-disk inputs. No second server, install during requests, code actions, execute command, listener or framework.
- No Makefile or environment-variable application configuration. Application JSON; preserve native host formats and selected lite profile/disabled Backplane.
- UTF-16 code-unit zero-based positions and end-exclusive ranges. Exact caller positions, no workspace-symbol-range-start or fixed-column inference.
- All P1–P6 and S1–S6 are required; final catalog is six reference names plus document_symbols, workspace_symbols, implementations. No silent removal or indefinite deferral.
- Mutations disabled by default, explicit operator writable roots, preview/apply, bounded preflight and recovery. No portable atomic multi-file filesystem transaction is claimed.
- Required FAIL/UNKNOWN/stale acceptance evidence blocks the terminal milestone; cognitive qualification and execution-host verification of the completed gz-skills reconciliation are not waived.
- Initial claimed write platforms: macOS arm64 and Linux x86_64 local filesystems; unsupported Windows writes disabled until equivalent safety proof.
- Routine hook set remains Ruff check/format, ty and unittest; deeper analyses stay outside routine hooks/CI. No tag/release publication.

## Platform verification lanes

T4 establishes Linux x86_64, macOS arm64 and Windows x86_64 verification lanes in
the existing workflow, using the same exact tool/interpreter selections and four-hook gate.
Record actual OS, architecture and filesystem; a runner label alone is not proof.
T8 adds real guarded filesystem/crash tests to both lanes as they are introduced.
Both supported write lanes must pass their required tests before write acceptance.

Windows runs portable unit/protocol/coordinate tests, actual ty read integrations
and explicit unsupported-write rejection tests. Only tests requiring the POSIX
write adapter may use a narrowly scoped platform skip; label them not applicable
to the proposed Windows write scope, never as passed write evidence. Missing ty,
failed setup or missing safety features on a claimed POSIX write platform must
fail rather than skip. T12 inventories skips per lane and keeps any unavailable
required platform evidence UNKNOWN. No Windows write support is added.

## Review Focus

1. Unopened dependency changes/config changes between calls must invalidate/restart ty, and changes during a query must discard stale results — T4/T5/T6 tests.
2. Percent-encoded aliases, symlinked parents and hardlinks must never bypass write containment or duplicate-target checks — T1/T7/T8 tests.
3. Cancellation or process death at the commit/receipt boundary must produce durable exactly-once outcome or explicit recovery, never an apparent empty success — T8/T9 tests.
4. Emoji before a target, CRLF/mixed newline and AST UTF-8 offsets must not shift semantic positions or corrupt replacement bytes — T1/T5/T7 tests.
5. Host approval denial and a model's claimed approval must leave targets unchanged; early Codex feasibility at T4 and full real mutation calls at T9/T11 prevent SDK-only acceptance.

---

## File map and common contracts

These are proposed paths; no runtime file exists besides the empty package initializer.
Use functions/dataclasses, no service container. Separate a module only when its
responsibility below earns the boundary.

| Files to create | Responsibility |
| --- | --- |
| src/gz_mcp_lsp/models.py, config.py, workspace.py | Shared value types, JSON settings, identity/position conversions and bounded manifest |
| src/gz_mcp_lsp/lsp_transport.py, session.py, documents.py | Wire requests, one process lifecycle/capabilities, document synchronization/generations |
| src/gz_mcp_lsp/navigation.py, source_text.py, diagnostics.py | Semantic mapping, bounded complete declaration/context extraction and diagnostic reports |
| src/gz_mcp_lsp/edit_plan.py, filesystem.py, mutations.py | Pure plans, durable guarded transaction/recovery, rename/edit orchestration |
| src/gz_mcp_lsp/mcp_api.py, cli.py, __main__.py | Official SDK registration and composition/JSON CLI |
| tests/test_*.py, tests/integration/__init__.py, tests/integration/test_*.py | Meaningful unit/failure tests and required real-ty integrations |
| tests/fixtures/semantic_workspace/**, tests/fixtures/edit_cases.json, tests/support/fake_lsp.py | Independently invented fixture relationships, byte cases and failure-controlled subprocess |
| docs/evidence/<execution-date>-<task>.json or .md | Actual per-revision evidence, never prefilled PASS results |

`models.py` defines recursive `Json` (JSON scalar/list/string-keyed map),
`Position(line:int,character:int)`, `Range(start:Position,end:Position)`,
`TextEdit(range:Range,new_text:str)`, `FileIdentity(device:int,inode:int,mode:int,links:int)`,
`Snapshot(uri:str,data:bytes,sha256:str,version:int,identity:FileIdentity)`, and
`AdapterError(code:str,message:str,retryable:bool=False,details:dict[str,Json]|None=None)`.
`Result` is `dict[str,Json]` satisfying the specification envelope; `TransactionReceipt` is a raw JSON record with plan_id/status/files, not a separate
framework. Use one error vocabulary from the spec, no silent exception-to-empty conversions.
Configuration is immutable `Config` exposing workspace_root, ty_executable,
state_directory, writable_roots, mutations_enabled and limits. Paths are pathlib.Path.
JSON policy keys and integer limits are validated in T1; optional request values
are checked without bool-as-int coercion.

SDK wrappers expose flat action-tagged mutation arguments. `action="preview"`
requires preview fields and forbids plan_id; `action="apply"` requires only plan_id.
Never accept a caller-provided approval boolean. SDK-generated schemas and these
cross-field checks must be tested, not assumed. No direct Pydantic dependency is
planned; if SDK-native dataclass schema support proves insufficient, bring the
specific need and dependency declaration back to review rather than substituting.

Each task follows red → minimal implementation → green/refactor → repository gate
→ reviewed local commit. Commit only that task's paths; no push, publication or
next phase acceptance implied by an individual commit. Commands below are future
commands, run only after human approval; expected red outcomes refer to missing
behavior, not environment/setup failure.

## Phase 0 — acceptance prerequisites

### T0: Close setup/version prerequisites and establish runtime test contract

**Files:** modify pyproject.toml, uv.lock, tools/verify_distribution.py,
tests/test_distribution.py, README.md; add tests/integration/__init__.py and
`docs/evidence/<date>-runtime-inputs.md`. gz-skills reconciliation is already
recorded in the October 31 receipt; this task verifies retained evidence and
execution-host discovery. Newly observed drift routes through the owning
maintenance workflow rather than automatically repeating installation.

**Interfaces:** produces verified runtime dependency metadata/SDK schema contract
and exact test/server executable provenance; no adapter tool behavior yet.

**Test assertion anchors:** `self.assertEqual(requirements, {"mcp==2.3.0"})`; `self.assertNotIn("tools/", wheel_payload)` (dependency comparison normalizes packaging spelling).

- [x] Read selected SDK tag's actual MCPServer/stdio/lifespan/tool schemas and Python 3.14 annotation behavior. Review direct/transitive licenses, compatibility and resource cost. Leave the verifier, dependency declarations and lock unchanged during this inspection.
- [x] Add distribution-policy tests using synthetic wheel metadata declaring exactly `mcp==2.3.0`, plus missing/unintended requirement rejection cases and retained source/test leakage guards. Run `uv run --locked python -m unittest discover -s tests -p test_distribution.py -v` against the existing verifier. Record assertion-level red because the intended SDK metadata is rejected; import/setup failure is not the negative control. Do not add the SDK or update the verifier before observing this result.
- [x] Update the verifier to enforce the intended exact dependency allowlist and update obsolete no-runtime-dependency fixture expectations. Rerun the same synthetic distribution suite green; continue rejecting missing/unintended requirements and payload leakage. This checks archive policy, not the still-unchanged project's actual dependency metadata.
- [x] Run `uv add 'mcp==2.3.0'` to update project metadata and regenerate the lock through uv, then `uv sync --locked --all-groups`. Build with `uv build --no-sources` and run `uv run --locked python tools/verify_distribution.py` to prove the actual wheel's Requires-Dist matches the allowlist and its outside-source installation succeeds. Rerun the distribution tests. Never edit uv.lock manually or treat synthetic-policy green as actual SDK adoption evidence.
- [x] Verify the completed gz-skills 0.8.3 reconciliation against the October 31 receipt and retained rollback/provenance. Check catalog/source agreement, duplicates, fresh execution-host discovery and outside-project control. Confirm the configured Git-source refresh separately: the receipt defers that observation to the final handoff, which must be located or re-observed. Do not infer success from the prepublication local-catalog probe. Route new drift through gzs-update-dependencies and starter/native procedures; do not edit native caches or repeat installation without cause.
- [x] Obtain selected cognitive engine availability/qualification evidence via its owning workflow. If unavailable, record owner/blocked condition; strict E3/E4 and final milestone remain closed. Do not substitute complexipy or invent a local scorer. Dependency qualification may proceed in parallel only if the maintainer explicitly permits it; no strict completion claim follows.
- [x] Verify exact managed interpreter, SDK schema/result/cancellation smoke tests, pinned ty 0.0.95 executable/version and source revision, lock and isolated artifact build. Test actual LSP compatibility rather than substituting the earlier 0.0.93 source assessment. Commit reviewed setup changes with normal hooks. Gate G0: runtime inputs tested and remaining engineering blockers individually recorded.

## Phase 1 — reliable MCP–LSP interoperability

### T1: Configuration, URI policy and coordinate value types

**Files:** create models.py, config.py, workspace.py, tests/test_config.py,
tests/test_workspace.py; modify README JSON example after contract is implemented.

**Interfaces:** `load_config(path:Path)->Config`; `Workspace(config:Config)` with
`read(uri:str)->Snapshot`, `manifest()->str`, `offset(snapshot:Snapshot,position:Position)->int`.
Offset is a UTF-8 byte offset for safe byte slicing; no disk writes in this task.

**Test assertion anchors:** `self.assertFalse(config.mutations_enabled)`; `self.assertEqual(workspace.offset(snapshot, Position(0, 3)), 5)`; `with self.assertRaises(AdapterError): workspace.offset(snapshot, Position(0, 2))` for `a😀b\r\n`.

- [x] Write `test_mutations_default_disabled`, `test_reject_unknown_config_and_env_override`, `test_uri_containment_aliases`, `test_utf16_offsets`. Assert mutations false; traversal/remote/query/fragment/NUL denied; for text `a😀b\r\n`, Position(0,3) maps to byte 5 and Position(0,2) raises INVALID_INPUT; bool/fraction positions rejected.
- [x] Run `uv run --locked python -m unittest discover -s tests -p 'test_workspace.py' -v` and the config suite; establish behavior-red, then implement exact signatures/defaults/limits from spec using stdlib only. Include file identity, excluded scope and manifest limits.
- [x] Run both suites green, routine gate and commit. Gate: identity/coordinate tests pass before LSP can query or edit anything.

### T2: Bounded independent JSON-RPC transport

**Files:** create lsp_transport.py, tests/test_lsp_transport.py; create tests/support/fake_lsp.py for subsequent process tasks.

**Interfaces:** `RpcClient(reader:asyncio.StreamReader,writer:asyncio.StreamWriter,limits:Config)`;
`async request(method:str,params:Json,*,timeout:float)->Json`,
`async notify(method:str,params:Json)->None`, `async close()->None`;
`set_handler(method:str,handler:Callable[[Json],Awaitable[Json]])->None`.
Reader loop starts/stops under Session; no product subprocess launched by transport.

**Test assertion anchors:** `self.assertEqual(result_by_id, {1: "first", 2: "second"})` despite reversed response arrival; `self.assertEqual(client.pending_count, 0)` after timeout/EOF (pending_count is a test observation, not a public API).

- [x] Write IsolatedAsyncioTestCase tests `test_fragmented_unicode_frame`, `test_two_writers_do_not_interleave`, `test_out_of_order_ids`, `test_cancel_late_response`, `test_eof_fails_all_waiters`, `test_invalid_or_oversized_frame`. Assert UTF-8 byte count, exact ID correlation, deadlines bounded and pending map empty after cancel/EOF; invalid duplicate Content-Length closes session.
- [x] Run `uv run --locked python -m unittest discover -s tests -p test_lsp_transport.py -v`, verify red, implement serialization/reader/dispatch/deadline ownership, then run green. Do not copy generated Go protocol classes.
- [x] Run routine gate and commit. Gate: C2/C4 transport assertions, not yet real-server interoperability.

### T3: One ty process, official SDK composition and minimal public path

**Files:** create session.py, mcp_api.py, cli.py, __main__.py;
create tests/test_session.py, tests/test_mcp_api.py; modify pyproject.toml entry
point `gz-mcp-lsp = 'gz_mcp_lsp.cli:main'`, distribution verifier/tests.

**Interfaces:** `Session(config:Config)` owns RpcClient and async context entry/exit,
`rpc:RpcClient`, `capabilities:dict[str,Json]`, `generation:str`;
`async restart(generation:str)->None`; `create_server(config:Config,session:Session)->MCPServer`;
`main(argv:Sequence[str]|None=None)->int` for `--config PATH` only.
Intermediate catalog exposes implemented tools only; do not stub success for remaining tools.
T3 owns composition and lifecycle; the first public production tool is hover in
T4, after document identity and generation coordination exist.
T9 later extends this same MCP lifespan/composition with the startup recovery gate;
T3's lifecycle tests do not certify recovery before that integration exists.

**Test assertion anchors:** `self.assertEqual(fake.initialize_count, 1)`; `self.assertEqual(fake.initialized_count, 1)`; `self.assertFalse(reply["applied"])`; `self.assertIsNotNone(child.returncode)` after cleanup.

- [x] Write `test_initialize_once_handlers_ready`, `test_applyedit_denied`, `test_startup_failure_reaped`, `test_parent_eof_and_shutdown_timeout`, `test_stdio_no_log_bytes`, SDK initialize/tools/list/call tests. Assert callbacks before initialized, correct configuration cardinality, UTF-16 negotiation and no leaked child after repeated cleanup. Use fake subprocess, never a readiness sleep.
- [x] Run those suites red, implement lifecycle/stdio composition and missing cleanup; keep no semantic success stubs. Update artifact tests to exercise installed `--help`/bad config and package origin without source-path injection.
- [x] Verify actual pinned ty initialization through the transport and record negotiated capabilities. Do not claim an MCP semantic read at T3. T4 owns the production hover wrapper/operation and fixture required for the first actual installed MCP→adapter→ty read. Routine gate and commit; phase 1 remains unaccepted until T4 passes G1.

### T4: Saved-file documents, bounded generations and real interoperability fixture

**Files:** create documents.py, navigation.py, tests/test_documents.py,
tests/test_navigation.py,
tests/integration/test_interoperability.py and synthetic semantic_workspace package
metadata/source; extend mcp_api.py with production hover, tests/test_mcp_api.py,
workspace.py/session.py only for their owned responsibilities,
.github/workflows/check.yml for platform lanes, and
docs/evidence/<date>-codex-feasibility.md. No temporary probe tool is exposed.

**Interfaces:** `Documents(workspace:Workspace,session:Session)` with
`generation()->AsyncContextManager[GenerationContext]` for workspace-wide operations,
`read(uri:str)->AsyncContextManager[ReadContext]` and
`exclusive()->AsyncContextManager[None]` for the T9 apply boundary, plus
`async committed(snapshots:Sequence[Snapshot])->None`;
`GenerationContext(generation:str,rpc:RpcClient)` and
`ReadContext(snapshot:Snapshot,generation:str,rpc:RpcClient)` are internal immutable
values defined in documents.py. Documents.generation() reconciles and pins
the workspace generation/client without choosing a document URI, taking a document-specific snapshot or
sending didOpen (manifest hashing still reads eligible source bytes). Documents.read(uri) composes that same lease with validated
snapshot/open handling; it consumes one admission slot, not nested/double admission.
All semantic operations hold a generation lease through every RPC, including
workspace-symbol resolution, source/context extraction and final manifest validation;
document operations additionally hold their snapshot. Cancellation and exceptions
release the lease in a finally path. Navigation gains
`Navigation(documents:Documents,session:Session)` and
`async hover(uri:str,position:Position)->Result`, using the final public schema.
T5 extends these same production modules rather than replacing a temporary path.
Tests use an independently authored fixture manifest with explicit expected calls/imports.

**Generation coordination:** Documents owns admission and active read contexts,
bounded to eight. The context pins one generation and its RpcClient; requests
never switch clients mid-call. Serialized reconciliation precedes admission;
document snapshot/open handling is serialized under that same lease and checked
for invalidation before returning a ReadContext. A detected manifest change closes admission, invalidates the old
generation and cancels its active RPC waiters with STALE_DOCUMENT; no old-context
result may be returned. Context release does not wait on the restart it enables.
After all old contexts drain, one transition owner reaps the old ty before starting
the replacement. A new caller waits within its request deadline or gets
WORKSPACE_BUSY/TIMEOUT; caller cancellation remains CANCELLED. Unexpected child
death remains SERVER_EXITED, not a semantic restart. Late replies cannot revive
invalid contexts. No unbounded wait or automatic semantic retry.

T9 apply uses Documents.exclusive() before final preflight, drains active reads
within the configured request budget and holds exclusivity through commit/rollback
and semantic invalidation. Failure to drain returns WORKSPACE_BUSY with zero target
writes. New reads cannot observe an adapter commit in progress. If external changes
invalidate readers while draining, the same stale-result rule applies; no generation
restart runs concurrently with the exclusive commit. T9 tests the shared boundary.

**Test assertion anchors:** `self.assertNotEqual(before_generation, after_generation)` after an unopened-file byte change; `self.assertLessEqual(max_live_children, 1)`; `self.assertEqual(error.code, "STALE_DOCUMENT")` for a mid-query change.

- [x] Write tests `test_open_once_close_eviction`, `test_negotiated_change_versions`, `test_generation_restart_reaps_before_spawn`, `test_unopened_change_create_delete_rename`, `test_midquery_manifest_change_rejected`. Verify exactly one live child, new saved contents visible, no mtime-only shortcut and STALE_DOCUMENT on result races. Use spies/fake server for sync forms plus actual ty for indexing outcomes.
- [x] Add deterministic `test_two_readers_change_restart`, `test_cancel_releases_read_context`, `test_restart_admission_deadline` and `test_late_reply_cannot_publish_old_generation` using barriers/events, not sleeps. Hold reader A's reply, change a source, admit reader B's reconciliation, and assert A fails STALE_DOCUMENT, its waiter/context is released, the replacement starts only after old-child reaping, and B receives the new-generation result or an explicit bounded error. Assert max live children ≤1 and no pending waiter/context leak.
- [x] Add `test_generation_lease_without_document` and `test_document_read_uses_one_lease`: assert an empty workspace can acquire/release a generation without a fabricated URI, source snapshot or didOpen; document reads consume one of the same eight slots; invalidation/cancellation drains both lease forms without leaks. T10 tests actual workspace-symbol behavior on this primitive.
- [x] Write production hover forwarding/schema/content tests red; implement document/session coordination, Navigation.hover and its real SDK wrapper. Run unit suites and `uv run --locked python -m unittest discover -s tests/integration -p test_interoperability.py -v`. Missing ty fails. Assert actual tools/call hover through installed stdio, preserved fixture type text, correct URI/position, and reopened dependency/config visibility. Extend the existing workflow with the platform lanes above and include integrations in ordinary unittest discovery as they are introduced.
- [x] Build/install outside the checkout, run the routine gate in the owning lanes and record G1 actual MCP→adapter→ty hover with correct fixture result. G1 does not require the definition wrapper scheduled in T5. Perform the early Codex checkpoint below, then commit reviewed changes. SDK communication alone does not pass G1.

**Early Codex feasibility checkpoint (before T5):** In an actual Codex session,
register the installed production adapter in a disposable synthetic workspace,
invoke hover through ty, and record host version, launch command, executable origin
and redacted transcript. Verify that this host exposes an approval interaction by
requiring approval for that existing hover tool in a disposable host profile;
observe one allowed invocation and one denial with no adapter call on denial.
Keep hover's read-only annotation unchanged; no temporary mutation/probe tool or
invented consent field. This proves the available approval workflow, not safe
mutation or H2. Record how T11 will exercise approvals for rename/edit on a supported
write host. If installed invocation, interactive denial or access to that write host
cannot be established, record UNKNOWN and pause before T5 for a human decision on
continued implementation; never waive final H1–H3. Full nine-tool and mutation-host
acceptance remains T11.

## Phase 2 — all six reference capabilities, with required corrections

### T5: Definition, references and hover with precise positions and source parity

**Files:** extend T4 navigation.py and tests/test_navigation.py; create source_text.py,
tests/test_source_text.py, tests/integration/test_navigation.py; extend mcp_api.py
and fixture decoy/decorated/nested/async/constant/Unicode cases.

**Interfaces:** `Navigation(documents:Documents,session:Session)` methods
`async definition(uri:str,position:Position,context_lines:int=0)->Result`,
`async references(uri:str,position:Position,include_declaration:bool=False,context_lines:int=0)->Result`,
`async hover(uri:str,position:Position)->Result`;
`declaration(snapshot:Snapshot,selection:Range,symbols:Json)->dict[str,Json]`
in source_text.py returns full/selection/source scope, not a new semantic position.

**Test assertion anchors:** `self.assertEqual(sent_params["position"], {"line": 0, "character": 4})` for the invented one-line definition; `self.assertEqual(expected_call_sites, observed_call_sites)`; `self.assertNotIn(decoy_uri, reference_uris)`.

- [x] Write `test_forwarded_position_is_exact`, `test_locationlink_ranges_remain_distinct`, `test_full_decorated_nested_source`, `test_ast_utf8_columns_differ_from_utf16`, `test_external_source_not_read`, `test_null_hover_variants`. Assert every envelope/schema and no declaration-start substitution.
- [x] Run unit suites red; add definition/references mapping, source extraction and their SDK wrappers, and complete hover normalization/edge cases on the T4 production path. Run green; retain T4's hover regression and canonical signatures. Preserve complete source behavior for supported P1 fixtures, not just locations.
- [x] Run `uv run --locked python -m unittest discover -s tests/integration -p test_navigation.py -v`; direct ty identifier and adapter calls must agree on exact expected call sites/imports, exclude same-name decoy, include declarations only when requested. Record keyword control and caller-provided coordinate provenance; do not add +4 to inputs. Verify empty/limits/source statuses and changed dependencies. Gate P1/P2/P4/S1/S5; routine gate, commit.

### T6: Current pull diagnostics, including unchanged/dependency behavior

**Files:** create diagnostics.py, tests/test_diagnostics.py,
tests/integration/test_diagnostics.py; extend mcp_api.py and synthetic error/fix fixture.

**Interfaces:** `Diagnostics(documents:Documents,session:Session)` with
`async diagnostics(uri:str,context_lines:int=0)->Result` owns resultId cache per
URI+generation; returns normalized current full list even for valid unchanged reports.

**Test assertion anchors:** `self.assertEqual(repaired["result"]["items"], [])`; `self.assertEqual(error.code, "PROTOCOL_ERROR")` for unmatched unchanged reports; `self.assertNotEqual(dependency_generation, previous_generation)`.

- [x] Write `test_full_and_unchanged_resultid`, `test_unchanged_without_cache_is_protocol_error`, `test_pull_error_is_not_empty_success`, `test_repair_and_dependency_change`. Assert cache invalidates on generation change, full current diagnostics used, codes/severity/ranges preserved, related-document external reads denied.
- [x] Run `uv run --locked python -m unittest discover -s tests -p test_diagnostics.py -v` red, implement capability-bound pull handling and SDK wrapper, then green. No sleeps or push-cache fallback.
- [x] Run same-pattern real integration suite to prove error→repair→empty and dependency edits through actual ty/MCP. Gate P3/S6 diagnostic portion; routine gate, commit.

### T7: Pure immutable edit plans and preview identity

**Files:** create edit_plan.py, tests/test_edit_plan.py, tests/fixtures/edit_cases.json.

**Interfaces:** `EditPlan` holds plan_id, workspace/session generation, base snapshots,
after bytes, exact normalized edit set, expiry and confirmation annotations;
`plan_edits(snapshot:Snapshot,edits:Sequence[TextEdit])->bytes`;
`plan_workspace_edit(edit:Json,snapshots:Mapping[str,Snapshot],generation:str)->EditPlan`.
No filesystem side effects or random approval flags inside the planner.

**Test assertion anchors:** `self.assertEqual(plan_edits(snapshot, edits), b"axb\r\n")` for replacing the emoji range; `self.assertEqual(before_hashes, after_preview_hashes)`; `self.assertEqual(error.code, "CONFLICT")` for overlapping ranges.

- [x] Write `test_edits_use_original_snapshot`, `test_adjacent_legal_overlap_rejected`, `test_duplicate_aliases_rejected`, `test_utf16_crlf_eof_bytes`, `test_resource_op_rejects_entire_edit`, `test_versions_and_digest`. Assert Position(0,1)..(0,3) on `a😀b\r\n` replaced by `x` yields exactly `axb\r\n`; coincident inserts fail; annotations/base hashes are bound to digest.
- [x] Run `uv run --locked python -m unittest discover -s tests -p test_edit_plan.py -v` red then implement pure planning with exact preimages, no clamping, count/byte bounds and both text WorkspaceEdit forms. Contradictory changes/documentChanges fail before any IO.
- [x] Run green plus zero-write spy tests, routine gate and commit. Gate W2/W3; preview tokens are content identity, not human consent.

### T8: Guarded POSIX filesystem transactions and durable recovery

**Files:** create filesystem.py, tests/test_filesystem.py,
tests/integration/test_recovery.py; extend fake subprocess support for crash injection only in tests.

**Interfaces:** `Transactions(config:Config,workspace:Workspace)` with
`recover()->list[TransactionReceipt]`, `apply(plan:EditPlan)->TransactionReceipt`, `receipt(plan_id:str)->TransactionReceipt|None`.
Filesystem adapter owns private journal/state lock/durable receipt. Failure statuses
and changed files match spec; no SDK/LSP imports. Supports macOS/Linux guarded local files.

**Test assertion anchors:** `self.assertEqual(after_failure_bytes, before_bytes)` after successful rollback; `self.assertEqual(receipt["status"], "recovery_required")` on external-write conflict; `self.assertEqual(replace_count_after_retry, replace_count_before_retry)`.

- [ ] Write `test_denied_target_changes_zero_files`, `test_parent_symlink_swap_and_hardlink`, `test_preflight_all_targets_before_replace`, `test_failure_at_each_replace_rolls_back`, `test_external_change_during_rollback_requires_recovery`, `test_lost_response_replay_once`, `test_state_quota_and_corrupt_journal`. Assert complete byte/mode hashes and exact statuses, not only exceptions.
- [ ] Run unit suite red, implement no-follow directory-relative validation, all-file staging/verified before-images, durable transitions and rollback rules. Recovery receipts survive preview expiry/session restart. Lookup committed receipts before ordinary expired-plan checks; no replay of an incomplete journal.
- [ ] Run `uv run --locked python -m unittest discover -s tests/integration -p test_recovery.py -v` with disposable subprocess crash at journal/replace/receipt boundaries on both Linux x86_64 and macOS arm64 lanes. Actual exit/restart must restore safe states or lock mutations with per-file recovery status. Add these tests to the existing lane gates now. On Windows run explicit unsupported-write rejection with unchanged source hashes; only POSIX-adapter tests may be marked platform-not-applicable. Missing required POSIX safety capabilities fail their lane. Gate W4–W7 requires separate passing evidence for both claimed write platforms; run routine gate/commit. Do not claim cross-file atomicity from per-file replace.

### T9: Rename/edit MCP tools and post-commit semantics

**Files:** create mutations.py, tests/test_mutations.py,
tests/integration/test_mutations.py and tests/integration/test_startup_recovery.py;
extend mcp_api.py for MCP lifespan/composition and mutation wrappers,
tests/test_mcp_api.py for recovery admission, and documents.py only at its public seams.

**Interfaces:** `Mutations(config:Config,documents:Documents,session:Session,transactions:Transactions)`;
`async preview_rename(uri:str,position:Position,new_name:str)->Result`,
`async preview_edit(uri:str,edits:Sequence[TextEdit],expected_hash:str)->Result`,
`async apply(plan_id:str)->Result` (receipt lookup first).
SDK wrappers use action preview/apply and validate mutually exclusive fields.

**Production startup recovery:** The mcp_api.py lifespan/composition constructs
Transactions and invokes recover() under its transaction-owned state lock, after
validating platform and operator authority but before yielding mutation admission.
No preview or apply may run while startup recovery is pending. For enabled writes
on a supported host, successful recovery completes before admitting mutations;
any recovery_required receipt or corrupt/unreadable state becomes a persistent
RECOVERY_REQUIRED mutation lockout. Do not silently treat an exception as an empty
recovery result. The lifespan may expose tool schemas after reaching that locked
state, but all mutation calls must return the lockout without new target writes.
Pending recovery keeps startup admission closed; startup cancellation releases
the lock through bounded cleanup or leaves durable recoverable state.

Disabled mutations or an unsupported write platform must never trigger automatic
source restoration merely by starting the server. Retain the mutation denial and
require valid operator authority before recovery writes; changed writable roots
or unsafe recovery targets fail closed. This preserves disabled-mode zero writes.
Recovery journal contents remain untrusted and subject to the T8 filesystem policy.
The startup gate is production wiring, not a test-only call to recover().

**Test assertion anchors:** `self.assertEqual(error.code, "MUTATIONS_DISABLED")`; `self.assertEqual(before_hashes, rejected_after_hashes)`; `self.assertEqual(retry_receipt, committed_receipt)` after restart.

- [ ] Write `test_disabled_and_claimed_approval_denied`, `test_preview_immutable_no_write`, `test_stale_apply_is_not_replanned`, `test_rename_prepare_and_null`, `test_annotations_remain_destructive`, `test_cancel_during_apply_does_not_lose_receipt`, `test_committed_but_sync_failed_is_not_rollback`. Assert new_name identifier/keyword rules and all denied cases leave source hashes unchanged.
- [ ] Add `test_apply_drains_readers_before_preflight`, `test_read_admission_blocked_during_commit`, `test_apply_drain_timeout_writes_nothing` and `test_no_restart_during_commit` against T4's coordinator. Use barriers to hold a read and a commit separately; assert no target replacement while reads remain, no semantic result during partial commit, no concurrent restart and bounded WORKSPACE_BUSY on drain timeout. Assert cancellation releases admission and post-commit reads use a fresh generation or fail explicitly.
- [ ] Write `test_lifespan_recovers_before_mutation_admission`, `test_recovery_lockout_rejects_all_mutations` and `test_disabled_or_unsupported_startup_never_restores_source`. Hold recovery with a test barrier and assert the actual production lifespan cannot admit mutation calls; release it and assert admission only after verified recovery. Inject corrupt state/unsafe targets and assert RECOVERY_REQUIRED with no additional target writes; disabled/unsupported startup preserves source hashes even with an incomplete journal.
- [ ] Run unit tests red; implement the production lifespan recovery gate and mutation wrappers together with prepareRename when advertised, real rename response planning, bounded retained previews (32/10 minutes), authority checks and shared transaction application. Obtain unit green before installed startup tests. A committed disk transaction followed by sync failure returns committed status with semantic_state unavailable and blocks stale reads; never misreports disk rollback. Shield commit/rollback and durably record its outcome; if the SDK has already
  returned cancellation, retry of the same plan_id reports the receipt rather than
  implying zero writes or reapplying.
- [ ] Build/install outside the checkout, then run `uv run --locked python -m unittest discover -s tests/integration -p test_startup_recovery.py -v` on both POSIX write lanes. Seed an incomplete journal via a disposable adapter subprocess crash, launch the installed CLI over real stdio without a test calling recover(), and assert safe restoration precedes the first accepted mutation. With an externally changed target or corrupt journal, assert real rename/edit previews and apply remain locked out and source hashes do not change further. Verify cleanup/restart after pending-recovery cancellation. Windows runs the zero-restoration denial case; POSIX recovery cases remain explicitly not applicable there.
- [ ] Run `uv run --locked python -m unittest discover -s tests/integration -p test_mutations.py -v`: real ty multi-module rename, local edit insert/replace/delete/EOF, complete rejected-set and post-edit definitions/references/diagnostics/hover. Lost response/retry stable; restart expires previews but returns prior receipt. Gate G2 = all P1–P6, W1–W8 and required protocol rows pass; routine gate/commit. Safe write behavior is required parity, not deferred polish.

## Phase 3 — bounded ty navigation extensions

### T10: Public document symbols, workspace symbols and implementations

**Files:** extend navigation.py/mcp_api.py; create tests/test_symbols.py,
tests/integration/test_symbols.py; extend class hierarchy and duplicate-symbol fixture.

**Interfaces:** Navigation gains
`async document_symbols(uri:str)->Result`,
`async workspace_symbols(query:str,resolve:bool=False)->Result`,
`async implementations(uri:str,position:Position)->Result`.
Internal document-symbol source support from T5 is reused, not duplicated.
workspace_symbols holds Documents.generation() across search, any advertised
resolve requests, normalization and final validation. It never selects an arbitrary
document to obtain a lease. Document symbols/implementations use Documents.read(uri).

**Test assertion anchors:** `self.assertEqual(set(tool_names), {"definition", "references", "diagnostics", "hover", "rename_symbol", "edit_file", "document_symbols", "workspace_symbols", "implementations"})`; `self.assertIsNone(unresolved["selection_range"])`.

- [ ] Write `test_nested_symbol_ranges`, `test_uri_only_symbol_never_guesses_position`, `test_duplicate_names_preserved`, `test_implementation_supported_empty_unsupported`, `test_exact_final_tool_catalog`. Assert nine expected names and no additional mutation/execute tools.
- [ ] Add `test_empty_workspace_symbols_needs_no_uri`, `test_workspace_change_during_symbol_search` and `test_workspace_change_during_symbol_resolve`. Assert successful empty search without a synthetic document/didOpen, and use barriers to change the workspace during search/resolve: return STALE_DOCUMENT, discard all old-generation results and release the generation lease. Include the empty-workspace and changed-workspace cases in real-ty integration evidence; fake barriers independently prove the precise race.
- [ ] Run unit suite red, implement exact methods/capability checks and SDK wrappers, then green. Preserve hierarchy, stable order and actual resolved ranges only.
- [ ] Run real-ty symbols/implementation suite with known subclass/member overrides and duplicate names. Gate G3 = S2/S3/S4 plus previous parity still green; routine gate/commit. No declaration/type-definition/call-hierarchy tool added.

## Phase 4 — installed Codex acceptance, engineering closure and stop

### T11: Installed distribution and actual Codex host acceptance

**Files:** extend tools/verify_distribution.py/tests/test_distribution.py,
.github/workflows/check.yml, README.md, SECURITY.md, CONTRIBUTING.md;
create tests/integration/test_installed_server.py and docs/evidence/<date>-codex-acceptance.md.
Keep application-specific host profiles/examples under docs/examples/, not enabled in
this repository's native engineering plugin config.

**Interfaces:** installed CLI `gz-mcp-lsp --config PATH`; official SDK stdio client
for distribution scenarios; actual Codex session using the same installed executable.
No new framework/host launcher product API.

**Test assertion anchors:** `self.assertEqual(installed_origin_root, clean_environment_root)` after resolving origin; `self.assertEqual(before_hashes, host_denied_after_hashes)`; each of nine host calls has asserted semantic/result content, not only a non-error flag.

- [ ] Extend artifact guard tests red for missing entry point/resources/notices/declared SDK deps; build `uv build --no-sources`, install wheel in clean outside-source runtime-only environment and verify all six capabilities/extensions over stdio with actual ty. Verify source independence/import origin and no development dependency masking.
- [ ] Complete installed-server coverage in the platform lanes established at T4 and extended at T8/T9; integration tests already participate in ordinary unittest discovery. Install dependencies at CI setup, never during MCP requests. Preserve four hooks. Missing ty or skipped required tests fail claimed-platform acceptance. Retain separate Linux x86_64/macOS arm64 write receipts, and Windows read/unsupported-write evidence with narrowly identified POSIX-only not-applicable tests; never enable Windows writes.
- [ ] Revisit T4's host-feasibility receipt and resolve any recorded limitation. In a disposable synthetic workspace on a supported write host, use actual Codex version/trust/stdio registration to discover and invoke all nine tools. First read-only startup: read successes and both mutation rejections; then operator write-enabled profile: previews and approved rename/edit apply, exact file assertions and fresh follow-up semantics. Configure mutation tool approval policy using current official host docs, not invented consent metadata. Early hover approval/denial does not substitute for actual rename/edit approvals and denial here.
- [ ] Observe a **denied host mutation approval** and compare before/after hashes; inspect actual host transcript, not only direct SDK results. If this harness cannot exercise approval interaction, H2 remains UNKNOWN and host acceptance is not passed. Capture timeout/ty death/EOF cleanup and PID reaping. Gate G4 = H1–H3/E2 measured; routine gate/commit with sanitized receipts.

### T12: Full affected-input engineering acceptance and plan reconciliation

**Files:** project evidence and owning configuration/contracts only when justified;
no new product capabilities. Add explicit Import Linter contracts for SDK-only boundary,
semantic→port direction and filesystem isolation in pyproject.toml.

**Interfaces:** repository-owned acceptance commands/A01–A18 evidence, not a new lifecycle.

- [ ] Run effective interpreter/tool/source provenance and required gate: `uv sync --locked --all-groups`; `uv run --locked pre-commit run --all-files`; `uv build --no-sources`; `uv run --locked python tools/verify_distribution.py`. Observe CI for exact candidate SHA when synchronization is authorized.
- [ ] Run applicable separate C901, independently qualified cognitive scorer, Lizard, cohesion, Interrogate, Vulture, Bandit, statement/branch coverage, bounded Cosmic Ray, deptry, pip-audit and Import Linter against actual runtime and meaningful tests. Document reviewed findings/survivors/timeouts and scopes; no inherited score floor, weakened ceiling or known-broken scorer PASS.
- [ ] Close T0 cognitive qualification and execution-host verification of the completed gz-skills reconciliation with correct sources/native discovery and selected pins. If unavailable, list owner/external condition and explicitly withhold strict E3/E4/terminal acceptance; do not describe partial work as full accepted parity milestone.
- [ ] Use gzs-plan-audit/intent comparison to map each P/S/C/D/W/H/E row to exact observed evidence and inventory every skipped test by platform/reason. A Windows POSIX-only not-applicable entry cannot satisfy Linux/macOS write evidence, and missing required lane evidence stays UNKNOWN. All required rows need observed PASS or a human-approved scope revision before any altered claim; an exception does not silently become strict conformance. Gate G5: engineering acceptance complete; routine gate/commit.

### T13: Accept the bounded milestone and stop

**Files:** CHANGELOG.md, ROADMAP.md, product evidence index and final report.

**Interfaces:** no new runtime interface.

- [ ] Review every acceptance row and the four human decisions against actual results. Record exact product/reference/ty/SDK/Codex revisions, supported OS scope, installed behavior and recovery limitations. Complete milestone only when all required rows pass; otherwise name the specific incomplete gates.
- [ ] Present tactical/operational/strategic results for human acceptance; preserve source attribution and current release status. No tag, release, second server or additional capability.
- [ ] **STOP.** Further work requires a new user instruction. Do not turn successful tests into authorization for continued framework development.

## Plan self-review and execution handoff

Coverage: P1/P2/P4→T5, P3→T6, P5/P6→T7–T9; S1/S5→T5,
S2–S4→T10, S6→T6/T9; protocol C→T2–T4/T8, workspace D→T1/T4/T5,
write W→T7–T9, early host feasibility→T4, full host H→T11,
engineering E→T0/T4/T8/T11/T12, STOP→T13. Production hover starts at T4;
P4/S5 acceptance still requires T5/T11. Platform lanes and concurrency tests
are assigned before dependent write/host acceptance, not deferred to the last gate.
Shared type/signature names and five Review Focus cases have owning tests above.
Tasks produce meaningful independently reviewable results; related setup belongs
to its deliverable, and all six tools remain in the finite phase-2 gate.

The work is one interconnected adapter, not independent subsystem projects. Commit
boundaries permit review without converting transport or transaction helpers into
public general-purpose libraries. Gate evidence, not task checkbox counts, controls
acceptance. This plan contains decisions/tests/signatures, no runtime implementation.

Human review and execution approval were received on 2026-11-01. Use the approved
plan in an isolated implementation branch; retain every required gate and the
T4 host-feasibility checkpoint. No merge, push, tag or release follows automatically.
