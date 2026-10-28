# Template versioning

The current template release is **0.7.1**; the initial release
was **0.1.0**. The 0.3
adoption contract removes starter-authored skills; see [migration](migration-0.3.md).
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

## Version contract

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
