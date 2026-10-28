# Reference Parity and ty Semantic Navigation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver accepted six-tool functional reference parity, corrected semantic targeting, the three specified ty navigation extensions and actual Codex interoperability, then stop.

**Architecture:** Official MCP Python SDK stdio adapter over narrow semantic operations, document/workspace identity, independent JSON-RPC transport and a single ty lifecycle owner. Rename and edit share pure planning and a guarded filesystem/recovery boundary; no general LSP framework.

**Tech Stack:** Managed CPython 3.14.10, uv/uv_build 0.13.6, Ruff 0.17.3, ty 0.0.93, pre-commit 4.7.0, unittest; proposed runtime mcp 2.3.0 and stdlib.

**Spec:** [Revision 2 specification](../specs/2026-10-28-semantic-navigation-design.md), [pinned parity matrix](../../discovery/reference-parity.md), [acceptance matrix](../../discovery/acceptance-matrix.md).

**STATUS: UNAPPROVED PLAN. Every task below is future work. No runtime task has started.**
The user expressly requested planning before approval, overriding the usual workflow
ordering for plan preparation only. It does not approve the approach, public schema,
write guarantees or execution. Resolve the specification's four review decisions
and obtain human approval before executing even T0. Do not invoke execution skills now.

## Global Constraints

- Python 3.14 family, selected managed CPython 3.14.10; uv/uv_build 0.13.6, Ruff 0.17.3, ty 0.0.93, pre-commit 4.7.0, unittest, src packaging and project lock.
- Official MCP SDK candidate mcp 2.3.0 (`2118f14f8a19bc158d8a1cf90af58d85d187f849`); ty candidate 0.0.93 (`3db5e4df7becd3ca55fd06c78e98bf7c8a38e469`). Test/review changes to these inputs; do not float latest during tests.
- Go baseline v0.1.1 (`46e2950b7969334780675e7797e13f140d2d42ac`), assessed main `e4395849a52e18555361abab60a060802c06bf50`; independent implementation, no copied source/tests/media.
- One canonical workspace, one live ty process, MCP/LSP stdio only, saved-disk inputs. No second server, install during requests, code actions, execute command, listener or framework.
- No Makefile or environment-variable application configuration. Application JSON; preserve native host formats and selected lite profile/disabled Backplane.
- UTF-16 code-unit zero-based positions and end-exclusive ranges. Exact caller positions, no workspace-symbol-range-start or fixed-column inference.
- All P1–P6 and S1–S6 are required; final catalog is six reference names plus document_symbols, workspace_symbols, implementations. No silent removal or indefinite deferral.
- Mutations disabled by default, explicit operator writable roots, preview/apply, bounded preflight and recovery. No portable atomic multi-file filesystem transaction is claimed.
- Required FAIL/UNKNOWN/stale acceptance evidence blocks the terminal milestone; cognitive qualification and gz-skills reconciliation are not waived.
- Initial claimed write platforms: macOS arm64 and Linux x86_64 local filesystems; unsupported Windows writes disabled until equivalent safety proof.
- Routine hook set remains Ruff check/format, ty and unittest; deeper analyses stay outside routine hooks/CI. No tag/release publication.

## Review Focus

1. Unopened dependency changes/config changes between calls must invalidate/restart ty, and changes during a query must discard stale results — T4/T5/T6 tests.
2. Percent-encoded aliases, symlinked parents and hardlinks must never bypass write containment or duplicate-target checks — T1/T7/T8 tests.
3. Cancellation or process death at the commit/receipt boundary must produce durable exactly-once outcome or explicit recovery, never an apparent empty success — T8/T9 tests.
4. Emoji before a target, CRLF/mixed newline and AST UTF-8 offsets must not shift semantic positions or corrupt replacement bytes — T1/T5/T7 tests.
5. Host approval denial and a model's claimed approval must leave targets unchanged; real Codex calls are required in addition to SDK tests — T9/T11 tests.

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
`docs/evidence/<date>-runtime-inputs.md`. Reviewed gz-skills reconciliation may
change only owning catalogs/config/managed records through documented procedures.

**Interfaces:** produces verified runtime dependency metadata/SDK schema contract
and exact test/server executable provenance; no adapter tool behavior yet.

