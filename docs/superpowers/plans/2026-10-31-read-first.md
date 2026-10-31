# Read-First Delivery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans. The user selected native inline execution, a single writer and one bounded package per handoff. Do not delegate implementation or automatically advance to the next package.

**Goal:** Prove seven read capabilities in actual Codex, then stop before the
separate write-parity milestone.

**Architecture:** Retain the existing official MCP SDK boundary, exact-position
semantic operations, saved-document generations and single ty subprocess.
Keep unfinished write components outside the read composition; later write
parity uses the same semantic core.

**Tech Stack:** Managed CPython 3.14.10; uv/uv_build 0.13.6; Ruff 0.17.3;
ty 0.0.93; pre-commit 4.7.0; mcp 2.3.0; pydantic 2.14.2 at the MCP boundary;
unittest, project lock and src packaging. Verify the effective existing pins;
this plan does not upgrade dependencies.

**Spec:** [Approved read-first design](../specs/2026-10-31-read-first-milestones-design.md),
[revision-2 contracts](../specs/2026-10-28-semantic-navigation-design.md),
[milestone acceptance](../../discovery/acceptance-matrix.md).

**Status: APPROVED on 2026-10-31.** The user reviewed this plan in conversation,
confirmed write-enabled configuration rejection and repository dogfooding, then
approved it with “looks good”. Execute R0 only in this bounded package.
It supersedes the older
plan's execution order, catalog assertions and single terminal acceptance gate;
unchanged task contracts remain references. Existing receipts and completed
task IDs are retained. T8 is incomplete and paused, not skipped as a passing gate.

## Global Constraints

- One canonical workspace, one live ty process, MCP/LSP stdio only; saved-disk inputs.
- Exact zero-based UTF-16 identifier coordinates; full/selection ranges distinct.
- Read catalog: definition, references, hover, diagnostics, document_symbols,
  workspace_symbols, implementations. Full-parity catalog later adds rename_symbol/edit_file.
- No source writes, mutation previews, transaction initialization or recovery at
  read-server startup or invocation. No unsolicited LSP applyEdit, code actions,
  execute-command, generic filesystem tool, second server or request-time install.
- Project JSON application settings; no environment overrides. Preserve native
  host configuration formats, lite governance, disabled Backplane and numeric ceilings.
- Preserve the three T9 drafts at their original paths and their Git-common backup
  manifest. Never reset/clean, overwrite, silently accept or fix them in a read package.
- Four-hook gate and separate applicable engineering acceptance remain required.
  Required UNKNOWN/FAIL/stale evidence blocks its conclusion. Cognitive qualification
  is still unresolved; complexipy is not a substitute or passing authority.
- Initial read validation targets are macOS arm64 and Linux x86_64. Claim only
  observed platforms. Linux write/recovery evidence belongs to the later write gate.
- No push, release/tag publication or actual host configuration change without
  applicable authorization. Approval of this plan does not publish anything.

## Review Focus

1. A write-enabled JSON setting must fail before starting ty or touching recovery
   storage; seven-tool discovery alone does not prove this boundary — R0.
2. A workspace symbol containing only a URI must never become an invented identifier
   coordinate, including with duplicate names — T10.
3. Installed tests must import the built distribution, while preserved untracked
   T9 drafts must not silently enter the passing candidate — R0/T11.
4. Saved dependency/config changes and child failure must invalidate results and
   reap ty through actual host calls — T11, existing T4–T6 evidence.
5. Read capability acceptance must not imply complete reference parity or waive
   unresolved engineering gates — T12/T13.

---

## Workspace and file ownership

The preserved worktree is `~/.codex/worktrees/359d/gz-mcp-lsp`, branch
`implementation/reference-parity`, checkpoint `2685a9c982fe35328608deab0e6188aa53b34fe7`.
Keep this as the single implementation workspace. Before executing, verify current
HEAD/status and the source/draft hashes recorded in the T8 receipt and backup manifest.

For whole-candidate verification, use an isolated snapshot containing only tracked
candidate files, including the reviewed current changes. Keep the source worktree
and T9 drafts untouched. Record snapshot inventory/hashes and import origin. A
failure in any tracked test is a candidate failure; do not narrow the required
gate, change discovery or suppress tests to obtain a pass. Untracked T9 drafts
are explicitly future work, not evidence for this candidate. Use normal hooks on
the actual commit candidate; if hooks require temporary draft isolation, use the
existing byte-verified archive/restore procedure and verify restoration afterward.

