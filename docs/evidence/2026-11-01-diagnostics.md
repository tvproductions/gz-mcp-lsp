# T6 current pull diagnostics — 2026-11-01

The production diagnostics tool uses advertised textDocument/diagnostic and
returns the complete current normalized list. No push cache, readiness sleep,
automatic retry or failed-pull-as-clean path is used. This is local P3/S6
development evidence; nine-tool/native-host/platform completion remains gated.

Managed CPython 3.14.10, uv 0.13.6, MCP SDK 2.3.0 and ty 0.0.95 are unchanged.
The protocol implementation was checked against the official
[pull-diagnostic specification](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_diagnostic)
and [Diagnostic definition](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#diagnostic).

## Observed behavior

Six initial unit assertions failed before diagnostics.py existed; the four-tool
SDK catalog assertion failed before registration. Nine diagnostic unit tests now
cover full/unchanged resultId handling, unmatched/mismatched reports, pull errors,
malformed reports, repair/dependency invalidation, returned-object cache poisoning,
related local/full/unchanged identities, per-call context and external no-read rules.

Full reports preserve exact URI/range, severity/code/source/message, tags, code
description and related information. Results are deterministically ordered.
Opaque code-action data is not requested or exposed. A matching unchanged report
expands the same cached full list only for the same saved hash/generation/resultId.
Missing/mismatched state is PROTOCOL_ERROR; unsupported pull is UNSUPPORTED.

The cache is bounded by configured reader capacity and byte-bounded reports.
Entries commit only after final manifest validation and contain copied base items,
without source context. Context is selected anew on each request. Related local
reports require their own saved identity; external reports remain marked metadata
and never trigger external reads. Source/context overflow is RESULT_LIMIT.

Installed SDK stdio → production adapter → actual ty independently verifies:
- value: int = 'wrong' returns one invalid-assignment error from ty, severity 1,
  range (0,13)..(0,20), with the exact saved source context.
- Repeating the pull returns the same complete list. Saving value: int = 1 yields
  a new generation and a genuinely empty pulled list.
- A consumer initially accepting an unopened dependency's int return has no errors.
  Changing only that return annotation to str yields a new generation and the
  expected consumer invalid-assignment at (2,13)..(2,21).

tests/fixtures/diagnostic_cases.json independently specifies source/fix/dependency
bytes and expected diagnostic positions/codes; erroneous Python is materialized
only in disposable integration workspaces.

## Generation corrections exposed by caching

Two additional document regressions failed before correction:
- Replacement transport with an unchanged scan digest reused the old generation.
  Generation now combines the scan digest and an advancing session epoch. Every
  replacement therefore invalidates transport-bound resultIds, including after a
  committed file outside Python indexing.
- A semantic document absent from the scan could be opened and called fresh.
  One Workspace.tracked predicate now controls scan membership and semantic
  document admission. Untracked semantic documents return UNSUPPORTED. The lower
  Workspace saved-byte reader remains available to the guarded existing-file
  edit planner; this does not narrow the approved edit_file scope.

Workspace target scope and pure envelope/budget helpers are shared with navigation;
diagnostics does not depend on the Navigation service. All earlier generation,
source, installed navigation and SDK controls remain in the routine suite.

Both full Windows/Linux gates pass with all 106 discovered tests. C901 src
and the scoped portability audit pass. [Source/fixture/artifact hashes](2026-11-01-diagnostics.json)
identify these inputs; the local task ledger records the commit. macOS arm64, hosted CI and full actual Codex H1-H3 remain
UNKNOWN/NOT ACCEPTED; this receipt is not mutation or release acceptance.
