# Implementation handoff — 2026-11-01

**T0-T10 complete. Resume T11 only on the next continuation.** The user's
continuation executed the approved T10 symbol extensions on main. Stop at this
stage boundary; installed/native host acceptance belongs to T11.

## Workspace and verified checkpoints

Continue on **main in the primary checkout**, without creating a linked worktree.
T10 starts at consolidation commit `0dbd303`; the stage commit is identified in
Git history and the final response. This continuation authorizes the bounded
stage commit, not a new push, tag or release. Local/remote alignment therefore
must be reported separately. No T10 exact-commit hosted CI is claimed here.

The retained T9 runtime is `5a2d662ab0a60b6771fefef4ff7b37e4c83ac928`;
[its CI 41354004112](https://github.com/tvproductions/gz-mcp-lsp/actions/runs/41354004112)
passed Linux x86_64, macOS arm64 and Windows AMD64. That result does not certify
T10 changes. See [T10 evidence](evidence/2026-11-01-symbols.md) for local verification.
The [consolidation record](evidence/2026-11-01-main-consolidation.md) preserves
both histories, the independent read-first tree, original pending planning files
and archived execution ledgers. Do not restore superseded planning status.

## Implemented behavior and seams

The catalog is exactly definition, references, diagnostics, hover, rename_symbol,
edit_file, document_symbols, workspace_symbols and implementations.

- Documents owns saved-file generations, reader admission, exclusive draining,
  final manifest validation and post-commit synchronization/invalidation.
- Navigation reuses one document-symbol RPC for declaration extraction and the
  public symbol tool. Hierarchy, duplicates and full/selection ranges survive.
  Flat and URI-only symbols never acquire invented identifier selections.
- Workspace search holds Documents.generation() through search, advertised
  resolution, normalization, scope classification and final validation. Empty
  workspaces need no document/didOpen. Changed search/resolve rejects stale results.
- Implementations forwards exact UTF-16 positions. Pinned ty includes the queried
  declaration as well as subclasses/member overrides. External targets are marked
  metadata. No external source is opened by the three extensions.
- Diagnostics uses current pull reports and identity-bound caching. EditPlan
  values are immutable; the planner validates complete WorkspaceEdits without IO.
- Transactions owns private journals, same-filesystem staging, state locking,
  exact bytes/modes, safe rollback, durable receipts and conservative recovery.
- Mutations composes those services with retained bounded previews. Production
  lifespan finishes authorized recovery before mutation admission.

All successes use schema_version, operation, position_encoding, result,
workspace_generation, documents and complete. Preview metadata is under result:
result.plan_id, result.files and result.annotations. Apply result is the durable
disk receipt; semantic_state is separate. Never report committed disk writes as
rolled back because later LSP synchronization failed.

Writes default to disabled. Enabled writes require bounded operator roots plus
private same-filesystem state on Linux x86_64/macOS arm64; Windows writes are
unsupported. Model approval flags are rejected; a plan token is not authenticated
human consent. Independent writers are not serialized by the private adapter
lock; a quiescent workspace is required.

## Verification baseline

T10 discovers **181 tests**. The Windows gate passes with **25 POSIX-only tests
not applicable**. Installed outside-checkout MCP/real-ty tests cover hierarchy,
duplicate names, subclass/member implementation locations, empty workspaces and
fresh search after creation. A real-ty search changed before final validation
returns STALE_DOCUMENT; controlled fake barriers prove search and resolve races.
The focused review's external-symbol scope finding was fixed with a failing
regression test. This is a T10 review, not T13's fresh whole-branch review.

Keep CPython **3.14.10**, uv **0.13.6**, MCP SDK **2.3.0** and ty **0.0.95**.
Nested hooks must resolve the same uv. Required gate:

```text
uv sync --locked --all-groups
uv run --locked pre-commit run --all-files
uv build --no-sources
uv run --locked python tools/verify_distribution.py
```

The four hooks remain Ruff check, Ruff format, ty and unittest. No pytest.
No application environment overrides, request-time installation, Backplane,
second server, generic filesystem operations or unsolicited LSP applyEdit.

## Next authorized stage: T11 only

Read README.md, AGENTS.md, AGENTS.skills-first.md, current design-revision evidence,
adopted engineering policies, the approved specification/plan and acceptance matrix.
Use the [T11 brief](superpowers/plans/2026-10-28-reference-parity.md#t11-installed-distribution-and-actual-codex-host-acceptance).

1. Extend artifact/installed-server checks to the full nine-tool contract, actual
   ty and runtime-only clean environments. Preserve source independence and origin
   checks; do not confuse a catalog assertion with semantic acceptance.
2. Obtain fresh Linux x86_64/macOS arm64 write evidence and Windows read/unsupported
   write evidence for the exact changed tree, including platform skip inventory.
3. Use actual Codex to exercise all read tools, disabled mutation denials, enabled
   previews, host-approved apply and a denied host mutation with unchanged hashes.
   Native host approval is separate from operator authority and preview identity.
4. Capture host timeout/ty death/EOF and reaping. H1-H3 require actual host evidence;
   direct SDK integration is insufficient. If approval interaction is unavailable,
   keep H2 UNKNOWN. Complete the stage gate/review/commit, then stop before T12.

## Remaining acceptance gaps

- T11 full installed/native nine-tool and host mutation approval acceptance;
  T12 deeper engineering; T13 fresh whole-branch review, acceptance and stop.
- No T10 Linux/macOS rerun or exact-commit hosted CI is claimed in this session.
- T4 Codex programmatic allow/deny remains partial H1-H3 evidence, not GUI/human
  mutation approval. Windows-host/Linux-adapter bridging remains unverified.
- Final fixtures still need shared_runtime/run_shared_cli and three importing/
  calling packages with independently enumerated positions.
- Cognitive qualification remains UNKNOWN; complexipy is not a passing authority.
  Native discovery retains duplicate/global-scope FAIL. Preserve caches/defaults.
  Routine gates and Git synchronization do not waive strict acceptance gaps.

Use the [execution record](evidence/2026-11-01-execution.md),
[T9 mutation evidence](evidence/2026-11-01-mutations.md),
[T10 evidence](evidence/2026-11-01-symbols.md) and
[configuration/request guide](configuration.md). The current ignored task ledger
is `.superpowers/sdd/2026-10-28-reference-parity/progress.md`; fresh clones use
tracked evidence and fixtures. Use gh for GitHub reads/authorized writes. Never
publish private source, journals or transcripts.
