# Early actual Codex feasibility — 2026-11-01

T4 checkpoint: installed production hover invocation and native approval/denial
are observed. Access to a supported Linux x86_64 write host is established.
The checkpoint permits continued implementation; it does not waive final H1–H3.

Machine-readable [source/fixture hashes and observed results](2026-11-01-codex-feasibility.json)
identify the final installed probe. Private raw transcripts remain uncommitted.

## Host and registration

Actual codex-cli 0.166.0 app-server on Windows x86_64, MCP SDK 2.3.0 and ty 0.0.95.
The adapter wheel was built and installed into a disposable environment outside
the checkout. An isolated Python import verified installed origin and SDK version.

Command-scoped native configuration registers only the checkpoint server entry
and per-tool hover approval_mode="prompt"; persistent Codex configuration, native
manager caches, global plugin defaults and hover's read-only annotation are not
changed. The ephemeral native thread has approvalPolicy="on-request",
approvalsReviewer="user" and sandbox="read-only".

Redacted launch:
- codex -c 'mcp_servers={gz_checkpoint={command="<installed-python>",
  args=["<transparent-stdio-witness>","<call-log>","<installed-gz-mcp-lsp>",
  "--config","<disposable-settings.json>"],tools={hover={approval_mode="prompt"}}}}'
  app-server --stdio
- The witness forwards bytes unchanged to the installed production console script;
  it records only incoming tools/call method/tool names in private disposable
  storage. It registers no additional tool and changes no product behavior.

The native protocol schema was generated from this exact installed Codex.
Current official [host configuration](https://learn.chatgpt.com/docs/extend/mcp#other-configuration-options)
and [app-server protocol](https://learn.chatgpt.com/docs/app-server) informed the
probe. A preliminary direct mcpServer/tool/call returned without approval; it is
installation evidence only. The model-driven path is required for approval proof.
An initial unsupported thread/stop cleanup call was corrected to the generated
thread/unsubscribe method; final app-server cleanup exited 0 without stderr.

## Redacted observed interaction

1. initialize → initialized → thread/start(ephemeral) → mcpServerStatus/list:
   gz_checkpoint exposes hover.
2. Direct native hover(main.py, {line:2,character:2}) returns schema_version=1,
   operation=hover, plaintext "int", range (2,0)..(2,5), saved hash/version and
   complete=true. It sends no native approval request.
3. Actual model turn requests this same hover once. Native
   mcpServer/elicitation/request arrives. The test client responds accept.
   The native mcpToolCall completes and returns plaintext "int".
4. A second actual model turn requests this hover once. Native approval request
   arrives; the test client responds decline. Codex reports approval denied.
   The transparent witness records two adapter calls before denial (direct plus
   allowed) and two afterward: denial sends zero tools/call requests to the adapter.
5. thread/unsubscribe and parent EOF cleanly end app-server, exit 0.

These are real native approval protocol interactions answered programmatically by
the test client. No GUI click or human-action claim is made. They establish that
the actual host exposes the interaction required for later operator-driven tests;
they are not safe-mutation acceptance.

## Supported write-host access and remaining gates

Existing Ubuntu-26.04 WSL2 provides Linux x86_64 with a native Linux filesystem.
A disposable saved-file replacement and directory fsync probe succeeds. A
hash-verified PyPI uv 0.13.6 Linux wheel provisions managed CPython 3.14.10 using
the project's pinned download metadata. Its full product gate and installed
SDK→adapter→ty hover pass on native Linux storage. Windows remains unsupported
for adapter writes.

WSL discarded /tmp artifacts between launches; test-owned scratch under the
Linux user's cache retains this isolated runtime. No system packages, global uv
installation or user defaults were changed. The selected uv wheel SHA-256 is
22759b8895e1103578de6fb4cd27e94b4399d021023378d29f01333717751fba.

T11 will register the installed Linux adapter through wsl --distribution
Ubuntu-26.04 --exec <installed-console> with a Linux-local synthetic workspace and
private state directory, and repeat actual rename/edit approval, denial, exact
file assertions and fresh semantics. That bridge, actual mutation behavior,
macOS arm64 write evidence and complete nine-tool H1–H3 remain unverified.
The early read-only approval result substitutes for none of those gates.
