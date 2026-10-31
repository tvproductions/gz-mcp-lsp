# T8 continuation checkpoint — 2026-10-31

**T8 remains INCOMPLETE.** The isolated candidate passes the routine gate, but
native synthetic probes demonstrate ACL/extended-attribute loss on replacement.
Linux write safety is unobserved. No mutation tools were registered; T9 did not
advance. This supersedes the earlier checkpoint's T8 verification observations,
not its historical audit or the approved specification.

## Changes and observed negative controls

Resumed the existing `implementation/reference-parity` worktree from `a872e25`.
Preserved incoming transaction/lifecycle work and three separate T9 drafts.
Reproduced two corrupt-state failures: dictionary-valued index IDs and journal
status escaped as raw TypeError. Validate those values before set membership;
both now return RECOVERY_REQUIRED without changing targets. A further failing
test demonstrated that workspace-level volume validation missed target mounts;
authorization now checks each target parent volume. These are observed red/green
corrections; inherited implementation is not relabeled as new test-first work.

Added coverage for target mode/symlink changes, restore I/O failure with retained
recovery lockout, and real child death during each of two rollback replacements.
The recovery driver remains test-only. Added explicit subprocess decoding to the
macOS volume probe and recovery tests. No runtime settings or dependencies changed.

## Candidate verification

[Source-hashed receipt](2026-10-31-t8-continuation.json) records Python 3.14.10,
uv 0.13.6, macOS 26.6.2 arm64, exact commands and exits. All four required commands
passed (0/0/0/0) with the three unfinished T9 files temporarily archived outside
the checkout. No hooks or tests were suppressed or modified to accept T9.

- Filesystem suite: 18 tests passed.
- Recovery suite: two tests passed, with 12 actual child-exit checkpoints including
  journal/staging/replacement/rollback/receipt boundaries. Registered-but-missing
  journals fail closed; missing recovery copies block without fabricating rollback.
- Routine Ruff check/format, ty and full unittest hook passed.
- Source-independent sdist→wheel build passed; outside-source installation/import,
  CLI and actual-ty MCP hover passed. This is read-path distribution evidence.
- Separate C901 passed. Repository-owned Lizard checker passed, 128 functions,
  maximum 20, with function/module/overall ceilings 20 unchanged.
- Portable scanner passed on runtime sources. Wider test scan reports three
  existing subprocess decoding findings in tests/test_mcp_api.py; these were not
  changed in this T8 package. An initial file-level scanner invocation was invalid;
  the reported result comes from the corrected directory scopes.

Full logs and the detailed Lizard receipt remain under this plan's ignored
`.superpowers/sdd/2026-10-28-reference-parity/` directory. After the checkpoint
commit, the T9 files are restored byte-for-byte to their original paths. That
combined dirty worktree is not the isolated passing candidate; the earlier
checkpoint documents the draft format/type/unregistered-tool failures.

## Blocking safety evidence and concrete next decision

Two disposable local probes used only invented source, file modes and metadata:

1. Set `com.example.gz-mcp-lsp=synthetic` on a.py with `/usr/bin/xattr -w`,
   preview the two-file fixture and apply. Receipt says committed, exact expected
   text is present, but `/usr/bin/xattr -p` no longer finds the attribute.
2. Add `everyone allow read` to a.py using `/bin/chmod +a`, preview/apply the same
   fixture. Receipt says committed, but `/bin/ls -le` no longer shows that ACL.

Both observations are in the JSON receipt. Existing code stages a new inode and
copies only group/mode, so it cannot preserve these attributes. The platform also
automatically attaches `com.apple.provenance` to new synthetic files; an attempted
`xattr -c` did not remove it. An all-attribute rejection policy is therefore not
usable here without an explicit treatment of OS-maintained attributes.

Before accepting T8, choose and implement an evidenced metadata policy: preserve
required ACLs/attributes on staged and restored files, or reject unsupported
metadata before any replacement, with an explicit rule for OS-managed attributes.
Rejecting unsupported custom metadata is the conservative direction; silently
whitelisting provenance or dropping ACLs is not an accepted decision in this run.
Check inherited directory ACLs, private recovery storage and race/recovery cases,
not only the original source inode. Apple documents descriptor-based inspection
in [flistxattr](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man2/listxattr.2.html)
and [acl_get_fd_np](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man3/acl_get_fd_np.3.html);
preliminary native API probes are not a shipped guard.

Rerun the T8 safety and routine gates after that decision. Obtain actual Linux
filesystem/recovery evidence before claiming Linux writes; no Linux execution or
exact-commit CI occurred here. W4–W7 and E5 are not accepted from passing fixture
checks alone. Cognitive qualification, full branch review, actual Codex acceptance
and the remaining milestone gates stay separately open. No release/tag/push.