**Test assertion anchors:** `self.assertEqual(requirements, {"mcp==2.3.0"})`; `self.assertNotIn("tools/", wheel_payload)` (dependency comparison normalizes packaging spelling).

- [ ] Read selected SDK tag's actual MCPServer/stdio/lifespan/tool schemas and Python 3.14 annotation behavior. Review direct/transitive licenses, compatibility and resource cost. Resolve official SDK with `uv add 'mcp==2.3.0'` only after updating the design-stage no-dependency guard to the intended dependency allowlist.
- [ ] Add distribution tests asserting the intended Requires-Dist and rejection of unintended requirements, while retaining source/test leakage failures. Run `uv run --locked python -m unittest discover -s tests -p test_distribution.py -v`; verify red on the old dependency policy, then update the verifier and obtain green. No blanket removal of dependency checks.
- [ ] Use gzs-update-dependencies and starter/native documented reconciliation for gz-skills 0.8.0→reviewed current release; inventory duplicates, compare source bytes, fresh-session discovery and outside-project control. Preserve old provenance/rollback. Do not edit native cache or relabel old SHA. Record failure as an explicit gate, not an upgrade claim.
- [ ] Obtain selected cognitive engine availability/qualification evidence via its owning workflow. If unavailable, record owner/blocked condition; strict E3/E4 and final milestone remain closed. Do not substitute complexipy or invent a local scorer. Dependency qualification may proceed in parallel only if the maintainer explicitly permits it; no strict completion claim follows.
- [ ] Verify exact managed interpreter, SDK schema/result/cancellation smoke tests, pinned ty executable/version, lock and isolated artifact build. Commit reviewed setup changes with normal hooks. Gate G0: runtime inputs tested and remaining engineering blockers individually recorded.

## Phase 1 — reliable MCP–LSP interoperability

### T1: Configuration, URI policy and coordinate value types

**Files:** create models.py, config.py, workspace.py, tests/test_config.py,
tests/test_workspace.py; modify README JSON example after contract is implemented.

**Interfaces:** `load_config(path:Path)->Config`; `Workspace(config:Config)` with
`read(uri:str)->Snapshot`, `manifest()->str`, `offset(snapshot:Snapshot,position:Position)->int`.
Offset is a UTF-8 byte offset for safe byte slicing; no disk writes in this task.

**Test assertion anchors:** `self.assertFalse(config.mutations_enabled)`; `self.assertEqual(workspace.offset(snapshot, Position(0, 3)), 5)`; `with self.assertRaises(AdapterError): workspace.offset(snapshot, Position(0, 2))` for `a😀b\r\n`.

- [ ] Write `test_mutations_default_disabled`, `test_reject_unknown_config_and_env_override`, `test_uri_containment_aliases`, `test_utf16_offsets`. Assert mutations false; traversal/remote/query/fragment/NUL denied; for text `a😀b\r\n`, Position(0,3) maps to byte 5 and Position(0,2) raises INVALID_INPUT; bool/fraction positions rejected.
- [ ] Run `uv run --locked python -m unittest discover -s tests -p 'test_workspace.py' -v` and the config suite; establish behavior-red, then implement exact signatures/defaults/limits from spec using stdlib only. Include file identity, excluded scope and manifest limits.
- [ ] Run both suites green, routine gate and commit. Gate: identity/coordinate tests pass before LSP can query or edit anything.

### T2: Bounded independent JSON-RPC transport

**Files:** create lsp_transport.py, tests/test_lsp_transport.py; create tests/support/fake_lsp.py for subsequent process tasks.

**Interfaces:** `RpcClient(reader:asyncio.StreamReader,writer:asyncio.StreamWriter,limits:Config)`;
`async request(method:str,params:Json,*,timeout:float)->Json`,
`async notify(method:str,params:Json)->None`, `async close()->None`;
`set_handler(method:str,handler:Callable[[Json],Awaitable[Json]])->None`.
Reader loop starts/stops under Session; no product subprocess launched by transport.

**Test assertion anchors:** `self.assertEqual(result_by_id, {1: "first", 2: "second"})` despite reversed response arrival; `self.assertEqual(client.pending_count, 0)` after timeout/EOF (pending_count is a test observation, not a public API).

