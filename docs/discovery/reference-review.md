# Initial reference implementation review — 2026-10-28

Historical initialization review. The [revision-2 parity assessment](reference-parity.md)
supersedes its read-only/inspiration scope. Correction: code-lens source exists but
its tools.go registration is commented out; only the six documented tools register.

Reviewed [Isaac Phi's mcp-language-server v0.1.1](https://github.com/isaacphi/mcp-language-server/tree/v0.1.1),
commit `46e2950b7969334780675e7797e13f140d2d42ac`; release publication verified
through gh (2025-05-16). Source was inspected in a separate temporary checkout.
No source, protocol generator, fixture, snapshot or media was copied or ported.
This is architectural observation, not an execution audit or an upstream patch.

| Area | Observed at v0.1.1 | Consequence for independent proposal |
| --- | --- | --- |
| Composition | main.go parses workspace/LSP executable and args; constructs client/watcher, initializes LSP before serving MCP | Keep startup orchestration explicit, avoid global chdir and separate protocol from lifecycle |
| MCP | mark3labs/mcp-go stdio, recovery/logging; tools.go registers definition, references, hover, diagnostics, rename_symbol, edit_file (code-lens registration is commented out) | Use official Python SDK; revised parity includes guarded mutations and diagnostics |
| Semantics | Definition/references locate named workspace symbols; hover takes a location; text rendering reads source context | Canonical URI/position queries; structured locations instead of ambiguous name matching or full-code extraction |
| Wire | internal/lsp/transport.go reads Content-Length headers and JSON bodies, dispatches request/notification/response IDs to handler maps/channels | Independent byte-counted framing, serialized writes and bounded reads; no Go protocol-code reuse |
| Requests | atomic IDs and pending-response map; Call accepts context but waits on the response channel without selecting ctx cancellation | Deadlines/cancellation must actually unblock pending work; EOF must fail every waiter |
| Server requests | Registered configuration/capability/applyEdit handlers; generated protocol/method wrappers | Implement only justified callbacks; reject applyEdit; register handlers before initialize |
| Documents | open-file map/versioning and didOpen/didChange/didClose; watcher scans workspace, fsnotify and debounce/filter logic | Preserve sync semantics without eagerly opening an unbounded workspace; freshness design needs proof |
| Readiness/lifecycle | one-second readiness sleep; signal and parent-PID handling; close files, shutdown, exit, close pipes/wait with forced-kill timer | Negotiate readiness, bounded shutdown and deterministic task/process reaping; avoid sleep-as-readiness |
| Tests | Go unit tests plus actual language-server integration workspaces and output snapshots; Python references use pyright; snapshot regeneration uses UPDATE_SNAPSHOTS | Use unittest with semantic assertions and pinned ty; snapshots cannot alone prove identifier targeting |

## Verified defect mechanism

[`internal/tools/references.go`](https://github.com/isaacphi/mcp-language-server/blob/v0.1.1/internal/tools/references.go)
first calls workspace/symbol, filters names and uses the returned location's
range start as the references request position. That range need not identify the
identifier. For a Python declaration beginning `def`, column zero may query the
keyword. The supplied private-project observation (column 0 empty, column 4
three references) is user-provided evidence; it was not rerun against private
sources during this work.

Our proposed public regression uses a newly invented shared package and three
consumer packages. No private sources or line padding will be transplanted.
Definition coordinates must distinguish a full declaration range from its
identifier selection range. Requests pass the caller's explicit identifier
position unchanged; symbol search is discovery, never implicit name resolution.

## Official specifications inspected

- [LSP 3.17 specification](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/): Content-Length counts bytes; requests can receive responses out of order; initialization/capabilities, zero-based positions, UTF-16 default/negotiation, document sync and shutdown/exit define separate contracts. A symbol's selectionRange is distinct from its full range.
- [ty language-server documentation](https://docs.astral.sh/ty/features/language-server/): all six candidate operations are documented, including implementation. This is documentation support, not adapter acceptance or a live initialize receipt.
- [Official MCP Python SDK](https://py.sdk.modelcontextprotocol.io/), [run](https://py.sdk.modelcontextprotocol.io/run/), [lifespan](https://py.sdk.modelcontextprotocol.io/handlers/lifespan/), [structured output](https://py.sdk.modelcontextprotocol.io/servers/structured-output/): v2 uses MCPServer, supports stdio, typed lifespan context and schema-based structured results. Latest release verified as v2.3.0; no SDK runtime was installed into this product.
- [Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp): stdio executable/args, project configuration under native trust, startup/tool timeouts. Registration example is proposed and not tested against a gz-mcp-lsp server.

Do not infer v2 SDK API behavior from old FastMCP snippets. Before implementation,
review the selected tag's code/signatures and test its Python 3.14 schema and
cancellation behavior. Current online documentation may move independently of tags.
