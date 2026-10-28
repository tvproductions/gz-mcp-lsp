# Security

No runtime is available yet. The proposed adapter and ty subprocess would run
with the launching user's operating-system permissions. Read-only MCP tools do
not sandbox the language server or prevent a host agent from forwarding returned
code and documentation to its model provider.

Design review must address URI scheme/authority validation, canonical paths and
symlink escapes, explicit workspace boundaries, bounded input/output sizes,
timeouts, subprocess cleanup, stale documents and untrusted hover text. Reject
workspace/applyEdit and expose no execute-command/edit/refactor operation. Use
explicit executables and argument arrays, never shell command evaluation.
Provision dependencies before launch. Do not log source contents by default.
No hosted service, listening port, credentials or environment settings are required.
External definition locations and dependency stubs need an explicit reviewed policy.

Do not post private code, credentials or exploitable details in public issues.
Use GitHub's private vulnerability reporting on this repository when available;
otherwise contact the maintainer through the organization profile to arrange a
private channel before sending details. There is no released supported version
or promised response SLA yet.
