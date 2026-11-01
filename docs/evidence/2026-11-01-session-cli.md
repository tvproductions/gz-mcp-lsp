# T3 one-child lifecycle and MCP CLI â€” 2026-11-01

The approved plan's T3 adds Session, official SDK composition, cli.py/__main__.py
and the sole console entry gz-mcp-lsp. The intermediate catalog is deliberately
empty until T4 supplies the production hover operation; no semantic success stub
was registered. G1 remains unaccepted.

Session owns one provisioned [ty_executable, "server"] process with pipes and child
cwd, callbacks installed before initialize, UTF-16 negotiation, a bounded stderr
tail/drain, child/wire supervision and bounded shutdown/terminate/kill/reap.
Unexpected failure does not restart or replay requests. Only explicit generation
restart may launch a replacement, and it rejects any unreaped prior child.

Negative controls were observed before lifecycle/composition implementation and
before the archive guard enforced the console entry. Further demonstrated failures
were fixed before commit: exec errors now become deliberate SERVER_EXITED errors;
a failed reap remains FAILED and closes pending transport work; restart cannot
launch a second child after failed reaping; SDK task-group lifespan failures are
unwrapped to source-free CLI errors rather than a traceback.

Observed on managed CPython 3.14.10 / uv 0.13.6, Windows x86_64:

- Ten synthetic-process Session tests cover early configuration/applyEdit callbacks,
  exactly-once initialization, denied unsolicited edits, failed/hung/unsupported-
  encoding startup, cancellation, duplicate/timeout cleanup, stderr flood,
  protocol failure, exec failure and failed-reap/restart behavior.
- Three actual pinned-ty integration tests initialize and observe its child exit,
  negotiate/list through the real MCP stdio CLI and close parent stdin, and prove
  invalid-child CLI startup returns typed source-free JSON on stderr.
- One SDK composition test proves the production lifespan and empty intermediate
  catalog, including unknown-tool rejection.
- Eleven distribution tests preserve dependency/leakage guards and require the
  sole console entry. Outside-source clean installation verifies the installed
  command's --help and typed missing-configuration rejection.
- All 54 tests and the four routine hooks pass. Source-independent build and
  outside-source installed checks pass. No semantic query or actual Codex tool
  invocation is claimed at T3.

RpcClient.wait_failure supplies Session supervision even without a pending request.
A narrow constructor-only spawn seam permits test subprocess substitution; JSON/CLI
does not expose arbitrary commands or server arguments. Cleanup evidence uses real
process handles, not a mocked return code. The failed-reap path uses explicit
fault injection and independently kills/reaps its test children during cleanup.

The CLI accepts only --config PATH (and argparse help); it fixes transport to
stdio and uses the official SDK's stdio lifespan. No request-time installation,
listener, environment-based application configuration or enabled write machinery.
T9 still owns production recovery admission integration.

Linux/macOS lifecycle proof, T4 saved-file/generation/hover correctness and actual
Codex feasibility remain required. Native scope FAIL and cognitive qualification
UNKNOWN continue to block strict final acceptance.
