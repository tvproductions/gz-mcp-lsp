# Astral guidance evaluation handoff — October 18, 2026

## Current continuation: authorized findings addressed

The user's subsequent instruction to address the findings authorized the bounded
implementation. Read [Astral acceptance](../engineering/astral-acceptance.md),
the [worked migrations](../engineering/astral-migrations.md),
[implementation plan/audit](../engineering/astral-implementation-plan.md) and
[starter acceptance record](../evidence/2026-10-18-astral-acceptance.md).
Application, typed-library and workspace examples were executed on Windows with
the pinned Python/tools, including installed behavior and typing negative control.
uv/Ruff/ty effective configuration, root/member semantics, source-independent
builds, namespace/coordinator cases and reviewed Ruff prose are reconciled.
The adopter fragment and wheel resource are updated; helper behavior, pins,
routine hooks and CI contract remain intact.

At the pre-sync save point the implementation is unreleased and uncommitted;
the user subsequently invoked `gzs-git-sync`, authorizing ordinary commit/push
of this completed unit. Read live history for the resulting SHA and CI rather
than treating this pre-sync state as current after publication of the save point.
The final local check receipt retains its observed scope. New acceptance
obligations belong in a future bundled minor, with no version selected here.
Existing real-adopter pilot, other hosts, freshness/deeper-tool verification and
utility ownership remain separately scoped work. Preserve the original analysis
and receipts below as historical evidence.

## Prior evaluation continuation (historical)

Latest continuation: read the [uv documentation deep dive](../engineering/uv-deep-dive.md)
before revising the proposal. The user requested especially careful treatment of
Projects and maximum Astral compliance. Two disposable Windows/uv 0.13.1 proof
receipts distinguish locked/exact execution, source/metadata and root/member
selection; unqualified root-selection wording needs reconciliation. Review the
findings and revise the implementation proposal next. No baseline implementation
or adopter pilot has been performed.

Continuation update: the [follow-up evaluation and bounded proposal](../engineering/astral-guidance-evaluation.md)
now traces requirements, evaluates all five gaps and separates applicable cases.
It rechecked synchronized commit `1c10764` and successful CI. Next review the
proposal before selecting implementation; the preserved analysis below remains
historical. No acceptance guide, worked migration or conformance checker has
been implemented by the evaluation.

Resume point: further evaluate the assessment preserved below before selecting
implementation work. First recheck live Git/CI, read AGENTS.md, README.md,
docs/architecture.md and the linked policy/code, then evaluate the five gaps
against current official Astral guidance. Distinguish mandatory baseline
requirements, applicable project-specific choices and optional advanced cases.
The expected next result is an evidence-backed, bounded improvement proposal;
this handoff does not authorize a general rewrite, new lifecycle or adopter pilot.

The user requested preserving the preceding analysis "as is if possible," then
Git synchronization. The assessment below retains the chat wording, including
its dated closing status, with repository links made relative for portability.
It is a starting assessment for further evaluation, not a completed exhaustive
Astral conformance audit. The continuation state after it supersedes that
closing status. This is the current next-session focus; the
[release continuation](2026-10-18-0.4.1-release-continuation.md) retains the
completed Cosmic Ray/Codex evidence and other open work.

## Preserved analysis

**The guidance is strict and fairly extensive for core Python projects, but adopter enforcement is not yet complete.**

| Dimension | Assessment |
|---|---|
| Binding requirements | Strong and explicit |
| Core Astral workflow coverage | Extensive |
| Starter's own implementation and checks | Strong, demonstrated |
| Repeatable adopter migration procedure | Partial |
| Proof that an adopter fully conforms | Still agent-dependent |

The [Astral alignment contract](../engineering/astral-alignment.md) already requires:

- `src/` packaging, declared builds, installed-package imports, and artifact verification.
- `uv_build` for pure Python, with evidenced reasons for another backend.
- Centralized `pyproject.toml`, managed Python, exact execution pins, committed locks, and locked commands.
- Ruff/ty configuration aligned with the runtime, consistent local/hooks/CI checks.
- Explicit workspace dependency edges, shared resolution, and separate verification where environments differ.
- Necessary adopter refactoring. Existing layout is explicitly **not an exemption**; exceptions need evidence, an owner, and a revisit condition.

These choices track Astral's documented project structure and environment practices. Astral itself permits alternatives, so ours is a deliberately stricter project baseline—not a claim that Astral mandates every choice. [Astral project guidance](https://docs.astral.sh/uv/concepts/projects/init/), [locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/).

The main gaps are practical:

1. **No consolidated adopter acceptance checklist.** Requirements are distributed across several documents. We lack one requirement-by-requirement record of evidence, result, exception, and outstanding work.
2. **Migration instructions are less detailed than the obligations.** We need complete worked paths for an existing application, a typed library, and a multi-package workspace.
3. **Effective configuration needs stronger verification guidance.** Centralization is required, but we do not thoroughly explain detecting nested/user configuration or overrides that weaken checks. Both Ruff and ty have configuration precedence that matters here. [Ruff configuration](https://docs.astral.sh/ruff/configuration/), [ty configuration](https://docs.astral.sh/ty/configuration/).
4. **Advanced build and deployment cases are unevenly covered.** Clean distribution builds, development source overrides, non-editable production environments, private indexes, and native extensions need explicit applicability guidance.
5. **There is some documentation drift.** For example, [python.md:137](../engineering/python.md#routine-engineering) says the expanded lint selection remains undecided, although the reviewed selection is already configured.

The helper correctly preserves adopter files; it does **not** establish Astral conformance by configuring the skill stack. That distinction is documented, but the subsequent reconciliation and acceptance process needs tightening.

My priority would be **one explicit adoption acceptance contract, supported by worked migration examples and concrete verification commands**. More "must" language would add less value.

Your release rule is now carried through both starter and adopter guidance; packaged instructions were regenerated and checks passed. Those edits remain uncommitted.

## Continuation state and authority

Observed October 18, 2026, 16:04 UTC, before this save point: branch `main`,
HEAD and `origin/main` at released v0.4.1 commit
`0a93e18fda328f84fda955d6bc182f34e5d4febf`; ahead/behind `0/0`. The worktree had
the user-directed release-policy clarification in AGENTS.md, baseline/versioning
guidance, adopter instructions, their generated wheel resource, changelog and
release handoff. The current request authorizes this new handoff and ordinary
commit/push of that completed unit. Read live history for the final save-point
SHA and CI; neither this pre-sync HEAD nor the closing sentence above describes
the state after successful synchronization.

The user's standing rule applies **to this starter and adopters**: every major
release, including 1.0.0, always requires a newly written PRD; minor releases
bundle related changes; patches remain compatible fixes and clarifications.
SP-BP is intended to help coordinate bundles but remains expected, deferred and
disabled until readiness and explicit adoption. The binding rule is in
[versioning](../versioning.md#version-contract), [baseline policy](../baseline-policy.md#release-planning)
and [adopter instructions](../../templates/AGENTS.skills-first.md). Application,
template and plugin versions remain independent. The working changes are
recorded under `Unreleased`; no next version or new release was selected.

No Astral implementation or enforcement changes were made in response to the
assessment. In particular, the stale Ruff sentence remains an evaluation
finding, and the proposed acceptance contract/examples are not yet implemented.
Preserve the existing configuration-only helper seam and public behavior while
evaluating what fuller adoption guidance should require. Keep policy in this
starter/project binding, generic engineering workflows upstream in gz-skills,
and project-specific domain rules with adopters. The starter still distributes
zero agent skills. Do not add a parallel maintenance skill, generic freshness
reporter, unapproved hooks/CI gates or gzkit lifecycle.

## Verification and next evaluation

The pending policy edits already passed regeneration with
`uv run --locked python tools/package_resources.py` and the documented locked
sync, four-hook routine gate, bundle/both catalogs, source/wheel build and
isolated installed CLI checks. The save-point process runs the full gate again
after this handoff and navigation edits. Follow AGENTS.md/README for commands;
analyzer unittest invocation is additionally required after analyzer changes,
which are not part of this documentation save point. Recheck CI for the final
synced commit rather than assuming a local pass establishes it.

For further evaluation, trace each existing Astral requirement to its authoritative
document, adopter-facing instruction, concrete verification and available
evidence. Use [adoption workflow](../adoption-workflow.md),
[configuration limits](../project-configuration.md#what-is-resilient-today),
[backport guidance](../backport.md), [pyproject.toml](../../pyproject.toml),
[hooks](../../.pre-commit-config.yaml), [CI](../../.github/workflows/check.yml)
and [artifact verifier](../../tools/verify_distribution.py). Consult the official
Astral sources linked in the analysis and the
[build guidance](https://docs.astral.sh/uv/concepts/projects/build/) before
turning suggested advanced coverage into universal obligations. Separate gaps
in written instructions, adopter procedure, automated checks and actual host/
platform evidence. Use the existing project planning authority for a bounded
proposal; no sub-agent delegation or broad implementation follows from this
handoff alone. Published tags and historical receipts remain immutable.
