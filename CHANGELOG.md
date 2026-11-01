# Changelog

## Unreleased

- Consolidate both implementation histories on main using the explicitly selected
  verified T9 runtime. Preserve the independent read-first tree, pending planning
  files and execution records; retire the linked worktree after verification.

- Refresh the T9 handoff with its final verified implementation SHA/CI,
  shared mutation-result contract, validation baseline and bounded T10 resume
  checklist. Preserve outstanding acceptance gaps; no T10 implementation.

- Use the common success envelope for both mutation actions; retain preview
  metadata under result with UTF-16, generation and saved-document provenance.

- Implement T9 rename_symbol/edit_file preview/apply tools, production recovery
  admission, immutable retained previews and coordinated disk/semantic outcomes.
  Preserve durable receipts through cancellation and restart; add installed
  actual-ty mutation/recovery tests. Windows writes remain unsupported.

- Implement T8 internal guarded POSIX transactions, exact-byte/mode rollback,
  private durable journals/receipts and conservative crash recovery. Add actual
  process-death tests; Windows writes remain rejected. T9 mutation tools and
  production startup recovery remain pending.

- Canonicalize temporary test roots and bound barrier waits; keep short deadlines
  only in explicit timeout controls. Cap CI jobs so portability failures cannot
  leave the suite waiting indefinitely. Production runtime behavior is unchanged.

- Add the T7 handoff with bounded-session execution, T8 transaction/recovery
  contracts, remaining acceptance gaps and branch synchronization instructions.

- Implement T7 immutable, zero-IO edit plans with original UTF-16 ranges,
  byte-exact after-images, alias/overlap/resource-operation rejection and
  content-bound preview identities. Mutation tools and filesystem writes remain pending.

- Implement T6 current pull diagnostics with saved-identity resultId caching,
  full-list unchanged handling, related-document scope and bounded source context.
  Verify actual installed error/repair/dependency behavior; distinguish every
  replacement transport by generation epoch and reject untracked semantic inputs.

- Implement T5 definition/references and complete authorized declaration source,
  preserving caller UTF-16 positions, distinct ranges and original hover forms.
  Verify three-consumer/decoy, decorated/nested/async/constant and Unicode fixtures
  through direct ty and an installed MCP adapter; enforce aggregate result limits.

- Implement T4 production hover, saved-file generation/read/exclusive leases,
  stale-result rejection, bounded document synchronization and fail-closed ty scope.
  Verify installed hover and local gates on Windows/Linux; actual Codex allows
  hover and denies it without an adapter call. Add three-platform CI lanes;
  macOS/hosted CI and final mutation/host acceptance remain pending.

- Implement T3 one-child ty lifecycle and official SDK stdio CLI, rejecting
  unsolicited edits and unreaped-child replacement. Verify actual ty startup,
  MCP framing/EOF and installed command behavior; semantic catalog awaits T4.

- Implement T2 bounded LSP byte framing, response correlation, callbacks,
  cancellation/deadlines and failure cleanup; add eleven controlled-stream tests.
  Real-server and MCP interoperability remain unaccepted.

- Implement T1 JSON settings, strict coordinates, contained UTF-8 snapshots and
  bounded byte-based workspace manifests; Windows writes remain unsupported.
  Add exact-byte portability regression coverage for subprocess diagnostics.

- Adopt official mcp==2.3.0 for T0; enforce its exact wheel requirement, retain
  distribution leakage guards and verify Python 3.14 SDK schema/results/cancellation.
  Record native plugin scope failure and unresolved cognitive qualification.

- Record approval of the revised plan and linked specification; begin T0 on an
  isolated implementation branch. Runtime acceptance remains evidence-gated.

- Correct second-review plan gaps: wire startup recovery before mutation admission,
  separate workspace generation leases from document snapshots, and place T0's
  failing dependency-policy test before verifier and SDK changes. Planning only.
- Correct four execution details in the unapproved plan: production hover at T4,
  coordinated concurrent reads/restarts/commits, explicit platform verification
  lanes and an early actual Codex feasibility checkpoint. Architecture and scope
  remain unchanged; no runtime task started.
- Reconcile unapproved design/plan prerequisites with ty 0.0.95 and the completed
  gz-skills 0.8.3 update; retain execution-host verification, unresolved cognitive
  qualification and all pending human decisions. No implementation authorized.
- Set the product's initial development version to 0.1.0 at user direction;
  no tag or release publication.
- Update ty to 0.0.95 and six transitive development/hygiene dependencies;
  update the pinned setup-uv action to v10.3.3.
- Independently select gz-skills v0.8.3 and reconcile project catalogs, provenance
  and native marketplace source while retaining starter v0.7.1, lite and disabled
  Backplane. See the [update receipt](docs/evidence/2026-10-31-dependency-update.md).
- Revise the intended objective to six-tool Go reference parity, corrected semantic
  targeting, three bounded ty navigation extensions, actual Codex acceptance and stop.
- Pin source assessment to latest release v0.1.1 and main e4395849, distinguishing
  unchanged implementation from dependency metadata updates and unverified behavior.
- Prepare unapproved write-safety specification, acceptance matrix and phased
  Superpowers implementation plan. No runtime code or dependencies added.

### Initialization

- Initialize gz-mcp-lsp directly from the public skills-first starter template.
- Record adopted v0.7.1 provenance, lite profile, independent product metadata,
  Python baseline, public contribution/security guidance and routine CI.
- Review mcp-language-server v0.1.1 and official MCP/LSP/ty documentation.
- Propose architecture and capability acceptance cases for human review.
- No adapter runtime, accepted semantic capabilities, tag or release.

Starter history remains in the initial generated commit and published starter;
its versions and release receipts do not version or certify this product.
