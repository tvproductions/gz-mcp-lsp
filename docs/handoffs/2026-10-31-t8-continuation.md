# Resume handoff: T8 continuation — 2026-10-31

**Resume T8 only. T8 is INCOMPLETE; do not advance to T9.** The user requested
one bounded work package and a handoff. This checkpoint stops at a concrete
metadata-safety decision and unobserved Linux acceptance, not task completion.

Read [the T8 evidence](../evidence/2026-10-31-t8-continuation.md) and
[source-hashed receipt](../evidence/2026-10-31-t8-continuation.json), then the
[prior formal handoff](2026-10-31-reference-parity-continuation.md) for approval,
single-writer ownership and historical audit. The approved plan/spec remain in
force. No new runtime capability, T9 registration or release is authorized here.

## Workspace and preserved drafts

Active worktree: `~/.codex/worktrees/359d/gz-mcp-lsp`, branch
`implementation/reference-parity`. Original main checkout is unchanged.
The checkpoint commit containing this handoff follows parent `a872e25`;
resolve its exact SHA with `git log -1` and compare source hashes in the receipt.
There is no implementation push or exact-commit CI. Do not infer remote backup.

The three incoming T9 drafts were temporarily moved out for T8 candidate
verification, then restored unchanged after committing the candidate:

- src/gz_mcp_lsp/mutations.py
- tests/test_mutations.py
- tests/integration/test_mutations.py

A second byte-for-byte copy and SHA-256 manifest remain under the original
checkout's `.git/handoffs/2026-10-31-t8-only/t9-drafts/`. Compare the manifest
before moving/restoring anything. Do not delete, overwrite or accept those drafts.
The prior all-file backup remains at the location recorded in the prior handoff.

## What changed and what passed

Corrupt index/journal value handling now fails closed with RECOVERY_REQUIRED;
each target parent filesystem is checked for locality. Negative controls were
observed before fixes. Filesystem tests now total 18; recovery tests remain two,
with 12 actual crash checkpoints including rollback. Mode/symlink and failed
restoration lockout cases are explicit. Incoming lifecycle changes are preserved.

The isolated T8 candidate passed the exact four-command gate, separate C901 and
repository-owned Lizard checks, plus runtime portability scanning. The build and
outside-source actual-ty hover probe passed. See evidence for scope/provenance.
Restored unfinished T9 drafts mean that the combined dirty worktree must not be
reported as that passing candidate. Its prior draft failures remain unresolved.

## Required next work

Synthetic probes show committed replacement drops both a custom xattr and an ACL.
The metadata policy must be settled and tested before accepting T8: either copy
required metadata safely, or deny unsupported metadata before source writes,
explicitly addressing automatic macOS provenance and inherited directory ACLs.
The evidence gives exact probes, conservative direction and native API sources.
No metadata preservation/guard is claimed implemented. Do not register writes to
paper over this issue or count passing routine tests as write acceptance.

Linux write/recovery behavior remains unobserved. T8's safety/platform gate stays
open. After the metadata decision, run all target/restore/crash cases and the
complete required gate on a separately reviewable T8 candidate. Use the existing
inline Superpowers/TDD and project engineering policies; do not introduce another
writer. Hand off again before T9. Leave T8 unchecked until all required evidence
exists. Cognitive qualification, final independent review and actual Codex host
acceptance remain later, distinct gaps.