- [ ] Write IsolatedAsyncioTestCase tests `test_fragmented_unicode_frame`, `test_two_writers_do_not_interleave`, `test_out_of_order_ids`, `test_cancel_late_response`, `test_eof_fails_all_waiters`, `test_invalid_or_oversized_frame`. Assert UTF-8 byte count, exact ID correlation, deadlines bounded and pending map empty after cancel/EOF; invalid duplicate Content-Length closes session.
- [ ] Run `uv run --locked python -m unittest discover -s tests -p test_lsp_transport.py -v`, verify red, implement serialization/reader/dispatch/deadline ownership, then run green. Do not copy generated Go protocol classes.
- [ ] Run routine gate and commit. Gate: C2/C4 transport assertions, not yet real-server interoperability.

### T3: One ty process, official SDK composition and minimal public path

**Files:** create session.py, mcp_api.py, cli.py, __main__.py;
create tests/test_session.py, tests/test_mcp_api.py; modify pyproject.toml entry
point `gz-mcp-lsp = 'gz_mcp_lsp.cli:main'`, distribution verifier/tests.

**Interfaces:** `Session(config:Config)` owns RpcClient and async context entry/exit,
`rpc:RpcClient`, `capabilities:dict[str,Json]`, `generation:str`;
`async restart(generation:str)->None`; `create_server(config:Config,session:Session)->MCPServer`;
`main(argv:Sequence[str]|None=None)->int` for `--config PATH` only.
Intermediate catalog exposes implemented tools only; do not stub success for remaining tools.

**Test assertion anchors:** `self.assertEqual(fake.initialize_count, 1)`; `self.assertEqual(fake.initialized_count, 1)`; `self.assertFalse(reply["applied"])`; `self.assertIsNotNone(child.returncode)` after cleanup.

- [ ] Write `test_initialize_once_handlers_ready`, `test_applyedit_denied`, `test_startup_failure_reaped`, `test_parent_eof_and_shutdown_timeout`, `test_stdio_no_log_bytes`, SDK initialize/tools/list/call tests. Assert callbacks before initialized, correct configuration cardinality, UTF-16 negotiation and no leaked child after repeated cleanup. Use fake subprocess, never a readiness sleep.
- [ ] Run those suites red, implement lifecycle/stdio composition and missing cleanup; keep no semantic success stubs. Update artifact tests to exercise installed `--help`/bad config and package origin without source-path injection.
- [ ] Verify actual pinned ty initialization through the transport and a minimal SDK stdio read path using the T4 fixture, recording negotiated capabilities. T3 may be committed before this joint integration gate, but phase 1 is not accepted until T4 supplies it. Routine gate and commit.

### T4: Saved-file documents, bounded generations and real interoperability fixture

**Files:** create documents.py, tests/test_documents.py,
tests/integration/test_interoperability.py and synthetic semantic_workspace package
metadata/source; extend workspace.py/session.py only for their owned responsibilities.

**Interfaces:** `Documents(workspace:Workspace,session:Session)` with
`async prepare(uri:str)->Snapshot`, `async finish(generation:str)->None`,
`async committed(snapshots:Sequence[Snapshot])->None`; prepare does serialized
manifest reconciliation/restart/open, finish rejects changed generation.
Tests use an independently authored fixture manifest with explicit expected calls/imports.

**Test assertion anchors:** `self.assertNotEqual(before_generation, after_generation)` after an unopened-file byte change; `self.assertLessEqual(max_live_children, 1)`; `self.assertEqual(error.code, "STALE_DOCUMENT")` for a mid-query change.

- [ ] Write tests `test_open_once_close_eviction`, `test_negotiated_change_versions`, `test_generation_restart_reaps_before_spawn`, `test_unopened_change_create_delete_rename`, `test_midquery_manifest_change_rejected`. Verify exactly one live child, new saved contents visible, no mtime-only shortcut and STALE_DOCUMENT on result races. Use spies/fake server for sync forms plus actual ty for indexing outcomes.
- [ ] Run unit tests red then implement document/session generation behavior; run `uv run --locked python -m unittest discover -s tests/integration -p test_interoperability.py -v`. Missing ty is a hard failure, not skipped acceptance. Assert actual hover/definition request to ty through initialized session, including unopened consumer/config changes and restart consistency.
- [ ] Run routine gate and installed stdio smoke, record G1 actual MCP→adapter→ty response with correct fixture result, commit. Proving SDK communication alone does not pass G1.