| Files | Responsibility |
| --- | --- |
| config.py, cli.py, mcp_api.py; test_config.py, test_mcp_api.py | R0 read composition, configuration refusal and catalog boundary |
| navigation.py, mcp_api.py; test_symbols.py, integration/test_symbols.py | T10 semantic discovery and implementation wrappers |
| tools/verify_distribution.py, test_distribution.py, integration/test_installed_server.py, docs/examples/, CI | T11 installed read behavior, platform and actual host evidence |
| pyproject.toml only for justified analyzer contracts; docs/evidence/ | T12 effective policy and independent acceptance evidence |
| README, ROADMAP, CHANGELOG, docs/handoffs/ and acceptance matrix | T13 accurate read result, remaining write work and deliberate stop |

Paths without a prefix in this table are under `src/gz_mcp_lsp/` or `tests/`
according to their role. Retain existing modules rather than adding a framework.

## Package R0: enforce and prove the read-only composition

**Interfaces:** preserve `load_config(path: Path) -> Config` and
`create_server(config: Config, session: Session) -> MCPServer`.
User-confirmed review decision: the read composition rejects
`mutations.enabled=true` with domain error `UNSUPPORTED`, including a programmatically
constructed Config, before starting a child or opening transaction state. Disabled
configuration remains compatible. Do not remove persisted settings or write modules.

- [x] Add assertion-level negative controls in tests/test_config.py and
  tests/test_mcp_api.py: `test_read_server_rejects_enabled_mutations_before_startup`
  expects `UNSUPPORTED`, zero subprocess launches and no state directory creation;
  `test_read_server_never_initializes_transactions` fails if Transactions is
  constructed on read startup/call. Retain the current four-tool catalog test;
  assert rename/edit calls are unregistered and source hashes unchanged.
- [x] Run each focused unittest file and observe the intended assertion fail before
  changing runtime code: `uv run --locked python -m unittest discover -s tests -p test_config.py -v`
  and the same command with `test_mcp_api.py`. An import/setup failure is not a red control.
- [x] Enforce the boundary in config/CLI/composition at existing seams. Keep
  transaction code unreachable; do not modify filesystem.py or any T9 draft.
- [x] Run the focused tests green, then the complete candidate gate below. Verify
  draft hashes and the candidate inventory; commit only reviewed R0 changes with
  normal hooks and record a bounded handoff. Stop before T10.

## Task 10: complete the three read extensions

**Interfaces:** Navigation gains `async document_symbols(uri: str) -> Result`,
`async workspace_symbols(query: str, resolve: bool = False) -> Result`, and
`async implementations(uri: str, position: Position) -> Result`.
Reuse existing document-symbol source support and SDK result/error wrappers.

- [ ] Extend tests/test_symbols.py and tests/integration/test_symbols.py with
  `test_nested_symbol_ranges`, `test_uri_only_symbol_never_guesses_position`,
  `test_duplicate_names_preserved`, `test_implementation_supported_empty_unsupported`,
  and `test_exact_read_tool_catalog`. Assert full versus selection ranges, honest
  unresolved symbols, stable ordering, result limits, capability checks and exactly
  the seven names in Global Constraints. Assert all annotations are read-only and
  no rename/edit preview or executor is callable.
- [ ] Run `uv run --locked python -m unittest discover -s tests -p test_symbols.py -v`
  and observe assertion-level failures, then implement the methods and wrappers
  in navigation.py/mcp_api.py. Preserve exact caller coordinates and strict inputs.
- [ ] Run unit tests green and
  `uv run --locked python -m unittest discover -s tests/integration -p test_symbols.py -v`
  through pinned ty/MCP with nested declarations, duplicate names and subclass/member
  overrides. Missing ty fails; no acceptance skip. Keep P1–P4 regressions green.
- [ ] Run the complete candidate gate, record S2–S4 evidence and seven-tool inventory,
  commit with normal hooks and hand off. This is no claim of actual Codex acceptance.

## Task 11: installed read distribution and actual Codex acceptance

**Interfaces:** installed CLI `gz-mcp-lsp --config PATH`, official SDK stdio client
and actual Codex using that same preinstalled executable. Retain host-native formats.

