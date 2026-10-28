# Canonical template updates

This is the maintained entry for adopters checking or migrating the starter.
Version 0.6.0 adds the single template-owned `update-gz-template` skill to make
this method discoverable inside an adopting project. Version 0.5.0 and earlier
do not contain it; use the bootstrap below or follow the
[adoption/upgrade runbook](adoption-0.5.md) directly.

## What an adopter invokes

After the skill is available in a fresh project session:

```text
Use $update-gz-template to check this project's adopted starter against the
latest published stable release. Explain policy and migration changes; apply
no updates.
```

To perform a scoped migration instead:

```text
Use $update-gz-template to upgrade this project's adopted starter to the reviewed
published target. Preserve project changes, reconcile managed files together,
run the required verification, and report remaining conformance/readiness gaps.
```

The request establishes review versus update mode. Invoking a skill alone does
not authorize an upgrade, plugin activation, publication, or notifications.
Generic dependency work remains with `gzs-update-dependencies`; template updates
do not implicitly refresh the whole runtime/tool/plugin stack.

## Canonical sequence

1. Read project authorities and `.skills-first/bundle.lock.json`. Record current
   starter version/full SHA, component pins, explicit lane and local changes.
   Unknown provenance requires investigation, not a guessed version.
2. Query canonical published releases. Respect the requested release or select
   the latest stable; resolve the tag's full commit in a separate clean checkout.
   Match tag, HEAD and manifest. Neither main nor a matching version label proves
   published identity. A failed network query leaves latest status UNKNOWN.
3. Read target release notes, intervening changelogs, baseline/versioning and the
   current runbook linked from adoption-workflow. Classify policy versus pin
   changes. Use review mode to report without changing adopter files/environments.
4. For an authorized update, follow the target's brownfield upgrade path:
   original managed content versus current local edits versus generated target
   candidates. Reconcile the lock, host tables, fragment, policy references and
   native update skill together. Preserve local guidance, product dependencies,
   lane, behavior and rollback. No force overwrite is provided.
5. Run the required checks and record actual evidence. Keep file configuration,
   Python conformance and native discovery separate. Changed required inputs
   invalidate affected proof. Report unresolved migration honestly; updating a
   recorded version does not certify acceptance or make every component current.

The skill is a compact entry to this method, not a resolver, automatic file
merger or conformance engine. Use the installed upstream maintenance skill when
available; its absence does not prevent following the published runbook directly.

## New adopters and bootstrap for older adopters

Version 0.6's configure preview includes
`.agents/skills/update-gz-template/SKILL.md`. Apply writes that one owned skill
and refuses conflicting content or symlinked destinations. Wheels carry the
same checked source. Existing app skills are preserved; no upstream skill trees
are copied. This path is the project discovery contract used by the Codex
helper; other hosts' discovery must be verified using their native facilities.

For 0.5.0 and earlier adopters, either reconcile the complete upgrade or bootstrap
just the skill. The [v0.7.1 release](https://github.com/tvproductions/gz-skills-first-starter/releases/tag/v0.7.1)
provides `update-gz-template-0.7.1.zip` and SHA256 checksums. Download and verify
those assets, then unpack the ZIP into a disposable review directory. It contains
only `update-gz-template/SKILL.md`. This bootstrap needs no project environment
changes. Alternatively, obtain and verify the release in a separate checkout
and generate candidates using its helper. In either case:

1. Read `templates/skills/update-gz-template/SKILL.md` at the verified release.
   Review its content and inventory any same-name project/global installation.
   Avoid installing duplicate discovery sources.
2. Compare the staged skill with the canonical source at the verified release.
   Review and copy that
   single skill to the corresponding project path only if it is absent and its
   parents are real project directories. Existing content requires reconciliation;
   do not overwrite it to make setup pass.
3. Record the skill's source version/full SHA in the existing project authority.
   A bootstrap is not a completed template migration: keep the adopter's lock
   identifying its actual prior baseline until all managed content is reconciled.
4. Start a fresh project session and verify the skill's name/source and invocation.
   File bytes and helper tests do not prove actual host discovery. For a host
   without verified discovery, point the agent directly to the reviewed SKILL.md
   or this canonical document and report native availability as unverified.

Local edits to the owned skill are protected like edits to the instructions
fragment. A later configure/status may report a conflict; reconcile old/current/
target guidance rather than deleting the edited file. Update bootstrap provenance
when adopting a newer skill. Never publish a new template version or change an
adopter product's own SemVer merely because this skill was added locally.
