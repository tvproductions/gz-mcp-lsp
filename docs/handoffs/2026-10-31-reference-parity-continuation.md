# Reference parity continuation — 2026-10-31

## Resume here: T8 only

Finish **Task 8: guarded filesystem transactions and durable recovery** in the
[approved plan](../superpowers/plans/2026-10-28-reference-parity.md#task-8-guarded-posix-filesystem-transactions-and-durable-recovery).
T8 is unfinished. Preserve the incoming T9 drafts; do not register mutation tools
or start another capability in this work package. Hand off after T8, with exact
checks/commit and unresolved gaps, before advancing to T9.

**First action:** verify the worktree/HEAD below against Git, read AGENTS.md and the
[execution checkpoint](../evidence/2026-10-31-execution-checkpoint.md), then inspect
the T8 diff and preserved T9 drafts. Safely isolate the unfinished T9 candidate
from T8 verification while retaining its exact contents. Do not hide a failing
T8 test or register unfinished T9 tools merely to make the gate green.

**Expected result:** a separately reviewable T8 candidate with its complete
required gate and recovery evidence, or a precise report of what prevents that.
Do not mark T8 complete while its required checks or safety claims remain unknown.
Stop at that bounded handoff. If closing T8 needs a material design/scope change,
report the concrete decision instead of silently changing the approved contract.

## Observed local state

- Observation: 2026-10-31 17:01:56 UTC.
- Active worktree: `~/.codex/worktrees/359d/gz-mcp-lsp`.
- Branch: `implementation/reference-parity`.
- HEAD: `a872e25ba2f5014b65596ada8f0ebf0164a5abee`.
- Original checkout: `~/Documents/Devel/gz-mcp-lsp`, main at `3d6a869`.
- Eight local implementation commits follow the design commit. Main is unchanged.
- T8 changes, T9 drafts, audit records and this handoff are **local, uncommitted**.
  There has been no implementation push, exact-commit CI, release or tag. Do not
  assume another clone contains this state.

Always set shell-tool workdir to the active worktree. The conversation's default
cwd may still point to the original main checkout.

A local recovery snapshot of all dirty tracked/untracked files and the ignored
execution ledger is stored under the original repository's Git common directory:

`.git/handoffs/2026-10-31-reference-parity/20261031T170156416260Z/`

It contains `working-files.tar.gz`, `tracked.patch`, `manifest.json`, Git status
and worktree metadata. This is a local backup, not a commit or remote handoff.
Use it only after comparing against the current files; do not overwrite newer work.
Normal terminal/application restart requires no restore.

## Standing authorization and ownership

The user approved the revision-2 specification and plan on 2026-10-31 with
“specification and plan approved.” Implementation remains authorized; terminal
restart does not require asking again. That approval does not waive gates or
permit release/tag publication or extra capabilities.

The user subsequently selected:

- **This session implements; the other agent stops editing.**
- **One bounded work package per handoff.** This overrides continuous whole-plan
  execution guidance. Resume with T8 only, then hand off before T9.

Another session modified filesystem.py and added mutations.py,
tests/test_mutations.py and tests/integration/test_mutations.py in this same
worktree. Its recovery checks were subsequently reproduced here. Its mutation
work remains unfinished, with type/format failures and MCP registration absent.
Preserve those contributions; do not relabel them as this session's test-first work.

## Evidence and open gate

The [source-hashed checkpoint receipt](../evidence/2026-10-31-execution-checkpoint.json)
and [audit](../evidence/2026-10-31-execution-checkpoint.md) own the detailed findings.
The latest complete gate observed exit codes **0 / 1 / 0 / 0**:

1. `uv sync --locked --all-groups` — passed.
2. `uv run --locked pre-commit run --all-files` — failed: Ruff check passed,
   formatting failed in the draft mutation integration test, ty reported three
   draft-mutation diagnostics, unittest ran 90 tests with two errors from
   unregistered mutation tools. See the exact findings in the checkpoint.
3. `uv build --no-sources` — passed; it builds the current unfinished tree too.
4. `uv run --locked python tools/verify_distribution.py` — passed: isolated
   installed import/CLI and an actual-ty MCP hover, not all nine tools.

Separate C901 and Lizard passed on the audited runtime tree. Full strict
engineering acceptance remains incomplete; the qualified cognitive engine is
unavailable, and complexipy is not a passing substitute.

T8 focused observations: 13 filesystem tests and two real-process recovery tests
passed; the latter exercise ten actual crash checkpoints. No general filesystem
safety or Linux acceptance is inferred. Extended metadata (ACL/xattr) behavior
has not been accepted; preliminary native API probes were not product guards.
Review unresolved safety/platform assumptions before claiming write acceptance.

Four read tools (definition, references, hover, diagnostics) are implemented and
verified through the official SDK and actual pinned ty. Rename/edit are not
registered; three extension tools and actual Codex acceptance are not implemented.
The completed increments have their own receipts; do not reconstruct their work.

## Read in this order

1. Root AGENTS.md, README.md, AGENTS.skills-first.md and adopted engineering policy.
2. [Approved specification](../superpowers/specs/2026-10-28-semantic-navigation-design.md).
3. [Reference parity](../discovery/reference-parity.md) and
   [acceptance matrix](../discovery/acceptance-matrix.md).
4. [Approved plan](../superpowers/plans/2026-10-28-reference-parity.md), T8 brief and
   the current checkpoint linked above.
5. Local ignored ledger `.superpowers/sdd/2026-10-28-reference-parity/progress.md`.
   T0–T7 are recorded complete. T8 is open. The ledger has material rulings and
   provenance; it is also copied into the local recovery snapshot.

## Resume controls

Use gzs-session-handoff Resume to compare this dated observation with current Git
and files. Use the adopted Superpowers execution/TDD workflow, with user-selected
bounded pacing; gzs-root-cause-debugging for failures, gzs-cross-platform-python
for filesystem/process seams, and gzs-quality-gate for the complete candidate.
A fresh independent review remains required at the eventual branch-completion
boundary; none has certified this unfinished implementation.

Retain lite governance, disabled Backplane, Python 3.14.10 / uv 0.13.6, locked
execution, four hooks, unittest, src packaging and JSON application configuration.
No environment application overrides, Makefile, pytest, copied Go/private sources,
second server or general LSP framework. Preserve attribution and numeric ceilings.
Gz-skills 0.8.3 native-source reconciliation was recorded in T0; cognitive strict
acceptance remains blocked by owning starter issue #1 and must remain visible.

Do not reset/clean this dirty worktree, bypass hooks, publish, or treat a build or
mocked result as semantic/host acceptance. Do not introduce another writer.
