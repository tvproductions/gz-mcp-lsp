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
The starter does not select a gz-skills profile. The pinned gz-skills v0.8.3
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

## Repository-owned installation and brownfield repair

Agents MUST use repository-owned settings for all three hosts. Existing global
or user installations MAY remain; they do not own the project's selected versions,
activation or commands. Agents MUST NOT uninstall global copies, rewrite user
defaults or broaden activation as a shortcut. Installation, version updates and
enablement are separate operations. Shared native caches and installation
registries are storage; project activation must remain local.

From a reviewed starter checkout, select the adopter's host on configure:

```bash
uv run --locked skills-first-starter configure --project /path/to/project --host codex --starter-ref FULL_STARTER_SHA
uv run --locked skills-first-starter configure --project /path/to/project --host codex --starter-ref FULL_STARTER_SHA --apply
```

Use `claude` or `opencode` for that host. The managed lock records non-Codex host
selection; legacy records without `host` retain Codex semantics. Status checks
the recorded host. This capability starts with 0.8.0.
Configure preserves existing compatible settings and refuses conflicting adoption
records. It does not install plugins or certify discovery.

For brownfield activation repair, use the separate project-only command:

```bash
uv run --locked skills-first-starter localize --project /path/to/project --host codex --starter-ref FULL_STARTER_SHA
uv run --locked skills-first-starter localize --project /path/to/project --host codex --starter-ref FULL_STARTER_SHA --apply
```

Repeat for each client the project uses. `localize` reads user plugin identities
for Codex/Claude and writes project overrides: the starter source is active,
inherited duplicate sources are disabled locally, and Backplane stays disabled.
Claude's existing local settings layer is repaired too. OpenCode receives local
ID exclusions before its pinned package targets. The command preserves existing
project marketplace sources, unrelated settings, adoption records and adopted
component pins; an unadopted project uses the reviewed starter's component pins.
It does not edit user settings or uninstall anything. OpenCode JSONC is updated
in place while preserving comments and unrelated fields. Ambiguous simultaneous
JSON/JSONC files and v1 adapters require explicit reconciliation.

