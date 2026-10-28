# Adopt the skills stack

For recurring template updates and pre-skill adopter bootstrap, use
[canonical template updates](updating.md). Version 0.6 adds one native
update skill; 0.5 and earlier adopters can bootstrap it from the published release.

For the required greenfield, brownfield first-adoption and existing-adopter
upgrade paths, start with [the 0.5 runbook](adoption-0.5.md). Explicit lane selection
and applicable adoption/release analysis are required in both lanes. The helper
still configures files only; it does not automatically enforce acceptance.

This document guides adoption; it does not replace the three upstream workflows.
Read [the adoption guide](adoption.md) for native host loading,
compatibility checks, updates, and rollback. The helper is
[starter.py](../starter.py); use its CLI help for current options.

For structural adoption in an existing project, read
[backport guidance](backport.md). Run the read-only assessment, map
existing sources to proposed targets, and implement only useful, authorized
changes with project verification. Configuration adoption does not move code.

Full Python baseline adoption requires the
[Astral alignment contract](engineering/astral-alignment.md). Inventory layout,
packaging, configuration and enforcement gaps, then implement necessary
refactoring within the authorized project scope. Preserve public behavior and
project authorities. Existing layout is not automatically exempt; compatibility
exceptions require evidence, an owner and revisit condition. Configuration-only
work reports the remaining migration explicitly.

Use the [Astral acceptance contract](engineering/astral-acceptance.md) to record
each requirement, actual evidence, applicability and owned exceptions in the
project's existing authority. Follow the [worked migrations](engineering/astral-migrations.md)
for application, typed-library and workspace paths. Reconcile effective uv/Ruff/ty
configuration, exact selected environments, executable provenance and clean
installed behavior before claiming full Python acceptance. File configuration
and fresh-session native discovery remain separate results.

Before choosing versions, use the adoption guide's “Getting current SP and
gz-skills” procedure. Check latest published releases, distinguish development
main from a release, and record reviewed full SHAs. The starter pins are a
baseline, not an instruction to keep SP behind because Backplane is deferred.
Also use its “Maintaining the adopted stack” procedure for the starter template,
SP, SP-BP and gz-skills at adoption and scoped maintenance. Compare recorded
provenance with upstream releases/commits, preserve app additions and overrides,
and record independent adopt/defer decisions. Track SP-BP updates without
enabling it while readiness and explicit adoption remain pending.
Generic maintenance routes to gz-skills `gzs-update-dependencies` for authorized
updates and `gzs-dependency-risk-audit` for risk assessments. Keep the starter's
role to policy and adoption bindings; do not add a competing local maintenance
skill. The pinned gz-skills v0.8.0 maintenance skill also supports freshness-only
reviews and starter/plugin inventory without changing pins or environments.
Preserve approved starter Python policy over upstream profile defaults; choosing
a profile remains explicit and separate from helper configuration, but is
required before adoption can be called complete.

Establish the exact target project and a reviewed published starter revision.
Read the starter's [versioning contract](versioning.md). Record its
declared template version and exact SHA independently of the app version;
confirm published release/tag identity separately. Legacy unversioned locks
require reviewed reconciliation, never an inferred label or silent rewrite.
Read the [project configuration contract](project-configuration.md);
inventory app dependencies, locks and settings, preserve additions and reviewed
overrides, and report freshness/adoption gaps. The helper leaves these files
untouched and does not resolve packages or load application settings.
Inspect project instructions, existing plugins and skill discovery, and gzkit
ownership. Keep app rules and existing user changes. Do not make a copy of an
upstream skill tree or install the same skill through two discovery contracts.

Run `uv run --locked skills-first-starter configure --project <root>` from this starter checkout.
Inspect its preview, then apply the already-authorized adoption with `--apply`.
A conflict requires reconciliation of the specific source or file; do not remove
other installations or use a force overwrite to make it pass. Existing AGENTS
stays untouched: review the generated fragment and add a pointer within scope.
Profile choice is separate; do not infer lite/heavy from the components selected.

Native installation is a separate, explicit operation. Follow only the guide for
the active host; preserve project scope and existing upstream versions. For a
configuration-only request, stop after configuration and identify installation
as pending. OpenCode is deferred until Backplane's upstream adapter is ready.

SP-BP is an expected addition to the target stack and is disabled by default. Preserve existing backlog/handoff practice; do not
install or activate Backplane as part of ordinary adoption. Its future activation
requires an explicit readiness review and configuration change.

Verify actual SP and gz-skills discovery in a fresh session. If Backplane is later
explicitly adopted, also verify its compatibility contract. Record exact sources and PASS/FAIL/UNKNOWN; status/configuration is not
proof of loading. GitHub authentication, a real issue preflight, and any mutation
scenario require the corresponding authorized environment. Do not operate on
production issues just to test installation. Backplane's manifest version does
not prove a published release or cross-harness readiness.