- [ ] Extend distribution/installed-server tests with a failing seven-tool catalog
  and semantic assertions for every read tool; assert outside-source import origin,
  runtime-only dependencies and notices. Add enabled-write startup refusal and
  unregistered-mutation tests with unchanged source hashes and absent recovery storage.
- [ ] Build without sources, install the wheel outside the checkout and run actual
  pinned ty scenarios. Extend verifier/CI as needed for required read coverage on
  macOS arm64 and Linux x86_64, preserving four hooks and no request-time installation.
- [ ] Prepare a concrete read-only Codex profile under docs/examples/ and obtain
  any needed host-configuration authorization before changing an active profile.
  In actual Codex, discover and invoke all seven tools with asserted semantic content.
  Dogfood this repository's Python adapter, tests and engineering tools as the
  primary practical workspace. Record the candidate revision and actual workspace
  manifest, including any preserved drafts, without accepting those drafts as
  runtime implementation. Starting with a symbol query, select a returned identifier
  position and trace a real cross-module definition/reference path; verify hover,
  diagnostics, document hierarchy and supported implementation results against source.
  Keep exact edge-case assertions in synthetic fixtures; empty results are valid
  when the queried real code has no implementations or diagnostics.
  Record host version, trust, executable origin, exact coordinates and transcript;
  SDK calls alone do not satisfy H1/H3.
- [ ] Observe saved-source/dependency/config changes and timeout/ty-death/EOF cleanup;
  use a disposable copy of this repository for change/failure scenarios so dogfood
  acceptance does not alter implementation work or the preserved T9 drafts.
  assert current generations, no orphan child and unchanged source bytes from read
  calls. H1/H3 remain UNKNOWN when a required host interaction is unavailable.
- [ ] Run the complete candidate gate, retain sanitized per-platform receipts,
  commit with normal hooks and hand off. H2 write approval remains future work.

## Tasks 12–13: read engineering assessment, human acceptance and stop

- [ ] Run the existing T12 affected-input engineering checks for this candidate,
  including shipped dormant code; keep original ceilings and scope evidence.
  Check effective interpreter/tool/configuration provenance, native discovery,
  dependencies/licenses and installed artifacts. Record cognitive qualification
  separately; do not mark strict E3/E4 accepted while it remains unresolved.
- [ ] Reconcile each read-required P/S/C/D/H/E assertion with exact receipts and
  supported read platforms. Deferred W/H2/commit assertions are future requirements,
  never PASS or silently deleted. Rerun relevant checks if candidate bytes changed.
- [ ] Update product docs and handoff with read capability status, engineering status,
  remaining write parity, exact commit/candidate hashes and unobserved host/platform
  gaps. Obtain human acceptance of the measured read result; withhold any blocked
  conclusion. No claim that seven tools equal full reference parity.
- [ ] Stop after the bounded handoff. Preserve T8/T9 and backups; do not start writes
  automatically, even if read tests pass. No release/tag publication.

## Complete candidate gate

Use uv 0.13.6 in nested hooks, CPython 3.14.10 and normal pre-commit execution:

```bash
uv sync --locked --all-groups
uv run --locked pre-commit run --all-files
uv build --no-sources
uv run --locked python tools/verify_distribution.py
```

The gate must pass on the exact separately reviewable candidate. Use the preserved
Git synchronization policy when synchronization is authorized; a local commit is
not remote backup, exact-commit CI or SHA alignment. No implementation push is
authorized by the existing handoff. Report those observations separately.

## Later milestone: resume T8/T9 and full parity

Requires a new instruction after the read handoff. Revalidate T7 and the preserved
T8/T9 work, settle metadata policy explicitly, prove private recovery storage and
macOS/Linux write/recovery behavior, then finish T8 and T9 under their existing
safety contracts. Extend catalog assertions to nine and rerun all read regressions.
Complete the write portions of T11 (including actual host approval/denial), T12
and T13. All required parity/write/engineering gates must pass before claiming
full reference parity. Keep the finite scope and deliberate stop.

## Self-review

Design coverage: R0 owns read-only composition; T10 owns the three missing reads;
T11 owns installed/host/platform proof; T12/T13 own separate acceptance and stop;
T8/T9 and later T11 retain all deferred write requirements. Interfaces reuse the
existing domain/SDK seams. Every Review Focus item has an owning test or evidence
step. No runtime implementation, dependency change or acceptance PASS is supplied
by this plan. Preserve the selected inline execution method and bounded pacing.
