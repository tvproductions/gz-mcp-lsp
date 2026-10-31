# Process and byte-transport foundation — 2026-10-31

Approved implementation worktree, Tasks 2–3. Independent stdlib JSON-RPC transport
and single-process lifecycle now exist. No reference source copied.

Observed byte-boundary tests: fragmented Unicode, complete serialized frames,
out-of-order correlation, deadline-bound admission, timeout/cancellation cleanup,
late responses, EOF, missing/duplicate/negative/oversized lengths, invalid response
IDs and malformed JSON. Callback configuration cardinality and unknown-method errors
are exercised. Seven transport tests pass.

Observed subprocess tests: initialize/initialized once, callbacks ready during
initialization, unsolicited applyEdit refused, startup crash reaped, shutdown hang
bounded, restart reaps old child before spawning, parent stdin EOF exits without
stdout log bytes or orphan child. Four process tests pass. Two SDK/CLI composition
tests pass; the intermediate catalog advertises no unimplemented operations.
Actual MCP stdio negotiation and ty semantic correctness remain Task 4 work.

Ruff/format, ty, unittest, sdist→wheel build and clean installed import/CLI verification
passed. C901 and Lizard checked separately against project ceilings; cognitive
qualification is still unavailable and strict engineering acceptance remains blocked.
No Linux portability or semantic/host acceptance is inferred from these macOS tests.
