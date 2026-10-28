# Security

No runtime is available yet. The revised scope includes diagnostics and guarded
rename/edit in addition to navigation. The proposed adapter and ty subprocess
would run
with the launching user's operating-system permissions. Read-only annotations do
not sandbox the language server or prevent a host agent from forwarding returned
code and documentation to its model provider.

Design review must address URI scheme/authority validation, canonical paths and
symlink escapes, explicit workspace boundaries, bounded input/output sizes,
timeouts, subprocess cleanup, stale documents and untrusted hover text. Reject
unsolicited workspace/applyEdit and expose no execute-command or code-action tool.
Rename/edit require operator-enabled writable roots, complete preview and immutable
plan identity, all-target validation, durable staging/recovery and truthful receipts.
Host approval and plan tokens do not themselves establish filesystem safety.
Validation failures write nothing; commit failure restores exact before-images or
blocks mutations with RECOVERY_REQUIRED. Multi-file crash atomicity and isolation
from noncooperating external writers are not promised. See the revised specification.
Use explicit executables and argument arrays, never shell command evaluation.
Provision dependencies before launch. Do not log source contents by default.
No hosted service, listening port, credentials or environment settings are required.
External definition locations and dependency stubs need an explicit reviewed policy.

Do not post private code, credentials or exploitable details in public issues.
Use GitHub's private vulnerability reporting on this repository when available;
otherwise contact the maintainer through the organization profile to arrange a
private channel before sending details. There is no released supported version
or promised response SLA yet.
