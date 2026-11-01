# T2 transport evidence â€” 2026-11-01

The approved plan's independent byte transport now implements one reader,
serialized whole-frame writes, bounded headers/bodies/admission/callbacks,
out-of-order response IDs, typed error replies, cancellation/deadlines, EOF
waiter failure and idempotent pipe cleanup. RpcClient.start() is called explicitly
by the future Session lifecycle; no subprocess launches from the transport.

Ten tests first failed at assertion level before lsp_transport existed.
All eleven transport tests now pass, including a later negative control:
an unexpected callback KeyError initially leaked a task and left the request to
TIMEOUT; the boundary now fails pending work as PROTOCOL_ERROR. It preserves
asyncio cancellation rather than converting it into apparent success.

Wire fixtures independently encode UTF-8 Content-Length frames. Tests cover
fragmentation/non-ASCII, coalesced/reversed responses, simultaneous writer drain
ownership, cancellation/late responses, timeout and EOF cleanup, malformed/
duplicate/missing/negative/oversized lengths, malformed JSON, invalid IDs and
conflicting response forms, unsupported methods and bounded pending admission.

A small invented fake_lsp peer is present for upcoming process tests. T2's passing
evidence uses controlled byte streams; no real ty, installed MCP process or Codex
semantic behavior is claimed. Transport-unit coverage is not G1 acceptance.

Observed on managed Python 3.14.10 / uv 0.13.6, Windows x86_64. Locked sync, all four hooks, source-independent build, outside-source artifact
verification and separate C901 src checks passed before the T2 commit.
Cognitive qualification and native-discovery gaps remain independent.