## Phase 2 — all six reference capabilities, with required corrections

### T5: Definition, references and hover with precise positions and source parity

**Files:** create navigation.py, source_text.py, tests/test_navigation.py,
tests/test_source_text.py, tests/integration/test_navigation.py; extend mcp_api.py
and fixture decoy/decorated/nested/async/constant/Unicode cases.

**Interfaces:** `Navigation(documents:Documents,session:Session)` methods
`async definition(uri:str,position:Position,context_lines:int=0)->Result`,
`async references(uri:str,position:Position,include_declaration:bool=False,context_lines:int=0)->Result`,
`async hover(uri:str,position:Position)->Result`;
`declaration(snapshot:Snapshot,selection:Range,symbols:Json)->dict[str,Json]`
in source_text.py returns full/selection/source scope, not a new semantic position.

**Test assertion anchors:** `self.assertEqual(sent_params["position"], {"line": 0, "character": 4})` for the invented one-line definition; `self.assertEqual(expected_call_sites, observed_call_sites)`; `self.assertNotIn(decoy_uri, reference_uris)`.

- [ ] Write `test_forwarded_position_is_exact`, `test_locationlink_ranges_remain_distinct`, `test_full_decorated_nested_source`, `test_ast_utf8_columns_differ_from_utf16`, `test_external_source_not_read`, `test_null_hover_variants`. Assert every envelope/schema and no declaration-start substitution.
- [ ] Run unit suites red; implement mapping/source extraction/normalization and three SDK tool wrappers using canonical signatures; run green. Preserve complete source behavior for supported P1 fixtures, not just locations.
- [ ] Run `uv run --locked python -m unittest discover -s tests/integration -p test_navigation.py -v`; direct ty identifier and adapter calls must agree on exact expected call sites/imports, exclude same-name decoy, include declarations only when requested. Record keyword control and caller-provided coordinate provenance; do not add +4 to inputs. Verify empty/limits/source statuses and changed dependencies. Gate P1/P2/P4/S1/S5; routine gate, commit.

### T6: Current pull diagnostics, including unchanged/dependency behavior

**Files:** create diagnostics.py, tests/test_diagnostics.py,
tests/integration/test_diagnostics.py; extend mcp_api.py and synthetic error/fix fixture.

**Interfaces:** `Diagnostics(documents:Documents,session:Session)` with
`async diagnostics(uri:str,context_lines:int=0)->Result` owns resultId cache per
URI+generation; returns normalized current full list even for valid unchanged reports.

**Test assertion anchors:** `self.assertEqual(repaired["result"]["items"], [])`; `self.assertEqual(error.code, "PROTOCOL_ERROR")` for unmatched unchanged reports; `self.assertNotEqual(dependency_generation, previous_generation)`.

- [ ] Write `test_full_and_unchanged_resultid`, `test_unchanged_without_cache_is_protocol_error`, `test_pull_error_is_not_empty_success`, `test_repair_and_dependency_change`. Assert cache invalidates on generation change, full current diagnostics used, codes/severity/ranges preserved, related-document external reads denied.
- [ ] Run `uv run --locked python -m unittest discover -s tests -p test_diagnostics.py -v` red, implement capability-bound pull handling and SDK wrapper, then green. No sleeps or push-cache fallback.
- [ ] Run same-pattern real integration suite to prove error→repair→empty and dependency edits through actual ty/MCP. Gate P3/S6 diagnostic portion; routine gate, commit.

### T7: Pure immutable edit plans and preview identity

**Files:** create edit_plan.py, tests/test_edit_plan.py, tests/fixtures/edit_cases.json.

