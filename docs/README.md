# Documentation scope

The [implementation handoff](handoff.md) is the current resume point: T0-T11 implemented,
T12 next on main after the final exact-commit platform gate, one bounded stage per session. The
[consolidation record](evidence/2026-11-01-main-consolidation.md) preserves both
branch histories and the user-selected runtime. Git sync does not waive gaps.

[Application settings](configuration.md) documents JSON settings, all nine tools and the mutation contract.
The [T11 native receipt](evidence/2026-11-01-codex-acceptance.md) records installed
and actual Codex evidence; its final synchronization response identifies exact-commit CI.

The [November 1 execution record](evidence/2026-11-01-execution.md) records the
user's subsequent approval and current T0-T13 execution state. The planning-only
boundaries in earlier dated receipts below are historical.

Product authorities: root README/AGENTS/CONTRIBUTING/SECURITY, the revised design and plan in
`superpowers/specs/`, discovery reviews in `discovery/`, and
`evidence/2026-10-28-design-revision.md`. Initialization evidence is historical;
revision 2 explicitly supersedes the earlier read-only scope without rewriting
its observed results.

The [October 31 dependency-update receipt](evidence/2026-10-31-dependency-update.md)
supersedes earlier tool/plugin freshness conclusions for its changed inputs.
It does not approve the specification or implementation plan.

The [November 1 prerequisite reconciliation audit](evidence/2026-11-01-plan-prerequisites.md)
records the corresponding corrections in the unapproved specification, plan and
acceptance matrix, with execution-host verification and cognitive qualification
still required.

The [targeted execution-plan audit](evidence/2026-11-01-plan-execution-corrections.md)
records four subsequent corrections to task ordering, concurrency coordination,
platform verification and early Codex feasibility. The implementation boundary
and pending design decisions remain unchanged.

The [second-review correction audit](evidence/2026-11-01-plan-second-review-corrections.md)
records production startup-recovery assignment, workspace generation leases and
dependency-test ordering, with updated plan/matrix hashes. No execution is approved.

Engineering policies, adoption guidance, update procedures and engineering
utilities were inherited from gz-skills-first-starter v0.7.1. They remain binding
where applicable. Starter evidence predating this product is historical upstream
evidence, not measurements of gz-mcp-lsp. `STARTER-README.md` and
`STARTER-AGENTS.md` preserve original context; their relative links were written
for the starter root. Product instructions take precedence on product scope.
Template-only helper code, helper tests/resources and X-Plane packaging were
removed from the product; they remain in the generated initial commit and the
published starter. Use a separate released starter checkout for adoption commands.
The managed bundle lock records the release commit; generation used template main
with three additional documentation changes, explicitly recorded in product evidence.
