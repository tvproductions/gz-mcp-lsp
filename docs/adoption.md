# Adoption and native loading

Version 0.6 supplies one owned template-update skill; published 0.5.0
supplies none. Use [canonical template updates](updating.md) for bootstrap and
maintenance. Start with the
[adoption workflow](adoption-workflow.md) and [structure contract](structure.md).
Project instructions reference upstream and project-owned workflows directly.
Use the [greenfield/brownfield runbook](adoption-0.5.md) for 0.5 adoption and
upgrades. Pre-0.3 skill copies additionally require the [legacy migration](migration-0.3.md).

## Establish the project boundary

Use a separate reviewed checkout of `tvproductions/gz-skills-first-starter`. Record
its full published commit SHA and review `bundle.json`. The configure helper
uses that checkout's HEAD unless `--starter-ref <full-SHA>` is supplied. Supplying
a SHA records your selection; the helper does not prove it is published. Verify
it before applying:

```bash
git rev-parse HEAD
gh api repos/tvproductions/gz-skills-first-starter/commits/FULL_STARTER_SHA --jq .sha
```

Also read the checkout's declared template version with
`uv run --locked skills-first-starter version`. For a published release, resolve its
`vMAJOR.MINOR.PATCH` tag to the same full SHA and review its changelog. The label
alone does not prove publication. New locks record version and SHA separately;
older unversioned locks require reviewed reconciliation. See
[template versioning](versioning.md). Preserve the adopter app's own version.

Review existing `AGENTS.md`, skill discovery surfaces, plugin configuration,
and gzkit ownership. Existing project authorities remain in place. A conflict
is a request for reconciliation, not permission to remove an existing install.
The starter does not select a gz-skills profile. The pinned gz-skills v0.8.0
supplies `gzs-project-setup`; invoking it and choosing lite/heavy remain separate
explicit adopter decisions required before completed adoption. Neither absent
nor null selection is a completed lane. Preserve starter Python policy over
profile defaults; both lanes require applicable adoption/release analysis.

## Project dependencies and settings

Inventory the project's dependencies, lock and application settings before
adoption. Use the [configuration and baseline contract](project-configuration.md)
to preserve additions, extensions and reviewed overrides. The configure helper
does not rewrite these files or resolve Python packages. Review baseline
freshness at adoption; changing a shared baseline does not migrate existing
adopters automatically.

## Codex

After configure preview/apply, `.codex/config.toml` registers the shared Git
marketplace at your reviewed starter SHA and enables SP and gz-skills for that
project. SP-BP remains pinned and
explicitly disabled. Configure writes `AGENTS.skills-first.md` for direct workflow
routing and maintenance obligations. Version 0.6 additionally seeds the
project update skill; it does not install upstream skill copies. Verify the
upstream plugins in a fresh session after native installation.
Commit this project configuration after review;
installation caches remain native-harness state.

Open the project in Codex and review its trust decision. Inventory the existing
plugins and marketplaces before installation:

```bash
codex plugin marketplace list --json
codex plugin list --json
```

The marketplace is named `skills-first-starter`. If the configured project
marketplace is absent, inspect project-config loading and trust; do not work
around it by silently changing global configuration. If the same components
already appear under another marketplace or through a checkout, reconcile the
sources before adding duplicates. The helper can catch repository-local copies
and configuration conflicts, but cannot inventory another host's session.

When the correct marketplace is loaded and duplicate discovery has been ruled
out, explicitly install its components through the native manager:

```bash
codex plugin add superpowers@skills-first-starter
codex plugin add gz-skills@skills-first-starter
codex plugin list --json
```

These are user-run native installation commands, not actions performed by the
helper. Native manager commands may alter user-level installation state; inspect
the resulting configuration and keep project enablement in the adopting repo.
Installing the bundle here does not authorize global enablement for unrelated
projects. If this host cannot maintain the intended project scope, stop and
record that limitation rather than claiming project-only activation.

Start a fresh session. Confirm the actual discovered identities:

- `superpowers:using-superpowers`
- `gz-skills:gzs-router`

For version 0.6, also verify the project-scoped `update-gz-template`
separately from upstream plugin discovery; published 0.5.0 has no such entry.
Verify each identity's owning
plugin and installed source revision; a same-named skill from another marketplace
does not establish this bundle's discovery. Reconcile duplicate sources only in
the adopting project's scope, preserving unrelated installations and user defaults.

Project trust is a prerequisite. The October 18 Windows/CLI 0.163.0 check first
reported the disposable project's layer as disabled for lack of trust. After
the user explicitly approved its native trust entry, a new session loaded the
pair from the published v0.4.0 revision; an outside-project control retained user
defaults and loaded neither starter source. See [verified CLI acceptance](evidence/2026-10-18-codex-discovery-verified.md)
and the preserved [initial UNKNOWN attempt](evidence/2026-10-18-codex-discovery.md).
Review the native project trust decision; never compensate for a skipped project
layer by registering or enabling the bundle globally. Native refresh may cache
configured disabled plugins too; cache presence is not activation or readiness.
Check the actual marketplace checkout SHA and discovered skill source bytes,
not just the configured ref. This CLI proof does not establish desktop UI or
other-harness behavior.

