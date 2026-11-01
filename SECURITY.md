# Security

The unreleased development runtime implements seven read tools and guarded
rename/edit. The adapter and ty subprocess run
with the launching user's operating-system permissions. Read-only annotations do
not sandbox the language server or prevent a host agent from forwarding returned
code and documentation to its model provider.

The runtime validates URI schemes/authorities, canonical paths and
symlink escapes, explicit workspace boundaries, bounded input/output sizes,
timeouts, subprocess cleanup and saved-document generations. Treat returned hover
text and source as untrusted data. Unsolicited workspace/applyEdit is rejected;
there is no execute-command or code-action tool.
Rename/edit require operator-enabled writable roots, complete preview and immutable
plan identity, all-target validation, durable staging/recovery and truthful receipts.
Host approval and plan tokens do not themselves establish filesystem safety.
Validation failures write nothing; commit failure restores exact before-images or
blocks mutations with RECOVERY_REQUIRED. Multi-file crash atomicity and isolation
from noncooperating external writers are not promised. See the revised specification.
Use explicit executables and argument arrays, never shell command evaluation.
Provision dependencies before launch. Do not log source contents by default.
No hosted service, listening port, credentials or environment settings are required.
External targets are marked metadata without reading their source. Writes default
to disabled, require explicit operator roots/private same-filesystem state, and
are supported only on verified Linux x86_64/macOS arm64 local filesystems. Windows
writes remain unsupported. Configure native host approval separately for both
mutation tools, including preview. A plan token is content identity, not human
authorization. Disposable acceptance evidence records actual native protocol
allow/deny decisions without claiming GUI clicks; see
[T11 acceptance](docs/evidence/2026-11-01-codex-acceptance.md).

Do not post private code, credentials or exploitable details in public issues.
Use GitHub's private vulnerability reporting on this repository when available;
otherwise contact the maintainer through the organization profile to arrange a
private channel before sending details. There is no released supported version
or promised response SLA yet.