**Interfaces:** `EditPlan` holds plan_id, workspace/session generation, base snapshots,
after bytes, exact normalized edit set, expiry and confirmation annotations;
`plan_edits(snapshot:Snapshot,edits:Sequence[TextEdit])->bytes`;
`plan_workspace_edit(edit:Json,snapshots:Mapping[str,Snapshot],generation:str)->EditPlan`.
No filesystem side effects or random approval flags inside the planner.

**Test assertion anchors:** `self.assertEqual(plan_edits(snapshot, edits), b"axb\r\n")` for replacing the emoji range; `self.assertEqual(before_hashes, after_preview_hashes)`; `self.assertEqual(error.code, "CONFLICT")` for overlapping ranges.

- [ ] Write `test_edits_use_original_snapshot`, `test_adjacent_legal_overlap_rejected`, `test_duplicate_aliases_rejected`, `test_utf16_crlf_eof_bytes`, `test_resource_op_rejects_entire_edit`, `test_versions_and_digest`. Assert Position(0,1)..(0,3) on `a😀b\r\n` replaced by `x` yields exactly `axb\r\n`; coincident inserts fail; annotations/base hashes are bound to digest.
- [ ] Run `uv run --locked python -m unittest discover -s tests -p test_edit_plan.py -v` red then implement pure planning with exact preimages, no clamping, count/byte bounds and both text WorkspaceEdit forms. Contradictory changes/documentChanges fail before any IO.
- [ ] Run green plus zero-write spy tests, routine gate and commit. Gate W2/W3; preview tokens are content identity, not human consent.

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
- [ ] Run `uv run --locked python -m unittest discover -s tests/integration -p test_recovery.py -v` with disposable subprocess crash at journal/replace/receipt boundaries. Actual process exit and restart must restore safe states or lock mutations with per-file recovery status. Unsupported platform/filesystem capabilities fail closed. Gate W4–W7; run routine gate/commit. Do not claim cross-file atomicity from per-file replace.

### T9: Rename/edit MCP tools and post-commit semantics

**Files:** create mutations.py, tests/test_mutations.py,
tests/integration/test_mutations.py; extend mcp_api.py/documents.py only at their public seams.

**Interfaces:** `Mutations(config:Config,documents:Documents,session:Session,transactions:Transactions)`;
`async preview_rename(uri:str,position:Position,new_name:str)->Result`,
`async preview_edit(uri:str,edits:Sequence[TextEdit],expected_hash:str)->Result`,
`async apply(plan_id:str)->Result` (receipt lookup first).
SDK wrappers use action preview/apply and validate mutually exclusive fields.

**Test assertion anchors:** `self.assertEqual(error.code, "MUTATIONS_DISABLED")`; `self.assertEqual(before_hashes, rejected_after_hashes)`; `self.assertEqual(retry_receipt, committed_receipt)` after restart.

- [ ] Write `test_disabled_and_claimed_approval_denied`, `test_preview_immutable_no_write`, `test_stale_apply_is_not_replanned`, `test_rename_prepare_and_null`, `test_annotations_remain_destructive`, `test_cancel_during_apply_does_not_lose_receipt`, `test_committed_but_sync_failed_is_not_rollback`. Assert new_name identifier/keyword rules and all denied cases leave source hashes unchanged.
- [ ] Run unit tests red; implement prepareRename when advertised, real rename response planning, bounded retained previews (32/10 minutes), authority checks and shared transaction application. A committed disk transaction followed by sync failure returns committed status with semantic_state unavailable and blocks stale reads; never misreports disk rollback. Shield commit/rollback and durably record its outcome; if the SDK has already
  returned cancellation, retry of the same plan_id reports the receipt rather than
  implying zero writes or reapplying.
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

**Test assertion anchors:** `self.assertEqual(set(tool_names), {"definition", "references", "diagnostics", "hover", "rename_symbol", "edit_file", "document_symbols", "workspace_symbols", "implementations"})`; `self.assertIsNone(unresolved["selection_range"])`.