Backplane installation and conformance checks below apply only to a future,
explicitly authorized adoption after readiness review. They are not part of
the default pair.

Read Backplane's pinned [installation/compatibility reference](https://github.com/tvproductions/superpowers-backplane/blob/d0eeee829c491da02351e793544aa16ad96461bf/skills/managing-superpowers-backlog/references/installing-superpowers.md).
Setup verifies GitHub CLI capabilities and actual native issue fields before
backlog operation. Use an authorized disposable issue for mutation scenarios.
Do not infer a right to modify production issues from installation.

Record starter and component revisions, host version, installed source identities,
fresh-session skill discovery, and Backplane compatibility/conformance results.
Report each result as PASS, FAIL, or UNKNOWN. The starter's tests do not replace
host verification. Five Backplane checks are skill structure, native issue
intake, language-neutral verification, lifecycle transitions, and Superpowers
installation. An `UNKNOWN` is not a passing combined-stack claim.

## Claude Code

The `.claude-plugin/marketplace.json` catalog references the same three immutable
sources. From the adopting project, inspect the current manager and existing
installations first. Then use Claude's project scope:

```text
/plugin marketplace add tvproductions/gz-skills-first-starter
/plugin install superpowers@skills-first-starter --scope project
/plugin install gz-skills@skills-first-starter --scope project
```

The displayed catalog pins component source revisions. The command above obtains
the current starter marketplace; for repeatable adoption, use a reviewed checkout
at a recorded full SHA and `/plugin marketplace add /path/to/reviewed-starter`
instead. Check the manager's current syntax before executing. Restart and verify
actual SP and gz-skills discovery. Backplane remains deferred.
Marketplace syntax validation
alone is not a completed installation or lifecycle proof.

This starter does not automate Claude project settings or claim end-to-end
Claude verification. Backplane Claude lifecycle acceptance remains upstream work.

## OpenCode

Do not generate a guessed adapter or claim readiness. Backplane's OpenCode
implementation/acceptance is pending. The bundle can add an OpenCode adapter
when those upstream contracts and negative cases have been demonstrated.

## Getting current SP and gz-skills

Check upstream at adoption time rather than assuming this template's baseline
is newest. SP's latest stable release is **v7.0.0**, checked October 11, 2026,
and selected at full SHA `bb92a77741419a4ab5f06e711a283343f1ada0c3` in the
0.3.2 development template. The starter also pins gz-skills v0.8.0, checked against the latest official
release on October 18, 2026. It adds explicit-only release support; adopting
it does not authorize release publication. These observations expire as
releases change. Read the [SP update assessment](evidence/2026-10-11-superpowers-7.0.0.md).
Backplane remains disabled and does not constrain active SP version selection;
review its readiness and compatibility before any future enablement.

From a shell with authenticated GitHub CLI, obtain each latest published release
and resolve its tag to a full commit SHA:

```bash
sp_tag=$(gh api repos/obra/superpowers/releases/latest --jq .tag_name)
sp_revision=$(gh api "repos/obra/superpowers/commits/$sp_tag" --jq .sha)
gzs_tag=$(gh api repos/tvproductions/gz-skills/releases/latest --jq .tag_name)
gzs_revision=$(gh api "repos/tvproductions/gz-skills/commits/$gzs_tag" --jq .sha)
printf 'SP: %s %s\nGZS: %s %s\n' "$sp_tag" "$sp_revision" "$gzs_tag" "$gzs_revision"
```

