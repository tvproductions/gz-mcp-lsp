# T11 — installed distribution and actual Codex acceptance

The user requested completion of T11 after T10 commit `a71bcd4`, then clarified
that accepted branches and worktrees must be consolidated on main and removed.
This is the bounded T11 record, not T12 engineering closure, T13 whole-branch
acceptance or a release. The [sanitized native receipt](2026-11-01-codex-acceptance.json)
contains source/fixture hashes, tool inventory, approval outcomes, failure cases
and private-transcript hashes. Raw host transcripts and disposable state remain
private and untracked.

## Distribution and installed contract

The archive verifier now rejects missing CLI code, typing resources, wheel license
notices and source license notices as well as its existing dependency/entry-point/
identity/leakage checks. Negative controls first demonstrated three accepted bad
archives (CLI code, LICENSE and NOTICE missing), then passed after correction.
No new runtime dependency, environment setting, capability or launcher API is added.

The installed-server suite builds a wheel and installs only the locked runtime
graph outside the checkout, before requests. It asserts exact resolved environment
origin and absence of Ruff/pre-commit/coverage/test-package masking. A synthetic
shared_runtime package defines run_shared_cli at (0,4). Three importing/calling
packages have imports at (0,27) and calls at (2,9); expected coordinates are
independently enumerated in expected.json. A same-name decoy is preserved.

One disabled server exposes exactly nine tools. All seven read tools have semantic
assertions: complete declaration source and exact target selection, three consumer
calls plus three imports and declaration, hover name/type text, current empty
diagnostics, document-symbol selection, ambiguous workspace symbols and real
member implementation locations. Both mutation tools reject apply while disabled,
with all recursive workspace hashes unchanged. Supported POSIX lanes then preview
and apply rename across the definition/three imports/three calls, apply an exact
edit, verify every Python file and query fresh post-edit declaration source.

The four routine hooks are unchanged. CI now prints verbose test results so the
platform skip inventory is visible. Windows has 26 explicit POSIX-only exclusions;
POSIX skips the Windows-only unsupported-write test. Missing ty is never a skip.

## Actual native host and approval proof

Observed codex-cli 0.166.0 app-server on Windows AMD64 launches the actual installed
Linux console through WSL Ubuntu-26.04. The workspace and private transaction state
are on native Linux local storage. Managed CPython 3.14.10, uv 0.13.6, MCP SDK 2.3.0
and ty 0.0.95 retain their execution pins. This resolves the previously unverified
Windows-host/Linux-adapter bridge; Windows adapter writes remain unsupported.

Command-scoped native configuration registers one acceptance server; it does not
edit persistent Codex configuration, caches or unrelated defaults. The launch is:

```text
codex -c '<isolated mcp_servers table>' app-server --stdio
  -> wsl.exe --distribution Ubuntu-26.04 --exec <installed-python>
     <private-transparent-witness> <private-call-log> <installed-gz-mcp-lsp>
     --config <disposable-settings.json>
```

The witness forwards bytes unchanged, records tool-call names/arguments privately
and exposes owned PIDs for cleanup assertions. It adds no tool and does not alter
product behavior. The installed adapter has the same runtime source identity as
the installed SDK artifacts, with source hashes in the linked receipt.

A fresh ephemeral native session semantically asserts all seven read tools and
both disabled mutation denials. A separate model-driven native turn invokes every
read tool exactly once and asserts post-mutation source, seven reference sites,
hover text, diagnostics, document/workspace symbols and implementation locations.
This is actual Codex execution, not a direct SDK substitute or a catalog-only test.

In a fresh operator-enabled native session, actual model turns request:

1. rename_symbol preview: native accept, no target writes.
2. rename_symbol apply: native decline, unchanged recursive hashes and **zero
   additional tools/call messages to the adapter**.
3. The same retained rename apply: native accept, exact definition/three-import/
   three-call changes, with the same-name decoy unchanged.
4. edit_file preview: native accept, no target writes.
5. edit_file apply: native accept, exact after-bytes and fresh declaration source
   containing the renamed function and `return value + 2`.

These are real mcpServer/elicitation/request decisions answered by the disposable
test client. The decisions are programmatic native host acceptance, **not GUI or
human-click evidence**. No model-supplied consent flag or plan token is treated as
approval. Native protocol decisions and operator filesystem authority are separate.

Current official [MCP configuration](https://learn.chatgpt.com/docs/extend/mcp) and
[app-server approval protocol](https://learn.chatgpt.com/docs/app-server) were
searched and opened on this execution date. Per-tool approval_mode="prompt" is
configured for both mutation tools; ephemeral threads select approvalPolicy=
"on-request", approvalsReviewer="user" and read-only host sandbox. Direct native
calls are used for precise read/failure assertions; model turns prove approval
interaction and all read-tool invocation. See the isolated
[WSL host example](../examples/codex-wsl.toml) and
[operator settings template](../examples/write-settings.json).

## Host failure and process ownership

Independent actual-native-host sessions exercise three failures after a successful
hover proves the real adapter/ty are ready:

| Scenario | Observed result | Files and cleanup |
| --- | --- | --- |
| Suspend only disposable ty; host tool timeout 2 seconds | Native timeout at 2.02 seconds | Hashes unchanged; resume ty, close host; adapter and ty reaped |
| Kill only disposable ty | Typed SERVER_EXITED | Hashes unchanged; adapter and ty reaped |
| Kill only disposable adapter | Native transport closed | Hashes unchanged; ty exits on EOF; both reaped |

Normal thread unsubscribe and parent EOF also close/reap the adapter and ty.
Every observed app-server exits 0. PID existence checks use the actual owned
processes, not arbitrary process-name cleanup. There is no forced termination of
unrelated applications.

## Gates, review and remaining authority

Local Windows and native Linux complete the four-hook gate, source-independent
sdist→wheel build and outside-source distribution verification. Source C901 remains
at the adopted ceiling 20. The final suite and review results are recorded in the
stage handoff and final synchronization response. The existing hosted platform
matrix executes the same contract on Linux x86_64, macOS arm64 and Windows AMD64;
the **exact final commit's run and platform job results** must be observed before
T11 is reported accepted. Earlier T9/T10 CI is not substituted. The final response
provides the immutable commit/run receipt without a receipt-only commit chain.

The focused fresh-context T11 review reported no substantive findings and verified
source, fixture and private-transcript hash consistency. Its independent test run
was blocked by sandbox cache/temp permissions; the passing gates are the
implementer's and CI's observations. One local pre-commit run observed concurrent
documentation edits and correctly returned nonzero despite 186 passing tests;
the unchanged final candidate is rerun through normal hooks before commit.

H1-H3 now have actual-host evidence; E2 has installed/source-independent evidence.
Programmatic approval proof is explicitly bounded above. T12 cognitive qualification
remains UNKNOWN, native discovery retains its separate duplicate/global-scope FAIL,
and T13 fresh whole-branch review remains outstanding. Routine/native/Git success
does not waive those requirements or accept the full milestone. Stop before T12.