Agents MUST inspect the preview and diff, run the applicable native procedure
below, and verify inside-project activation plus an outside-project control.
Record actual installed revisions independently of declared refs. Do not call
adoption complete while required runtime evidence is missing or mismatched.
See the [three-host evidence](https://github.com/tvproductions/gz-skills-first-starter/blob/3f76acf0038b030bf5abd85ce4a419e890d3e420/docs/evidence/2026-10-31-three-host-repo-scope.md).

## Codex

Repository/project scope is required for this stack's installation, marketplace
registration and enablement. Do not use global/user-level installation as the
default or as a fallback. Native download caches may live under the user's home;
that storage location does not authorize user-wide installation or activation.

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
out, let the native runtime resolve the pair selected by the project's
`.codex/config.toml`, then inspect `codex plugin list --json`. This path has
verified native discovery without an unscoped installation command; see the
[development discovery receipt](https://github.com/tvproductions/gz-skills-first-starter/blob/3f76acf0038b030bf5abd85ce4a419e890d3e420/docs/evidence/2026-10-31-native-development-skills.md).

Codex CLI 0.166.0's `plugin add` unconditionally enables the plugin in
user-wide configuration, even when invoked from a project with a local
marketplace. Running it from the repository does not make it project-scoped.
Do not use it for project installation, updates or reinstalls. Do not run
unscoped `codex plugin marketplace add` either. The verified CLI 0.166.0 has no
project-scope option for those commands. Use project-owned native configuration
instead. Keep installation, version updates and enablement as separate
operations; authorization to update a version does not authorize activation or
a change of enablement scope.
If a host requires a separate installation action, use it only with verified
repository/project scope. Otherwise record installation/discovery as pending;
do not substitute a global/user install. Preserve existing user defaults.

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
installations first. Register the reviewed marketplace through project-owned
settings using the host's verified current syntax, then use Claude's project
scope for installation:

```bash
claude plugin marketplace add /path/to/reviewed-starter --scope project
claude plugin install superpowers@skills-first-starter --scope project
claude plugin install gz-skills@skills-first-starter --scope project
```

These exact scope options were checked with Claude Code 2.1.316 CLI help.
Run them from the adopting project's root. Inspect project settings afterward;
do not omit `--scope project`, whose default is user scope. End-to-end Claude
installation and fresh-session discovery still require host verification.

The displayed catalog pins component source revisions. For repeatable adoption,
register a reviewed marketplace checkout at a recorded full SHA in project-owned
settings. Do not use an unscoped marketplace-add command that writes user/global
settings. Check the manager's current syntax and actual scope before executing;
if project registration is unsupported or unverified, report that gap instead
of installing globally/at user scope. Restart and verify actual SP and gz-skills
discovery. Backplane remains deferred.
Marketplace syntax validation
alone is not a completed installation or lifecycle proof.

The 0.8.0 helper generates project settings with `--host claude`; it does not
run the native installer. The scoped install and activation checks are recorded
in the three-host receipt. Fresh desktop/model invocation and Backplane Claude
lifecycle acceptance remain separate requirements.

## OpenCode

Use OpenCode v2. The pinned SP 7.0.1 and gz-skills 0.8.3 releases already own
their v2 adapters; this starter configures them and authors no competing adapter.
Generate project `opencode.json` using `configure --host opencode`, or repair
existing activation using `localize --host opencode`. The project `plugins`
array contains full-SHA Git package specifications for the active pair.
Backplane's OpenCode lifecycle remains deferred and MUST NOT be activated.

Do NOT run `opencode plugin add` or `plugin remove`: the 2.2.0 CLI defines those
as global configuration operations. Maintain version selections by reviewing
the repository's config/lock and using its upstream maintenance workflow.
On OpenCode 2.2.0, repository configuration alone cannot override an inherited
plugin with the same ID: native resolution retains the earlier source and marks
the project copy as a duplicate. Agents MUST use the starter's scoped launcher:

```bash
uv run --locked skills-first-starter run-opencode --project /path/to/project
uv run --locked skills-first-starter run-opencode --project /path/to/project -- plugin list
uv run --locked skills-first-starter run-opencode --project /path/to/project -- api skill.list
```

Run these from the reviewed starter environment. The launcher performs substantive
configuration reconciliation: it retains ordinary user preferences, excludes
inherited plugin declarations, uses the repo's config directory and explicit
project file, restores explicit project skill paths, and starts a private server.
It writes no user settings and persists no copied preferences/secrets. It blocks
global plugin add/remove and attachment to a shared server. This is a native
environment workaround, not a patched OpenCode distribution. System-managed
policy still applies. Existing global plugins remain installed for other projects.
The tested inherited-source fixture loads the correct local pin through this
route; plain native startup failed that brownfield test. Do not claim plain
startup is scope-correct on this host version.

Keep the server running while missing
packages install in the background. An immediate one-shot list may be empty
before loading completes. Inspect the native state after startup:

```bash
uv run --locked skills-first-starter run-opencode --project /path/to/project -- plugin list
uv run --locked skills-first-starter run-opencode --project /path/to/project -- api skill.list
```

Require SP and gz-skills to be active, verify their source targets and entry
skills, then inspect an outside project. Its state must retain the user's own
defaults. The tested 2.2.0 server reports the exact pinned package SHAs and no
starter skill leakage outside. See
[OpenCode v2 configuration](https://dev.opencode.ai/v2/docs/plugins).

## Getting current SP and gz-skills

Check upstream at adoption time rather than assuming this template's baseline
is newest. The October 31, 2026 release review selects SP **v7.0.1** at
`2ce8aa15d05bd57213e6f746f953aafb7ded7a8b` and gz-skills **v0.8.3** at
`d6acc26e28ca1c4f43e5bb46d8973021d7d006c3`. These observations expire as
releases change. See the [0.8.0 release review](https://github.com/tvproductions/gz-skills-first-starter/blob/3f76acf0038b030bf5abd85ce4a419e890d3e420/docs/evidence/2026-10-31-0.8.0-release.md).
Explicit-only release support does not authorize publication by adoption.
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
those portable workflows. The pinned gz-skills v0.8.3 maintenance skill supplies
freshness-only reporting and template/plugin inventory. Review mode leaves pins
and environments unchanged. This starter adds no competing command and does not
select a lite/heavy profile or invoke setup as part of a bundle update.

Treat this as a freshen-up workflow. End every freshness review with a concrete
recommended upgrade batch and an explicit offer to apply it. Strongly recommend
supported policy-compliant updates; identify targets, benefits, compatibility
risks and required checks. An inventory or adopt/defer table alone is incomplete.
In review mode, leave dependency state unchanged until updates are authorized.
When updates are already authorized, perform and verify them without asking
again. Explain evidenced deferrals; if everything is current, state that no
upgrade is needed. This is the starter's binding to the upstream skill, not a
claim that the pinned skill already requires this closing behavior.

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

Before any native plugin update, record the selected and actual installed
revisions, project enablement, user defaults and any duplicate-source overrides.
Choose a version-update operation that preserves those settings. Inspect its
side effects before execution; an install/reinstall command is not automatically
a scope-preserving updater. In Codex CLI 0.166.0, do not substitute `plugin add`:
it enables the plugin user-wide regardless of the project's local marketplace.
Use reviewed project configuration and native resolution, then compare actual
installed revisions and effective enablement with the recorded state. Verify
outside-project behavior too. A requested update must leave disabled plugins
disabled and project-only plugins project-only. If native resolution cannot
deliver the requested revision without changing scope, report the update as
pending; do not broaden activation or claim success from an advertised ref.

Components remain separately owned. Do not update upstream Superpowers as a
side effect of a Backplane update. Review candidate revisions and compatibility,
change `bundle.json` and both catalogs together, then run the repository checks
and affected host tests before publishing the starter change.

The configure helper intentionally refuses an existing different lock or
marketplace revision. For an adopter update, review a diff of the new lock,
marketplace ref and instructions fragment; commit the accepted configuration
change, then use a verified scope-preserving native version-update route. No
force-overwrite or automatic update command is shipped. Preserve the prior refs
and restore the prior reviewed configuration and plugin revisions if verification
fails. Recheck discovery after either update or rollback.

To remove the stack, first inspect whether other projects use the cached plugins.
Remove this project's enablement/configuration after review. Use native plugin
removal only for installations no longer needed; never delete shared caches by
hand. Preserve app skills, operational records, and unrelated configuration.