- [ ] Write `test_nested_symbol_ranges`, `test_uri_only_symbol_never_guesses_position`, `test_duplicate_names_preserved`, `test_implementation_supported_empty_unsupported`, `test_exact_final_tool_catalog`. Assert nine expected names and no additional mutation/execute tools.
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
- [ ] Add required pinned-ty integration tests to ordinary unittest/CI scope; install dependencies at CI setup, never during MCP requests. Preserve four-hook set. Missing ty fails, no acceptance skip. Observe macOS/Linux separately; do not enable Windows writes.
- [ ] In disposable synthetic workspace, use actual Codex version/trust/stdio registration to discover and invoke all nine tools. First read-only startup: read successes and both mutation rejections; then operator write-enabled profile: previews and approved rename/edit apply, exact file assertions and fresh follow-up semantics. Configure mutation tool approval policy using current official host docs, not invented consent metadata.
- [ ] Observe a **denied host mutation approval** and compare before/after hashes; inspect actual host transcript, not only direct SDK results. If this harness cannot exercise approval interaction, H2 remains UNKNOWN and host acceptance is not passed. Capture timeout/ty death/EOF cleanup and PID reaping. Gate G4 = H1–H3/E2 measured; routine gate/commit with sanitized receipts.

### T12: Full affected-input engineering acceptance and plan reconciliation

**Files:** project evidence and owning configuration/contracts only when justified;
no new product capabilities. Add explicit Import Linter contracts for SDK-only boundary,
semantic→port direction and filesystem isolation in pyproject.toml.

**Interfaces:** repository-owned acceptance commands/A01–A18 evidence, not a new lifecycle.

- [ ] Run effective interpreter/tool/source provenance and required gate: `uv sync --locked --all-groups`; `uv run --locked pre-commit run --all-files`; `uv build --no-sources`; `uv run --locked python tools/verify_distribution.py`. Observe CI for exact candidate SHA when synchronization is authorized.
- [ ] Run applicable separate C901, independently qualified cognitive scorer, Lizard, cohesion, Interrogate, Vulture, Bandit, statement/branch coverage, bounded Cosmic Ray, deptry, pip-audit and Import Linter against actual runtime and meaningful tests. Document reviewed findings/survivors/timeouts and scopes; no inherited score floor, weakened ceiling or known-broken scorer PASS.
- [ ] Close T0 cognitive/gz-skills evidence with correct sources/native discovery and current pins. If unavailable, list owner/external condition and explicitly withhold strict E3/E4/terminal acceptance; do not describe partial work as full accepted parity milestone.
- [ ] Use gzs-plan-audit/intent comparison to map each P/S/C/D/W/H/E row to exact observed evidence. All required rows need observed PASS or a human-approved scope revision before any altered claim; an exception does not silently become strict conformance. Gate G5: engineering acceptance complete; routine gate/commit.

### T13: Accept the bounded milestone and stop

**Files:** CHANGELOG.md, ROADMAP.md, product evidence index and final report.

**Interfaces:** no new runtime interface.

- [ ] Review every acceptance row and the four human decisions against actual results. Record exact product/reference/ty/SDK/Codex revisions, supported OS scope, installed behavior and recovery limitations. Complete milestone only when all required rows pass; otherwise name the specific incomplete gates.
- [ ] Present tactical/operational/strategic results for human acceptance; preserve source attribution and current release status. No tag, release, second server or additional capability.
- [ ] **STOP.** Further work requires a new user instruction. Do not turn successful tests into authorization for continued framework development.

## Plan self-review and execution handoff

Coverage: P1/P2/P4→T5, P3→T6, P5/P6→T7–T9; S1/S5→T5,
S2–S4→T10, S6→T6/T9; protocol C→T2–T4/T8, workspace D→T1/T4/T5,
write W→T7–T9, host H→T11, engineering E→T0/T11/T12, STOP→T13.
Shared type/signature names and five Review Focus cases have owning tests above.
Tasks produce meaningful independently reviewable results; related setup belongs
to its deliverable, and all six tools remain in the finite phase-2 gate.

The work is one interconnected adapter, not independent subsystem projects. Commit
boundaries permit review without converting transport or transaction helpers into
public general-purpose libraries. Gate evidence, not task checkbox counts, controls
acceptance. This plan contains decisions/tests/signatures, no runtime implementation.

Human review is required now. Choose/confirm an execution workflow only after the
specification and plan are accepted. Neither Superpowers execution sub-skill is
invoked by this document. The next authorized action in this assignment is handoff,
not T0 or code generation.
