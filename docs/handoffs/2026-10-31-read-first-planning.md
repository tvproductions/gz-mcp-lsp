# Read-first planning handoff — 2026-10-31

Historical planning checkpoint: after this record, the user reviewed the plan in
conversation and approved it with “looks good”. The implementation package is R0
only, followed by a new bounded handoff; do not infer T10 advancement.

The user selected and confirmed two milestones: seven read tools through actual
Codex first, then the reference project's write parity. Their “yes” approves the
short design presented in conversation. The written
[design record](../superpowers/specs/2026-10-31-read-first-milestones-design.md)
captures it; the [revised execution plan](../superpowers/plans/2026-10-31-read-first.md)
is ready for review. Do not treat approach approval as approval of the unseen
detailed plan or resume runtime implementation before that review.

Review in conversation: the user confirmed explicit rejection of write-enabled
configuration for the read milestone and selected dogfooding this repository's
Python code for practical Codex acceptance. Keep the executable installed outside
the checkout; use a disposable repository copy for saved-change/failure scenarios.
Synthetic fixtures remain the exact edge-case controls. Full plan review is ongoing.

## Current state and next package

Active workspace remains `~/.codex/worktrees/359d/gz-mcp-lsp`, branch
`implementation/reference-parity`, base checkpoint
`2685a9c982fe35328608deab0e6188aa53b34fe7`. The original main checkout is unchanged.
This planning package edits documentation only and is uncommitted. It has no push,
exact-commit CI, remote backup or runtime acceptance claim.

The older T8-only resume direction is paused by the newer user instruction.
T8 remains incomplete. Preserve all existing T8 source/evidence and T9 drafts:
`src/gz_mcp_lsp/mutations.py`, `tests/test_mutations.py`,
`tests/integration/test_mutations.py`. The Git-common backup manifest and historical
source receipt are linked from the [prior handoff](2026-10-31-t8-continuation.md).
Source receipt hashes and all three draft hashes matched when this session resumed.

After detailed-plan approval, use the preserved native inline execution method,
single writer and one bounded package per handoff. The next package is **R0:
prove the read-only composition**. It is not resuming T8 or implementing T10 early.
R0 must prove no transaction/recovery startup and refusal of write-enabled config;
the current four-tool runtime is not yet the intended seven-tool milestone.

## Observations and limits

During resume, the existing focused filesystem suite passed 18 tests. The recovery
suite passed two tests with 12 actual child-exit checkpoints. These checks do not
cover the known metadata defect, certify the combined T9 dirty tree, or establish
Linux writes. No complete gate was rerun for this documentation-only package.

Disposable macOS probes found that native descriptor-based metadata copy can
preserve a custom xattr and com.apple.provenance byte-for-byte without changing
staged text; a separate probe copied an ACL. These are exploratory observations,
not shipped preservation code. Inherited directory ACLs also appeared on a mode-0700
child directory and mode-0600 backup, granting additional read access. Private
recovery storage must account for ACLs; modes alone do not prove privacy.

No metadata policy was approved or implemented. The earlier metadata question is
deferred with T8; it must not be treated as a pending decision for read planning.
No local Docker, Podman, Colima, Lima, QEMU or Multipass executable was found;
Linux write/recovery remains unobserved. Do not install infrastructure implicitly.

The short design and plan change sequencing and acceptance applicability. They
do not waive required engineering checks, cognitive qualification, actual Codex
read acceptance, later write approval/denial or supported-platform evidence.
No registration, source mutation, runtime/dependency change or publication was
performed by this planning package.

Documentation checks: `git diff --check` passed; relative Markdown link targets
in every changed/new document resolved; runtime/test source hashes still match
the prior T8 receipt; all three T9 draft hashes still match the backup manifest.
Only Markdown files changed. These checks are not the product runtime gate.
