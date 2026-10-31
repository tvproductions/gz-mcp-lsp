# T1: configuration, workspace and coordinates — 2026-10-31

Approved implementation in native isolated worktree, branch implementation/reference-parity.
The original checkout/main remains unchanged. No MCP tool/server entry point exists yet.

Implemented strict bounded JSON configuration with no environment overrides; disabled
mutation authority by default; explicit writable roots/external recovery path; typed
positions/ranges/snapshots; bounded UTF-8 reads, local URI containment and UTF-16-to-byte
mapping; byte/identity-based workspace manifest and explicit scope exclusions.

Negative controls: tests first observed the absent module; subsequent behavioral
regressions reproduced ambiguous duplicate JSON policy (not rejected), exclusion bypass
(direct read accepted) and a named-pipe read hanging until subprocess timeout. Fixes now
reject all three. No-follow directory-relative POSIX handles protect parent traversal;
O_NONBLOCK allows rejecting special files without waiting on a writer. Other hosts
without equivalent primitives report UNSUPPORTED, not unverified portability.

Observed full suite: 19 tests pass. It covers non-BMP/CRLF/EOF byte positions,
surrogate split/invalid integer coordinates, malformed/remote/traversal URI, symlink
and non-text/missing input denial, same-mtime byte changes, source creation/deletion,
file/workspace limits and explicit mutation authorization validation. The deliberate
malformed-type test casts only its input for static analysis; runtime validation is
still exercised. No production type check was weakened.

Locked Ruff check/format, ty, unittest and source-independent build/isolated import
pass. Explicit C901 and Lizard checks run separately, outside routine hooks/CI.
Cognitive acceptance remains unavailable; no qualified cognitive result is claimed.
No LSP transport, language-server semantic or Codex interoperability acceptance.

Additional defensive ruling: bound all scanned directory entries at four times the
configured eligible-file limit, before sorting/allocation. This can conservatively
reject a sparse workspace with excessive non-source entries; it never silently omits
source to claim complete references. POSIX read support is measured locally on macOS;
Linux/Windows execution is not inferred from local success.
