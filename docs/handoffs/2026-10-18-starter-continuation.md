# Starter continuation — October 18, 2026

Read AGENTS.md, README.md, docs/architecture.md and ROADMAP.md. Recheck live
worktree, branch, remote and CI before continuing. This handoff supersedes the
current-state and next-work guidance in the
[October 9 handoff](2026-10-09-starter-continuation.md); preserve that history.

## Current candidate

Template 0.4.0 is unreleased. Its baseline requires maximal documented Astral
alignment and necessary adopter refactoring, with evidenced compatibility
exceptions. The starter has migrated to a `src/skills_first_starter` package,
uv_build, an installed CLI and checked wheel resources. `starter.py` remains a
compatibility launcher. Python stays 3.14.8; uv/uv_build 0.13.1, Ruff 0.15.22,
ty 0.0.89 and pre-commit 4.7.0 are pinned. ty's beta exception must be revisited
at stable release or the next scoped maintenance. Read
[the alignment contract](../engineering/astral-alignment.md) and
[migration evidence](../evidence/2026-10-18-astral-alignment.md).

The complexity backlog item is complete. Adoption validation/rendering/planning/
rollback and checker scope validation are decomposed without changing public
behavior or the `lizard-functions-v1` contract. All three on-demand complexity
checks pass across `src tests tools`: maximum Lizard score 16, cognitive score
14, zero violations/tool errors. Preserve historical failing receipts and read
[the before/after assessment](../evidence/2026-10-18-complexity-remediation.md).

Latest observed verification on Windows / managed Python 3.14.8: 35 routine
adoption tests, twelve explicit analyzer tests, Ruff check/format, ty, four
pre-commit hooks, bundle/both catalogs, locked sync/lock check, wheel built from
sdist and isolated installed CLI verification. Local hooks are installed. CI is
configured with matching locked routine commands and artifact checks; recheck
its actual result for the synced commit. Native skill loading and macOS/Linux
execution are not established by the local results.

## Priorities for continuation

1. **Next repository-local implementation: Cosmic Ray's Python 3.14 compatibility
   proof.** Use `gzs-update-dependencies` for the scoped tool selection and pin.
   Check official release/compatibility evidence, select a release family, lock
   the newest verified compatible release and test on the actual pinned 3.14
   interpreter. Use invented standalone source and unittest fixtures; prove
   baseline tests pass and mutation execution reports meaningful killed/surviving
   mutants with reliable exit handling. Record exact versions, commands and
   results. If compatibility fails, retain the evidence, constraint, owner and
   revisit condition. Keep mutation testing outside hooks and CI. Do not apply a
   mutation-score gate or refactor app code to obtain this synthetic proof.
2. **First adoption milestone: fresh-session Codex discovery verification.** In
   a disposable project, use a reviewed published starter revision and the native
   marketplace manager. Verify project enablement scope, exact loaded component
   revisions and SP/gz-skills entry identities in a new host session. Keep native
   manager state and unrelated installed sources intact; never copy skill trees.
   Record PASS/FAIL/UNKNOWN with evidence. Configuration, package tests, caches
   and status output do not prove discovery. Testing the current 0.4.0 candidate
   as a published revision requires its separately authorized release first.
3. **Then an authorized adopter pilot.** FDAU is the primary candidate. Read its
   instructions and host/runtime constraints before work; preserve its domain
   authorities, operational data, profile choices and public behavior. Full
   baseline adoption requires necessary Astral reconciliation, while a
   configuration-only request reports remaining refactoring. No cross-repository
   changes are authorized merely by this handoff.

Shared/local analysis-utility ownership and the remaining selected deeper-tool
compatibility proofs remain open after these priorities. Claude combined-stack
acceptance and OpenCode support retain their upstream readiness dependencies.

## Boundaries and verification

This starter authors/distributes zero skills. Active default components remain
SP 7.0.0 and gz-skills 0.8.0 at their existing full SHAs. SP-BP is independently
pinned, expected, deferred and disabled; preserve current backlog/handoff
authority. No profile is selected or inferred. Strong Python/tool preferences
stay starter/project-owned, and generic maintenance stays upstream in gz-skills.

Use current AGENTS.md/README checks. Regenerate checked wheel resources with
`uv run --locked python tools/package_resources.py` after changing the bundle,
either catalog or adopter instructions. Run analyzer CLI tests explicitly after
analyzer changes; deeper checks stay outside routine hooks/CI. Keep versioned
Python 3.14 benefits, risks and adopt/defer decisions concrete and scoped.

The user authorized writing this handoff and Git synchronization of the completed
work. Commit/push does not publish 0.4.0, move tags, install plugins, update other
repositories or authorize the next dependency implementation. Preserve published
releases and exact rollback evidence. Read live Git history/status for the final
synced commit identity; a handoff's version label does not establish publication.
