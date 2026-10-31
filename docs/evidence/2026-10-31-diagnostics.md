# Pull diagnostics evidence — 2026-10-31

Task 6 adds the fourth actual MCP tool, diagnostics, using advertised
textDocument/diagnostic. The bounded resultId cache is keyed by canonical URI and
workspace generation; full reports replace it, unchanged reports require a matching
cache entry, and dependency generation changes clear it. Pull failures/malformed
reports propagate as errors, never a clean empty list. Original diagnostic ranges,
severity, code, source and message remain intact. Related documents retain identity
status with no external source reads. Optional context is saved-snapshot text.

Observed actual pinned ty tests: a typed consumer is clean; changing an unopened
provider's return type produces invalid-assignment at the consumer after restart;
repairing the provider restores an empty current report. A real MCP stdio invocation
also observes a local invalid assignment, then empty diagnostics after saved repair.
No readiness sleep or push-cache fallback. Unit tests exercise full/unchanged IDs,
unmatched reports, malformed pull result and generation cache invalidation.

This establishes diagnostic behavior on macOS in the synthetic fixture. It does
not establish mutation safety, Linux behavior, full Codex host acceptance or strict
engineering conformance. Cognitive qualification remains UNKNOWN.
