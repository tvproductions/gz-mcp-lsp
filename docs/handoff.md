# Fresh implementation handoff — 2026-11-01

**T0–T9 complete. T10 unstarted.** This session refreshes the handoff and
synchronizes Git only. Do not begin T10 as part of this request.
The remaining specification/plan are approved; resume one bounded stage on the
user's next continuation, then stop at that stage boundary.

## Verified checkpoint and workspace

Continue on **feat/reference-parity** in the existing isolated implementation
worktree. The original main checkout has preserved pending planning documents;
do not reset, overwrite or include them in the feature-branch sync.

The final T9 implementation is **5a2d662ab0a60b6771fefef4ff7b37e4c83ac928**.
[Exact-commit CI 41354004112](https://github.com/tvproductions/gz-mcp-lsp/actions/runs/41354004112)
passed Linux x86_64, macOS arm64 and Windows AMD64, including the final shared
success-envelope correction. This supersedes the earlier T9 implementation and
documentation checkpoints as runtime verification evidence.

The fresh handoff commit changes documentation only. Observe its own exact-commit
CI through completion when synchronizing; do not create another commit solely to
record that result. The sync response and branch history identify the final SHA.
Ordinary feature-branch push is authorized. No main merge, force-push, tag or release.

## Shipped behavior and important seams

The catalog is **definition, references, diagnostics, hover, rename_symbol,
edit_file**. Exactly three semantic extensions remain for T10.

- Documents owns saved-file generations, reader admission, exclusive draining,
  generation validation and post-commit synchronization/invalidation.
- Navigation supplies definition/references/hover and internal document-symbol
  support for declaration source extraction. Reuse this support in T10.
- Diagnostics supplies current pull reports and identity-bound result caching.
- EditPlan values are immutable; the planner validates the entire WorkspaceEdit
  and computes after-images without filesystem IO.
- Transactions owns private journals, same-filesystem staging, state locking,
  exact bytes/modes, safe rollback, durable receipts and conservative recovery.
- Mutations owns bounded retained previews and composes those services.
  Production MCP lifespan finishes authorized recovery before mutation admission.

All successes use schema_version, operation, position_encoding, result,
workspace_generation, documents and complete. **Preview metadata is under result**:
use result.plan_id, result.files and result.annotations. Apply result is the
durable disk receipt; semantic_state is separate. Never misreport a committed
disk outcome as rolled back because later LSP synchronization failed.

Mutation tools remain destructive even for preview. Writes default to disabled
and require explicit operator roots plus private same-filesystem state on Linux
x86_64/macOS arm64. Windows writes are unsupported. Model approval flags are
rejected; plan identity is not authenticated human consent. Independent writers
are not serialized by the private adapter lock; a quiescent workspace is required.

## Verification baseline

The suite discovers **165 tests**. Complete Windows/native Linux gates, C901
source ceiling 20 and scoped portability audit passed for the final T9 code.
Hosted CI independently passed the complete gate on all three platforms.
Windows runs disabled/unsupported startup denials with **25 POSIX-only tests
not applicable**. POSIX lanes skip only the Windows-specific startup denial.

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

## Next authorized implementation stage: T10 only

On the next continuation:

1. Verify branch/status and read README.md, AGENTS.md, AGENTS.skills-first.md,
   current design-revision evidence and adopted engineering policies.
2. Read the [T10 brief](superpowers/plans/2026-10-28-reference-parity.md#t10-public-document-symbols-workspace-symbols-and-implementations),
   [specification](superpowers/specs/2026-10-28-semantic-navigation-design.md)
   and [acceptance matrix](discovery/acceptance-matrix.md).
3. Continue the adopted executing-plans/test-driven workflow and task ledger.
   Add exactly document_symbols, workspace_symbols and implementations.
   Reuse existing normalization; preserve hierarchy, duplicates, and distinct
   full/selection ranges. Never invent positions for URI-only workspace symbols.
4. Hold Documents.generation() through workspace search, advertised resolution,
   normalization and final validation, without choosing a synthetic document.
   Prove empty-workspace, changed-search and changed-resolve cases.
5. Complete real-ty integration, required gate and reviewed stage commit, then
   hand back before T11. No T10 implementation is included in this handoff.

## Remaining acceptance gaps

- T10 extensions; T11 final installed/native nine-tool and mutation approval
  acceptance; T12 deeper engineering; T13 fresh whole-branch review, acceptance
  and deliberate stop. No fresh whole-branch review has occurred yet.
- T4 Codex 0.166.0 programmatic accept/deny is partial H1–H3 evidence, not GUI/
  human-click or full native mutation acceptance. Windows-host/Linux-adapter
  bridging and operator-enabled native mutation scenarios remain unverified.
- Final fixtures must include shared_runtime/run_shared_cli and three importing/
  calling packages with independently enumerated positions.
- Cognitive qualification remains UNKNOWN; complexipy is not a passing authority.
  Native discovery retains duplicate/global-scope FAIL. Preserve caches/defaults.
  Git synchronization neither waives these gaps nor accepts a release.

Use the [execution record](evidence/2026-11-01-execution.md),
[T9 evidence](evidence/2026-11-01-mutations.md) and
[configuration/request guide](configuration.md#mutation-requests).
The ignored .superpowers/sdd/2026-10-28-reference-parity/ retains the complete
local task ledger/rulings and execution helpers. These are continuation aids,
not sole authority; fresh checkouts use tracked fixtures. Never publish private
source, journals, transcripts or machine-specific scratch locations.
