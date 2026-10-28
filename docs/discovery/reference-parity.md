# Reference baseline and functional parity assessment

Assessment: 2026-10-28. Status: source-grounded design input, **not runtime parity acceptance**.
This supersedes the initial reference-as-inspiration scope. The user now requires
all six documented tools as functional baseline, followed by corrections and ty
extensions. No reference source/tests/media are copied into the product.

## Immutable assessment inputs

| Input | Verified identity |
| --- | --- |
| Latest published release | [v0.1.1](https://github.com/isaacphi/mcp-language-server/releases/tag/v0.1.1), published 2025-05-16, commit `46e2950b7969334780675e7797e13f140d2d42ac` |
| Current default branch | `main`, commit [`e4395849a52e18555361abab60a060802c06bf50`](https://github.com/isaacphi/mcp-language-server/tree/e4395849a52e18555361abab60a060802c06bf50) |
| Release → main | One commit; only go.mod/go.sum changed: x/text 0.24.0→0.25.0, x/sync 0.13.0→0.14.0, go-spew reclassified direct. No tool, transport, lifecycle, documentation or test source changed |
| Behavioral reference | Published v0.1.1, assessed alongside current main; identical source does not prove dependency changes have no runtime effects |
| Local assessment | Clean detached upstream worktree; Go 1.27.3 darwin/arm64. Source inspection plus bounded unit-test execution |

The [machine-readable receipt](../evidence/2026-10-28-reference-assessment.json)
records exact revisions, source hashes, comparison and observed test scope.
Moving branch names are not implementation acceptance inputs.

Evidence vocabulary: **S** = source verified; **T** = test source inspected;
**E** = executed in this assessment; **U** = runtime behavior unverified here.
A registration/schema/snapshot is not a verified working capability.

## Six-tool parity matrix

All Python rows are REQUIRED DESIGN SCOPE / NOT IMPLEMENTED / NOT ACCEPTED.
Functional parity preserves user outcomes; it does not preserve unsafe behavior,
ambiguous resolution, JSON schema errors, prose bytes or configuration mechanisms.
The six names are retained; input schemas deliberately change as specified below.

| ID / tool | Upstream public contract and actual implementation (S) | Tests and evidence limit (T/E/U) | Independently defined Python behavior / acceptance |
| --- | --- | --- | --- |
| P1 `definition` | tools.go: required `symbolName`; promises complete implementation source. ReadDefinition calls workspace/symbol, filters exact/qualified names, opens files, uses document symbols and GetFullDefinition to extract numbered code, kind/container/ranges. It does **not** call textDocument/definition. Failed matches/source reads may be skipped and become a not-found success string | Python definition tests assert source substrings and snapshots; some method/static-method cases have `mayFail`. U for actual server execution here | URI/zero-based identifier position → textDocument/definition; return all resolved target locations and authorized workspace declaration source with explicit completeness. Function/class/nested/decorated/multiline constant fixtures must yield correct complete declaration text; null/external/unavailable source is marked, never invented. Name discovery uses workspace_symbols first. Prose/source formatting is not byte parity |
| P2 `references` | tools.go requires `symbolName`. FindReferences queries workspace/symbol, filters names, then uses `loc.Range.Start` in textDocument/references with includeDeclaration false. Groups file locations/context and renders 1-based text. `LSP_CONTEXT_LINES` can override context size | Python tests check names, minimum file count and snapshots; file counting uses output substrings. U for Go/ty. Known private identifier-position reproduction is user-supplied and not rerun | URI/position passed unchanged; explicit include_declaration false default; structured ranges and optional bounded context. Three synthetic consumer calls/imports, same-name decoys, includeDeclaration variants and direct-ty/adapter comparison must pass. No workspace-symbol-range inference or fixed offset |
| P3 `diagnostics` | tools.go declares `contextLines` as boolean but handler expects int, defaults to 5; filePath and showLineNumbers. GetDiagnosticsForFile opens file, sleeps 3s, calls pull diagnostic, discards result/errors except logging, then reads push cache. Can report no diagnostics without current pull data | Python tests cover clean/error files and dependency change, using sleeps, manual didChange/watched-files/reopen. U for server execution here | URI plus nonnegative integer context_lines and bounded source context. Use negotiated ty pull full/unchanged reports with resultId cache invalidation; never substitute absence of push for a clean result. Return diagnostics, severities/codes/source/ranges plus document hash. Error→repair→empty and dependency-edit cases prove freshness |
| P4 `hover` | filePath plus 1-based numeric line/column; handler accepts int/float and truncates to int, subtracts one, builds file:// by concatenation, returns MarkupContent.Value or line-based no-info prose | Python tests cover function/class/constant/invalid/no-info and snapshots. U for LSP execution here | URI/zero-based UTF-16 integer position; preserve hover content variants/kind/range and inferred signature/type text. Null is explicit. Reject booleans/fractions/negative/out-of-line/split-surrogate positions. No fabricated normalized type string |
| P5 `rename_symbol` | filePath/1-based line/column/newName. Skips prepareRename, calls rename, counts both WorkspaceEdit forms, directly applies edits through utilities.ApplyWorkspaceEdit. Returns occurrences/file prose; zero occurrences is a non-error failure string. No per-target authorization/hash transaction | Python tests check renamed constant in definition and consumer plus invalid positions; generic utility unit tests cover mocked edit/resource-op cases. U for actual rename/ty here | URI/exact position/new_name generates a complete bounded WorkspaceEdit preview; prepareRename when advertised. Apply only approved unchanged plan to authorized files. Verify definition/import/call changes and decoy preservation, version/hash conflicts, safe rollback/recovery and truthful commit result. Both changes and documentChanges text edits required; unsupported resource ops rejected as a whole |
| P6 `edit_file` | filePath plus edits[{startLine,endLine,newText}], 1-based inclusive line spans; omitted newText deletes. Converts line spans to LSP-like ranges, sorts descending, applies locally. getRange clamps some out-of-bounds inputs/EOF. Utility preserves detected newline style, checks overlaps, but slices Go string bytes and writes files directly | Mock utility tests exercise replacement/insertion/deletion/newlines/overlap and filesystem failures; integration text_edit tests use servers. U for end-to-end editing here | Existing authorized UTF-8 text file + end-exclusive UTF-16 range edits, explicit new_text including empty deletion. These ranges express every valid upstream line replacement/append/delete outcome. Preview then apply with base hashes; exact bytes, newline/EOF, adjacent edits, invalid/overlap/conflict/no-op and denied paths tested. No silent coercion/clamping, implicit create or partial-success message |

Upstream sources (same source bytes at release and main):
[registration/schema](https://github.com/isaacphi/mcp-language-server/blob/e4395849a52e18555361abab60a060802c06bf50/tools.go#L11),
[definition](https://github.com/isaacphi/mcp-language-server/blob/e4395849a52e18555361abab60a060802c06bf50/internal/tools/definition.go#L12),
[references](https://github.com/isaacphi/mcp-language-server/blob/e4395849a52e18555361abab60a060802c06bf50/internal/tools/references.go#L15),
[diagnostics](https://github.com/isaacphi/mcp-language-server/blob/e4395849a52e18555361abab60a060802c06bf50/internal/tools/diagnostics.go#L16),
[hover](https://github.com/isaacphi/mcp-language-server/blob/e4395849a52e18555361abab60a060802c06bf50/internal/tools/hover.go#L13),
[rename](https://github.com/isaacphi/mcp-language-server/blob/e4395849a52e18555361abab60a060802c06bf50/internal/tools/rename-symbol.go#L16),
[editing](https://github.com/isaacphi/mcp-language-server/blob/e4395849a52e18555361abab60a060802c06bf50/internal/tools/edit_file.go#L22),
[filesystem application](https://github.com/isaacphi/mcp-language-server/blob/e4395849a52e18555361abab60a060802c06bf50/internal/utilities/edit.go#L24),
[Python integration tests](https://github.com/isaacphi/mcp-language-server/tree/e4395849a52e18555361abab60a060802c06bf50/integrationtests/tests/python).

## Runtime/configuration assessment

| Concern | Actual reference mechanism (S) | Parity obligation versus correction |
| --- | --- | --- |
| Configuration/workspace | main.go parseConfig requires workspace and arbitrary LSP command plus trailing args; absolute path/executable lookup; global chdir; child inherits environment. LSP_CONTEXT_LINES and logging env settings exist | Keep one explicit workspace/process. Product uses reviewed JSON and fixed ty server argument vector, no environment application settings or global chdir. General server selection is excluded by the user's initial ty-only boundary |
| Initialize | Client constructs capabilities including gopls-oriented codelenses/options, sends initialized before registering callbacks, then sends initialized again; WaitForServerReady sleeps 1s | Register callbacks before initialize; advertise only implemented capabilities; initialized once. Per-server semantics/ready tests replace sleeps |
| Wire/request dispatch | Content-Length header/body JSON framing; separate unsynchronized header/body writes; response-channel map and atomic IDs; Call(ctx) blocks on channel without waiting on ctx; tool handlers pass long-lived s.ctx instead of incoming ctx | Own serialized byte framing, bounded input, out-of-order IDs, real cancellation/deadlines/EOF waiter failure. Do not preserve blocking or write interleaving as parity |
| Documents/workspace | OpenFile caches open URIs at version 1; NotifyChange increments versions and sends full text; close notifications; watcher fsnotify recursion, ignores/debounce and matching-file opens | Saved-file sync and changed dependency discovery are required outcomes. Startup scanning/opening strategy, watcher package/glob approximation and eager opening are choices, not required algorithms |
| Callbacks | workspace/configuration returns one empty map regardless of requested items; dynamic registration routes watchers; workspace/applyEdit applies server-supplied edits without tool-scoped authorization | Exact configuration response cardinality; only supported registration. Reject unsolicited applyEdit even when mutation tools enabled; explicit tool-controlled application only |
| Lifecycle | signals/parent-PID monitor; close files, shutdown/exit, wait with force-kill; timeouts wrap calls that may ignore ctx; Close uses competing close paths on forcedKill channel | One owner, bounded idempotent cleanup/reap and failure state; no transparent mutation retry. Potential shutdown races are source risks, not reproduced failures here |
| Errors/recovery | MCP text errors, some skipped source/diagnostic errors become success prose; no durable transaction or automatic LSP restart policy | Typed errors, distinguish empty/unsupported/stale/failure. Report server death and require session restart; durable write recovery without claiming cross-file OS atomicity |
| Hidden wider behavior | Generic WorkspaceEdit utility supports create/delete/rename resource operations, including recursive delete; code-lens implementation files exist but tool registration is commented out | Six public tools are baseline. No code-lens/execute-command/filesystem-management API. Reject resource ops in ty symbol-rename responses; explicit review boundary, not a hidden omission |

Sources: [main/lifecycle](https://github.com/isaacphi/mcp-language-server/blob/e4395849a52e18555361abab60a060802c06bf50/main.go#L38),
[client/sync](https://github.com/isaacphi/mcp-language-server/blob/e4395849a52e18555361abab60a060802c06bf50/internal/lsp/client.go#L51),
[transport](https://github.com/isaacphi/mcp-language-server/blob/e4395849a52e18555361abab60a060802c06bf50/internal/lsp/transport.go#L20),
[callbacks](https://github.com/isaacphi/mcp-language-server/blob/e4395849a52e18555361abab60a060802c06bf50/internal/lsp/server-request-handlers.go#L26),
[watcher](https://github.com/isaacphi/mcp-language-server/blob/e4395849a52e18555361abab60a060802c06bf50/internal/watcher/watcher.go#L157).

## Extensions and corrections, not additional parity tools

| ID | Capability | Classification / observable result |
| --- | --- | --- |
| S1 | Exact definition/references/hover/rename targeting | Correction to existing tools; positions flow unchanged and full declaration ranges never replace identifier selections |
| S2 | Document symbols | New MCP tool `document_symbols`; hierarchy and full/selection ranges preserved, flat server form normalized honestly |
| S3 | Workspace symbols | New MCP tool `workspace_symbols`; name-based discovery only, ambiguity retained; URI-only results not invented into positions; resolve when server supports it |
| S4 | Implementations | New MCP tool `implementations`; ty class/subclass/member-override meanings verified with real fixtures and unsupported handling |
| S5 | Type information | Existing hover's semantic result preserved; not a separate guessed-type tool or type inference engine |
| S6 | Diagnostic freshness and safe edits | Corrections necessary for functional parity to be trustworthy; not deferred polish |

No declaration/type-definition/call-hierarchy/completion/code-action tool or second
language server is added. LSP document symbols can be used internally for complete
source extraction before the public symbol tool is introduced.

## Observed tests versus unproven behavior

Executed on assessed main: `go test -json ./internal/logging ./internal/tools
./internal/utilities ./cmd/generate`, exit 0; four packages pass; 86 passing
test/subtest events and two skipped generator tests requiring another repository.
No upstream integration suite, watcher suite, Go bridge with ty, or Python runtime
was run. Dependencies downloaded only for this upstream temporary test checkout.

Source inspection limits: integration fixtures primarily call internal tool
functions, not MCP tools/call schemas; Python uses pyright, not ty. Snapshot helper
auto-creates missing snapshots, and some definition cases permit failure. Certain
text extraction unit tests exercise a copied test-local helper, not the production
function. No internal/lsp transport test files were found. None of this proves
correct MCP dispatch, cancellation, Unicode slicing, authorization or transactions.
Our acceptance suite must assert actual contracts at public boundaries.

## Licensing and attribution

Both assessed versions use BSD-3-Clause; root notice says `Copyright 2025 Phil
Isaac`, while the project is attributed here to Isaac Phi as requested. ATTRIBUTION
identifies Go Authors protocol generator material. No source port/copy is planned;
MIT project/starter notices remain. The comparison does not imply fork,
continuation, affiliation or endorsement. See [license review](licenses.md).
