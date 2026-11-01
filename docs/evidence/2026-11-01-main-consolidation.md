# Main consolidation - 2026-11-01

The user requested merging every project branch to main, removing worktrees and
Git synchronization. Inspection found two independent implementations rather than
a linear feature history. The user explicitly chose: **retain the verified T9
runtime; preserve the read-first branch's unique work separately**.

## Branch disposition

| Input | Commit | Resolution |
| --- | --- | --- |
| Original main | 922bd622e5d0d21f833eba70550c01fe07616a90 | Fast-forward to verified T9 history |
| feat/reference-parity | f0e26cc29401c2548f2b3d414b7c68fee9a20724 | Retained tracked tree, including all T9 source/tests and current toolchain |
| implementation/reference-parity | fc3fb7dfbecd6258c1141d6c300e04c1d8e90fa9 | Merge parent retained using the user-selected T9 tree resolution; independent read-first tree archived separately |

This is a history merge with an explicit tree choice. It does not combine the two
incompatible implementations or claim the read-first branch's seven-tool catalog
is active. Its unique code/tests, approved read-first documents, metadata and
receipts remain recoverable from the original commit in main's ancestry.
For example, git show fc3fb7d:src/gz_mcp_lsp/navigation.py reads that version;
git archive fc3fb7d reconstructs its full tracked tree. The GitHub CLI preference
is carried forward in AGENTS.md without changing runtime/configuration provenance.

Retained source tree: b7a5882619e93dbb83744d4acc9b08ef45f48acc.
Retained test tree: de6ff1c5f02035a52cf91f0127b25c3e9c85fc52.
No runtime, test, lockfile or dependency changes are part of this consolidation.
T10 remains unstarted in the retained T9 sequence; read-first task labels apply
only to that separately preserved implementation.

## Local recovery material

Before changing main or removing the worktree, a byte-verified archive was made
under Git-common handoffs/2026-11-01-main-consolidation-f0e26cc/:

- all-branches.bundle, verified by git bundle verify;
- read-first-tree.zip, a separate complete snapshot of fc3fb7d;
- pending-main/ with all ten original pending planning files, plus their patch
  and a SHA-256 backup-manifest.json;
- feature-execution-records/ with 496 verified ignored execution-record files.

The pending planning tree is also retained in Git stash commit
de1c54b86e8d4227cb2e914cf16d691e892e81b8. Its pre-execution status wording was already
incorporated or superseded by T9's approved execution records; it is preserved,
not reapplied over the current specification. The original stash is not dropped.

The archive is local-only; it is never packaged or pushed. The merged Git history
preserves both committed implementations for fresh clones. Worktree environments,
bytecode, build outputs and linter caches are reproducible; unique execution
records are retained before their worktree is removed. Git hooks are reinstalled
against main's interpreter so removal cannot leave a hook pointing at the old
worktree environment. No native manager cache/defaults are changed.

## Validation and handoff

Immediately before integration, the retained 165-test suite passed on Windows
with 25 POSIX-only not-applicable tests. The full merged-tree gate and exact-commit
main CI must pass before this request is reported complete. The final sync response
records the main SHA, CI, cleanup and local/remote alignment without another
receipt-only commit.

Continue from docs/handoff.md on main after consolidation. Existing cognitive
qualification, native discovery, full host acceptance and final whole-branch
review gaps remain open. This merge is not a release or full milestone acceptance.
