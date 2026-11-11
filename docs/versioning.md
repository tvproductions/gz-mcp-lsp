# Template versioning

The current template release is **0.9.0**; the initial release was **0.1.0**.
Its minimum-only uv policy
change governs the minor increment, alongside compatible corrections recorded
in the [release-planning audit](https://github.com/tvproductions/gz-skills-first-starter/blob/3f76acf0038b030bf5abd85ce4a419e890d3e420/docs/evidence/2026-11-01-release-planning-audit.md).
The [starter release-scope record](https://github.com/tvproductions/gz-skills-first-starter/blob/3f76acf0038b030bf5abd85ce4a419e890d3e420/docs/handoffs/2026-10-24-session-close.md#november-8-git-synchronization-and-release-scope)
supersedes the audit's earlier patch-only target after upstream reconciliation.
The [0.9.0 receipt](https://github.com/tvproductions/gz-skills-first-starter/blob/3f76acf0038b030bf5abd85ce4a419e890d3e420/docs/evidence/2026-11-08-0.9.0-release.md) records the authorized
publication and acceptance inputs. Verify its immutable tag and GitHub release
before treating this metadata as publication evidence.
The adopting product's independent pending release scope is in [ROADMAP.md](../ROADMAP.md).
The 0.3 adoption contract removes starter-authored skills; see [migration](migration-0.3.md).
Release 0.8.0 bundles three-host repository configuration, brownfield scope repair
and mandatory adopter discipline. Its [release receipt](https://github.com/tvproductions/gz-skills-first-starter/blob/3f76acf0038b030bf5abd85ce4a419e890d3e420/docs/evidence/2026-10-31-0.8.0-release.md)
records independent execution-pin refreshes and retained acceptance limitations.
Release 0.7.1 ships the consumer-side preparation and a compatible Ruff patch.
The maintainer explicitly directed publication without waiting for the engine.
Actual cognitive integration remains open and unscheduled in
[issue #1](https://github.com/tvproductions/gz-skills-first-starter/issues/1).
The incoming gzkit-owned engine must still be selected, qualified and measured
before the cognitive exception can be removed. This release retains that
exception and does not claim the cognitive defect is fixed; see the
[release receipt](evidence/2026-10-26-0.7.1-release.md).
The current version is recorded in
`bundle.json` as `template_version`, independently of SP, SP-BP and gz-skills
versions and the adopter's application version. `pyproject.toml` mirrors the
version for this starter's helper project; the repository tests check agreement.
An adopter may change its app metadata without changing the starter's identity.

```bash
uv run --locked skills-first-starter version
```

This reports the checkout's declared version, not proof of a published release.
The initial release is
[v0.1.0](https://github.com/tvproductions/gz-skills-first-starter/releases/tag/v0.1.0),
dated October 11, 2026. Its annotated tag identifies the verified release commit.
Earlier development commits were untagged; do not label them as a released
v0.1.0 retroactively. Release
[v0.7.0](https://github.com/tvproductions/gz-skills-first-starter/releases/tag/v0.7.0)
adds independently locked X-Plane tooling, Dependabot scans, current execution
tooling and shared policy alignment. The maintainer explicitly authorized its
publication with cognitive qualification deferred to planned 0.7.1; this is a
release-specific exception, not a passing cognitive result or an adopter waiver.
See [release evidence](evidence/2026-10-26-0.7.0-release.md).
Release 0.6.0 added the single template-native update skill and
[canonical update/bootstrap method](updating.md). It retains 0.5's expanded
Astral acceptance, lane/analysis policy, adopter SemVer and major-release PRDs,
and [greenfield/brownfield migration runbook](adoption-0.5.md). It retains the runtime,
tool and independent SP 7.0.0/gz-skills 0.8.0 pins. Automatic conformance/PRD
validation remains unimplemented; release notes disclose acceptance gaps.
Future publication remains a separately authorized operation.

## Ecosystem policy authority and consistency

### Initial adopter project version

The first substantive release is the first versioned commitment to the project's
public contract. Declare that contract and issue the release as **0.1.0**.
This establishes a versioned baseline; the contract may evolve under the required
0.x compatibility rules. It does not assert the stability required for 1.0.0.

Permit `0.0.0` only as an unpublished placeholder for a bare scaffold. As soon
as any original implementation, tests, documentation or configuration is added,
set the initial adopter project version to **0.1.0**. Do not release project-owned
work as `0.0.0`. Align package metadata, runtime version output and release
records, and verify agreement before accepting adoption. Correct an unpublished
`0.0.0` project containing original work to `0.1.0`; preserve published versions
and immutable tags, and
advance an existing released project from its actual current version. Never
reset a released project to `0.1.0` or rewrite a published `0.0.0` release.

This is a mandatory starter policy. SemVer permits zero-valued components, but
its [initial-development guidance](https://semver.org/spec/v2.0.0.html#how-should-i-deal-with-revisions-in-the-0yz-initial-development-phase)
recommends starting at `0.1.0`. Do not mistake syntax validity for acceptance
under this template. The adopter's initial version is independent of the
starter and upstream plugin versions.

### Shared authority

This repository is the authoritative alignment source for the maintainer's
shared engineering and release policy. This document owns the SemVer and
release-planning rules for this template, its adopters, and the maintainer's
`gz-skills` and `superpowers-backplane` repositories. The companion repositories
bind these rules in their own instructions and release documents; they do not
formally adopt this template or bootstrap its bundle into themselves.

Policy flows from this template to those repository bindings. Workflow ownership
is separate: [Backplane](https://github.com/tvproductions/superpowers-backplane)
owns requirements tracking, issue classification/lifecycle labels, backlog and
release monitoring, handoffs, and the definitions of lite and heavy modes.
Refer to its [mode authority](https://github.com/tvproductions/superpowers-backplane/blob/main/docs/superpowers-backplane/modes.md)
and governance instead of defining a second lifecycle here. gz-skills supplies
portable procedures such as `gzs-release`; Superpowers owns feature development.
Upstream Superpowers is independently owned and is not bound by this policy.

The companion repositories must check this source before release preparation,
during scoped policy/tooling maintenance, and when notified of a relevant source
change. Read this document, the changelog, and applicable baseline/engineering
guidance from the canonical repository. Compare with the last reviewed source;
record the date, full source SHA, paths, applicability, differences, and the
adopted decisions in the companion's existing release or handoff authority.
Record development guidance as unreleased; for authorized working-tree review,
also record content hashes and do not present the base SHA as the edited source.
Recheck the final source revision before claiming published alignment.

An unavailable source or unresolved applicable difference is an explicit gap,
not evidence of consistency. A departure needs evidence, the maintainer's
approval, an owner and a dated revisit condition. A local binding may specify
project details but must not silently redefine this shared policy. No automatic
schedule, plugin update, runtime upgrade or synchronized release is implied.

The major-release PRD rule below also applies prospectively to independently
versioned gz-skills skills, including their first 1.0.0. Each affected major
needs newly written requirements identifying that component and major; a new
coordinated PRD may cover several explicitly identified majors. Published
releases and historical acceptance evidence are not retroactively relabeled.

Repository governance is distinct from shipped workflow policy. gz-skills and
Backplane must continue to respect each consumer's own adopted policy; this
alignment does not impose starter tooling or PRDs on unrelated consumers.
Backplane's unfinished capabilities remain unfinished, and both mode intent
and policy alignment remain separate from installed readiness or full starter
conformance. Keep existing project authorities until the relevant Backplane
workflow is ready and explicitly adopted.

Each companion owns the explicit binding for its own development environment.
The maintainer's current Python rule is 3.14 for ordinary projects and supported
3.12 for X-Plane/XPPython3-bound code; the starter owns that rule for its adopters.
gz-skills workflows consume the governing project's policy instead of maintaining
a competing family/tool/package baseline. Publisher-side choices do not become
blanket constraints for unrelated skill or Backplane consumers. A corrected
source candidate must still be released and explicitly selected before installed
alignment can be claimed; source bindings are not native installation evidence.

## Version contract

### Plan releases from their governing work

Use this hierarchy for this starter, adopting projects and the bound companion
repositories: **PRDs guide major releases; selected work and requirements drive
minor releases; fixes drive patch releases.** Apply compatibility analysis to
that scope before selecting the number. A version bump alone is not a release
plan, and an individual task, commit or completed issue is not a release unit.

| Release | Governing scope | Required planning evidence |
| --- | --- | --- |
| Major, including 1.0.0 | A newly written PRD defines the intended product outcomes, requirements and boundaries for that major. | Link the new PRD, acceptance criteria and migration/compatibility decisions. Do not reuse an earlier major's PRD. |
| Minor | A coherent selected bundle of work and requirements advances the product within its governing direction. | Link the included requirements/work items, exclusions, dependencies and acceptance criteria in the existing backlog/release authority. |
| Patch | Corrections restore existing commitments, including compatible clarifications. | Link the defects or incorrect commitments, expected corrected behavior and verification. New capability or obligations do not become fixes by labeling them maintenance. |

Before implementation planning, identify which release scope the work serves.
Before accepting a completed change, reconcile its disposition into that scope:
included, deferred or excluded, with evidence. Keep a current release-scope record
in the project's existing backlog, roadmap or release authority; do not create a
parallel lifecycle. Record all of the following:

1. The actual last published version/tag and exact revision, or explicit evidence
   that this is the first unpublished release. Distinguish that baseline from
   current development metadata and the adopted starter/plugin versions.
2. The proposed next version and governing PRD, selected requirements/work or
   fixes. State why that scope requires major, minor or patch. Review the complete
   scope since the published baseline; the largest required increment wins.
3. Included completed work, included remaining work, deferred work and measurable
   release acceptance gates. Do not treat the whole future backlog as one release
   or require unrelated future work to finish before every release.
4. Compatibility impact and required migration, plus outstanding decisions and
   the evidence needed to resolve them. Unresolved scope/version decisions remain
   explicit; agents MUST NOT silently shrink an approved release to publish sooner.

Maintain the pending version, metadata/runtime mirrors, lock metadata where
affected, and changelog together once the release scope is selected. Multiple
changes in one planned release share its pending version; do not increment once
per task. Before release preparation passes, verify that the selected work and
actual diff agree, all required evidence exists, and the version matches that
scope. Missing scope or classification evidence blocks that claim.

For example, after released `0.4.2`, selected new reporting requirements drive
`0.5.0`; a correction to an existing report drives `0.4.3`. After `1.4.2`, a
compatible new reporting bundle drives `1.5.0`; its compatible defect correction
drives `1.4.3`. A new PRD guiding `2.0.0` must identify that major's outcomes and
requirements; incompatible changes cannot be hidden in `1.5.0`. A PRD does not
automatically make every implementation task a major release. During 0.x,
requirements and incompatible changes advance minor under the rules below;
the first stable `1.0.0` still needs its own newly written PRD.

An unpublished initial `0.1.0` may cover an explicitly selected first-release
scope. It is not evidence of a versioning defect merely because many tasks are
complete. Conversely, "unreleased" is not permission to accumulate unrelated
requirements indefinitely: review scope growth and record whether it belongs
in the first release or a later minor. Preserve existing approved release gates
until a scope change is approved. Published tags and release history stay immutable.

These are planning and acceptance obligations, not publication authorization.
Backplane retains workflow ownership; until ready and explicitly adopted, each
project's existing authorities execute them. Both lite and heavy follow this rule.

### Required version decision procedure

Agents MUST perform this procedure when accepting requirements, planning work,
and closing a change. Do not defer it until someone asks to publish a release.

1. **Establish the baseline.** Read project metadata, runtime version output,
   changelog, published tags/releases and current release scope. Verify their
   identities. Record missing publication evidence as UNKNOWN; do not infer it
   from a version string or silently assume there were no previous releases.
2. **Identify the governing commitment.** Link the new major's PRD, the selected
   minor requirements/work bundle, or the existing commitment being corrected.
   A patch needs an identifiable defect or compatible clarification. New required
   behavior is minor work even when its ticket or commit says "fix".
3. **Classify the complete pending scope.** Use the highest required increment,
   with compatibility constraints below. A stable breaking change requires a
   major and its newly written PRD before implementation planning can pass.
   Never suppress that consequence to avoid writing the PRD. A new PRD can guide
   several minor bundles within its major; it does not make each task a major.
4. **Select one target and reconcile it now.** Calculate it from the last
   published baseline, resetting lower components as shown below. Reuse a valid
   existing pending target. If new work exceeds it, revise the target and scope
   together; do not increment once per pending task. Update metadata/runtime
   mirrors, affected lock metadata and the unreleased changelog in the same
   change. Routine classification and version-file reconciliation are part of
   authorized work; do not ask the maintainer to choose a number agents can
   derive from this policy.
5. **Keep the bundle bounded.** State the release outcome, included requirement
   IDs, exclusions and measurable completion gate. An initial 0.1.0 needs that
   finite scope too. Assign unrelated/new future requirements to later minor
   bundles; do not append the whole roadmap to the active release. Changing an
   approved product outcome or gate requires a scope decision, not a guessed
   version. Ask only for the unresolved product decision and record the blocker.
6. **Verify and report.** Review the actual change against the governing work,
   check all version mirrors and prove the relevant acceptance criteria. Report
   `published baseline -> pending target`, release kind, source requirements or
   defects, included/remaining/deferred work and publication status. A closeout
   MUST NOT claim versioning complete without that evidence. Missing PRDs,
   scope, classification or inconsistent versions fail the applicable planning,
   closeout and release-preparation checks; configuration is not acceptance.

| Published baseline | Selected scope | Pending target |
| --- | --- | --- |
| No previous release, verified | Bounded first usable scope | 0.1.0 |
| 0.4.2 | Compatible fixes only | 0.4.3 |
| 0.4.2 | New requirements, including a bundle also containing fixes | 0.5.0 |
| 1.4.2 | Compatible fixes only | 1.4.3 |
| 1.4.2 | Compatible new requirements or public deprecations | 1.5.0 |
| 1.4.2 | Incompatible public contract, guided by a newly written PRD | 2.0.0 |

Use this compact decision record in the existing release/backlog authority;
equivalent existing fields are sufficient. Do not introduce a second tracker.

```text
Published baseline: version, tag and exact revision; or verified first release
Pending target / kind: version / major | minor | patch
Governing source: new major PRD | selected requirements/work | corrected defects
Release outcome and acceptance gate:
Included completed work / evidence:
Included remaining work:
Deferred or excluded work:
Compatibility / migration / version-mirror checks:
Unresolved product decisions: none, or decision owner and blocked action
Publication: unpublished | published with immutable identity
```

Selecting a version does not assert readiness or authorize publishing it. Tool
updates and refactors are classified by their effect on the public contract;
commit prefixes, effort, elapsed time and the upstream dependency's own version
do not determine this project's bump. Preserve published identities and approved
scope. Do not manufacture past releases to make development progress look older.

### Classify compatibility within the selected scope

Use [Semantic Versioning](https://semver.org/spec/v2.0.0.html) for the template's
public adoption contract: CLI commands and outputs, managed-file formats,
preservation/conflict behavior, baseline requirements and project guidance.
During 0.x development, bump the minor version for additions, requirement changes
or adoption changes requiring reconciliation; bump the patch for compatible
fixes and clarifications. Release 1.0.0 only when the intended public contract
and its compatibility guarantees are established. After 1.0, incompatible
contract changes require a major bump, compatible additions a minor bump and
compatible fixes a patch bump. Explain adopter impact even for small changes.

Version 0.6.0 adds a native template-update skill and a managed adopter
file, changing the supported adoption capability and ownership contract. It
therefore increments minor from 0.5.0. A compatible correction to an existing
capability would increment patch (for example 0.5.1) and get its own new tag;
neither case moves or reuses v0.5.0.

The following release-planning rules bind this starter and each adopting
project's own releases. App, template and upstream component versions remain
independent; an adopter's PRD describes its own product and major release.

Adopting projects also use `MAJOR.MINOR.PATCH` for their own public product
contract. Apply the same 0.x and stable-release classification above to that
contract, independently of the template's version. Document the supported public
surface, such as Python APIs, CLI behavior, file/data formats and configuration
contracts. A breaking change to that surface requires major after 1.0 even when
it changes no Python function signature. Compatible additions require minor;
compatible fixes require patch. Public deprecations require minor, with removal
reserved for a subsequent major after 1.0. Incrementing major still requires
the newly written PRD below; the PRD does not replace compatibility analysis.

Every major release, including 1.0.0, **always requires a newly written PRD**
for that major release. Reference that PRD in release preparation and evidence;
reusing an earlier major's PRD or changing the version number alone does not
satisfy this requirement. Compatibility impact still determines when a major
bump is needed; the new PRD is a mandatory part of preparing that release.

Minor releases bundle a coherent selected set of related changes. A completed
feature does not automatically trigger its own minor release; record the bundle
in the project's existing backlog and handoff authorities. SP-BP is intended to
help coordinate this bundling when ready and explicitly adopted. While it is
deferred, use the existing authorities without inventing a replacement lifecycle.
The compatibility rules above still bound what belongs in a minor release.

Patch releases remain compatible fixes and clarifications, including bounded
verification of existing commitments; they do not introduce new baseline
obligations. These release-planning rules supplement the version classification
above and do not retroactively relabel published releases.

The user explicitly selected patch versions 0.3.1 for the adopter cohesion
requirement clarification and 0.3.2 for the independent SP update. Their changelog
entries distinguish policy from pin changes; these scoped choices do not change
the general rule above. SP's upstream major version is independent of the
template version.

Release notes distinguish changes to [adopter range/selection policy](baseline-policy.md)
from refreshes of tested exact pins within that policy. Adopters review constraints
and their reasons rather than treating every checkout pin as a permanent requirement.

The current manifest accepts numeric `MAJOR.MINOR.PATCH` versions. Development
snapshots carry the next intended version plus their exact commit SHA; they are
not stable releases until published. Prerelease suffixes would require a scoped
manifest/CLI change. Stable Git tags use `vMAJOR.MINOR.PATCH` and must never be
moved or reused after publication. Subsequent changes receive a new version.

Template version, bundle/lock `schema_version` and upstream component versions
are separate. A template bump does not enable SP-BP, update a plugin or alter a
file schema automatically. A metadata-only additive field does not imply a new
schema; a breaking interpretation of a managed format requires its own reviewed
schema/migration decision.

## Adopter provenance and upgrades

New adoption records the starter's repository, manifest version and full commit
SHA in `.skills-first/bundle.lock.json`. Configure preview/apply and status expose
that starter record. Keep the SHA: multiple development commits may share the
next intended version, and a label alone cannot identify their contents.
The helper records the supplied/default SHA and manifest label; it does not prove
that they match a published tag. Verify the checkout, tag and full commit before
adoption. Native catalogs continue to pin upstream components by full SHA.

Legacy records without a starter version have unknown version provenance.
Do not infer their version from today's metadata or edit their recorded SHA.
Compare the original revision with the desired reviewed release, preview the
full managed-file diff and reconcile the lock, configuration and guidance
together. The helper deliberately refuses different managed records instead of
silently adding a version or migrating an adopter. Preserve app additions,
settings, overrides and profile choices and retain prior pins for rollback.
Until reconciled, configure/status may report the managed-record conflict.

Use the existing [stack maintenance binding](adoption.md#maintaining-the-adopted-stack)
and gz-skills workflows to assess upgrades. Check published starter releases
alongside SP, SP-BP and gz-skills independently; generic freshness tooling remains
upstream-owned. A newer starter does not automatically migrate a generated
repository or prove fresh-session skill discovery.

## Preparing and publishing a release

1. Select the next version according to the adoption contract. For every major,
   including 1.0.0, write a new PRD and reference it in the release evidence.
   For a minor, identify the coherent change bundle in the existing backlog;
   SP-BP may assist only after readiness and explicit adoption. Update
   `bundle.json` and the starter's `pyproject.toml` together, then refresh `uv.lock`
   with uv if its project metadata changed. Preserve independent plugin pins
   unless their upgrade was explicitly scoped.
2. Add a changelog entry describing behavior, baseline/pin changes, adopter
   reconciliation steps, verification evidence and remaining limitations. Mark
   the entry unreleased while preparing it. Preserve historical evidence as-is.
3. Run the documented repository checks on the exact Python pin and review the
   clean committed release candidate. For bundle changes, validate both native
   catalogs. Native loading/readiness evidence remains separate.
4. When publication is authorized, mark the changelog entry released, commit the
   final release metadata, tag that exact verified commit with an annotated
   `vMAJOR.MINOR.PATCH` tag and publish the GitHub release with those notes. The
   release must identify the full commit SHA and remaining host/Backplane gaps.
   Verify the remote tag resolves to the intended commit; do not move it to fix
   a release. Do not conflate an ordinary Git sync with release publication.

The template's GitHub release is the adopter-facing distribution record. No
package-registry upload, plugin installation or new release automation is
required by this policy.
