# Pure edit planning evidence — 2026-10-31

Task 7 implements immutable content-bound previews, with no source/state filesystem
effects. Both text WorkspaceEdit forms are accepted independently; resource
operations, contradictory forms, aliased/duplicate targets, document version
conflicts, overlapping ranges and coincident insertions reject the whole plan.
Confirmation annotations and complete base identity/hash/version/after bytes are
bound to the digest. Preview identity does not represent host or human consent.

Observed tests preserve exact UTF-8 bytes, UTF-16 astral characters, CRLF, mixed
CR/LF/CRLF, adjacent edits, insertion/deletion/replacement and explicit EOF append.
Every range addresses the original snapshot; no clamping or shifted edits. Byte,
file and edit count ceilings reject before oversized result allocation. Filesystem
open/replace negative controls demonstrate pure planning has no effects.

Two regressions first failed: lone-CR coordinates and an over-limit after-image.
The shared mapper now recognizes exactly LSP CRLF/LF/CR delimiters; AST source and
synchronization EOF reuse it. Allocation/count checks occur before joining output.
The full gate also exposed help startup latency: a negative subprocess test proved
help loaded MCP before parsing. Protocol imports are now deferred until settings
validation; existing timeouts were retained.

Routine gate, build, clean installed actual-ty MCP hover, C901 and Lizard pass.
Lizard's 22-branch edit-set parser was split at annotation validation; thresholds
and checker unchanged. No filesystem commit, recovery or mutation tool is enabled
by this task. Cognitive qualification and actual Codex acceptance remain incomplete.