Review the release notes and installation guidance at each exact revision:
[SP releases](https://github.com/obra/superpowers/releases) and
[gz-skills releases](https://github.com/tvproductions/gz-skills/releases).
A failed query is not proof that a release is absent. Resolve network or access
errors before choosing a version. Do not run upstream bootstrap scripts blindly.

Latest published release and latest development commit are different choices.
For an explicitly requested development version, resolve `commits/HEAD` through
the same repository API, review its changes, and record its full SHA with release
set to null and status identifying an unreleased development snapshot. Never put
`main`, `HEAD`, or a moving tag in the catalog's revision field. gz-skills v0.8.0
ships project setup; inspect the selected version's profile contract and retain
an explicit user profile choice. Preserve approved starter Python policy over
upstream defaults. Proposals are not shipped
capabilities just because they appear on main.

To adopt newer versions in the shared starter:

1. Change each selected component's release, revision and accurate status in
   `bundle.json`. Keep SP-BP disabled. Updating SP or gz-skills does not depend on
   Backplane's old compatibility baseline while Backplane is deferred.
2. Change the corresponding full SHA in both native catalogs:
   `.agents/plugins/marketplace.json` and `.claude-plugin/marketplace.json`.
   Keep upstream ownership and plugin names intact.
3. Run the repository's tests, bundle validation and lint/format checks. Publish
   the reviewed starter revision and record host verification separately.
4. For a new adopter, configure from that reviewed starter checkout, then follow
   the active host's native installation steps above. For an existing adopter,
   review the configuration/lock/entry-skill diff as described below; the helper
   deliberately refuses to overwrite older managed files.
5. Use the installed host manager's supported update/reinstall operation after
   reviewing its current help. Verify the selected marketplace source, actual
   loaded revision and fresh-session skill discovery; a manager saying “updated”
   or a changed lock alone does not prove that the newest selected source loaded.
   Retain the prior pins for rollback.

Do not edit cached upstream skills, duplicate their installation under a second
marketplace, or silently update unrelated projects. To use a project-specific
version ahead of the shared baseline, record it in a separately reviewed catalog
and reconcile the existing discovery source explicitly. Do not leave the shared
bundle lock claiming one revision while another is installed.

## Maintaining the adopted stack

Adopters maintain four independent sources: this starter template, SP, SP-BP and
gz-skills. A copied template, pinned bundle or installed plugin does not establish
freshness. Review them at adoption, scoped upgrades and quarterly on-demand
maintenance alongside the [Python baseline](project-configuration.md#keep-the-baseline-current).
Adopters choose whether to reconcile updates from this starter, maintain their
dependencies directly from upstream, or combine both approaches. They own update
timing and project compatibility verification. The starter maintains a reviewed
baseline; its [scheduled scanning policy](baseline-policy.md#scheduled-dependency-scanning)
covers standard and X-Plane cases independently and imposes no adopter schedule.

Route authorized dependency/tool updates through gz-skills'
`gzs-update-dependencies` and dependency-risk reviews through
`gzs-dependency-risk-audit`, subject to project scope and authorities. The source
inventory and native adoption requirements below are the starter's binding to
those portable workflows. The pinned gz-skills v0.8.0 maintenance skill supplies
freshness-only reporting and template/plugin inventory. Review mode leaves pins
and environments unchanged. This starter adds no competing command and does not
select a lite/heavy profile or invoke setup as part of a bundle update.

1. Read `.skills-first/bundle.lock.json`, project configuration and native manager
   inventory. Record the adopted starter SHA, component SHAs, selected versions
   and actual loaded sources. A generated template also carries copied files;
   inventory project changes before comparing them with newer starter material.
2. Check official upstream sources independently:
   [starter](https://github.com/tvproductions/gz-skills-first-starter),
   [SP releases](https://github.com/obra/superpowers/releases),
   [SP-BP releases](https://github.com/tvproductions/superpowers-backplane/releases)
   and [gz-skills releases](https://github.com/tvproductions/gz-skills/releases).
   Assess the latest stable release, including new families, against project
   compatibility policy. Review family changes and record any retained older
   release as an explicit exception; an old range is not proof of freshness. For sources with no
   published release, record that fact and a reviewed full published commit SHA;
   label it as an unreleased snapshot. A successful query with no release is
   different from an authentication/network failure. Never record moving branches
   or tags as immutable revisions.
3. Keep a project maintenance receipt in the existing decision/handoff authority:
   checked date, selected/latest release or SHA, evidence links, compatibility
   findings and independent adopt/defer decisions for all four. Record a reason
   and revisit condition for a retained older revision. Template maintenance may
   adopt useful guidance without wholesale copying of newer scaffold files.
4. For an authorized update, preview the concrete diff from a separate reviewed
   newer starter checkout. Review changelog changes to baseline policy as well as
   dependency versions. Reconcile instructions, managed lock/configuration and
   project policy references together; preserve app dependencies, settings, overrides,
   profile choices and native manager state. The helper refuses differing managed
   files: there is no force overwrite or automatic template migration. Run project
   checks, use the host's supported update operation and verify fresh-session
   discovery. Retain the earlier configuration and source pins for rollback.

Review SP and gz-skills without waiting for SP-BP. Track Backplane's updates and
readiness even while disabled; a newer revision or first release alone does not
authorize activation or prove compatibility. Its pre-release host acceptance
limitations remain until independently verified and adoption is explicit.
Python/tool-family preferences stay in the starter/project binding; do not edit
the upstream plugins to impose them.

## Updates and rollback

Components remain separately owned. Do not update upstream Superpowers as a
side effect of a Backplane update. Review candidate revisions and compatibility,
change `bundle.json` and both catalogs together, then run the repository checks
and affected host tests before publishing the starter change.

The configure helper intentionally refuses an existing different lock or
marketplace revision. For an adopter update, review a diff of the new lock,
marketplace ref and instructions fragment; commit the accepted configuration
change, then use the native manager's supported update/reinstall route. No
force-overwrite or automatic update command is shipped. Preserve the prior refs
and restore the prior reviewed configuration and plugin revisions if verification
fails. Recheck discovery after either update or rollback.

To remove the stack, first inspect whether other projects use the cached plugins.
Remove this project's enablement/configuration after review. Use native plugin
removal only for installations no longer needed; never delete shared caches by
hand. Preserve app skills, operational records, and unrelated configuration.
