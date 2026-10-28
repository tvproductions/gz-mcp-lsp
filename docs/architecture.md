# Architecture and ownership

The starter owns one narrow `update-gz-template` skill, introduced in 0.6 as the canonical entry for adopter template updates. Generic
engineering and dependency-update skills remain upstream-owned. It owns opinionated
project policy, deterministic adoption tooling, configuration and provenance;
upstream plugins and adopting projects own their skills. See the
[structure contract](structure.md) and [migration guide](migration-0.3.md).

This repository is the shared policy alignment source for gz-skills and
Backplane; see [the consistency contract](versioning.md#ecosystem-policy-authority-and-consistency).
Those repositories retain local release execution and independent versions.
Backplane owns requirements tracking, labeling, backlog/release monitoring,
handoffs and [lite/heavy definitions](https://github.com/tvproductions/superpowers-backplane/blob/main/docs/superpowers-backplane/modes.md).
The template refers to those workflows without implementing a competing
lifecycle. Its own release records and session handoffs are ordinary project
records, not a generic lifecycle supplied to adopters. Neither companion must
install this template's bundle to consult its policy.

One bundle catalog tracks three independently maintained plugins. SP and
gz-skills are enabled by default; Backplane is an expected addition to the target
stack, pinned but deferred pending readiness and explicit adoption. Its two
native marketplace adapters refer to immutable upstream revisions; they do not
contain authored copies of those skill trees.

```text
Project AGENTS and domain authorities
  -> direct workflow references -> SP (feature work) + gz-skills (engineering)
  -> existing backlog/handoff practice; SP-BP deferred
  -> project-owned operational skills
  -> project-owned deterministic code and adapters
  -> versioned operational records and generated products
```

The adoption helper is standard-library Python. It previews before writing,
checks all intended files before changing any, preserves unrelated TOML bytes
and existing AGENTS content, refuses conflicting managed files and discovery
copies, and never invokes a native install, remote model, or GitHub mutation.
Existing projects preserve their app layout during configuration, then reconcile
it with the required [Astral baseline](engineering/astral-alignment.md) through
reviewed refactoring or evidenced compatibility exceptions. Empty projects get the same minimal
configuration and entrypoint, rather than a speculative web or database stack.

Application dependency declarations, locks and settings remain project-owned.
The [configuration contract](project-configuration.md) permits additions,
extensions and reviewed overrides and separates shared baseline maintenance from
adopter updates. The helper preserves those files; it supplies no application
settings loader or automatic dependency merge.

`bundle.json` is desired composition. `.skills-first/bundle.lock.json` in an
adopter records selected sources. Neither is a runtime readiness receipt. Actual
loaded skills, native scope, trust, and conformance require a fresh host session.

`bundle.json` also owns the template's independent `template_version`. New
adopter records carry that label alongside the exact starter SHA; neither proves
a published release. The starter's package metadata mirrors its version without
binding an adopter's app version. See [versioning](versioning.md) for compatibility,
immutable release tags and preservation of legacy unversioned records.

FDAU supplies the primary precedent: portable disciplines, separate upstream
Superpowers, project adapters, domain rules, and independently inspectable
verification. Its older checkout/discovery surfaces are evidence, not instructions
to copy them over the native plugin installation contract.

Backplane's current skills companion and the proposed broader Python backplane
are different maturity targets. This starter supports the existing pinned package
without pretending the proposed requirements/traceability/release system has
shipped. gzkit remains a separate ecosystem; its ledger and lifecycle are not
imported here.

Project-specific constraints stay behind project seams. Public catalog and
starter changes must not carry real operational records, credentials, machine
paths, or sensitive source data. Examples and tests use invented fixtures only.

The starter writes an instructions fragment with direct workflow references.
Configure seeds only `.agents/skills/update-gz-template/SKILL.md`; legacy starter
copies still require reviewed reconciliation. Upstream skill trees are never copied. The
read-only `backport` assessment supports an agent-led source mapping and verified
refactoring; it does not relocate app files or impose heavy-profile governance.

The starter owns the [Python engineering binding](engineering/python.md):
required runtime, idiom, tool, architecture and on-demand hygiene standards for
its non-gzkit projects. gz-skills retains portable discipline ownership. The policy is ordinary versioned documentation in `docs/engineering/`;
on-demand analysis utilities live in `tools/engineering/`. Read it from a reviewed
checkout or reconcile it into project-owned documentation with provenance.
Shared-versus-local utility ownership has not been established. Existing-project
adoption remains a preservation-first design task, not an automatic rewrite.

Strong Python and tool preferences are starter-owned: Ruff + complexipy +
Lizard, with periodic on-demand dependency freshness review. gz-skills and SP
remain portable and agnostic; SP-BP should be agnostic too. Backplane is still
expected and deferred. No upstream plugin policy or pin changes follow from
this preference. Each adopting project binds the portable workflows to its
reviewed tool choices and measurements.

Generic dependency maintenance is owned by gz-skills: authorized updates route
to `gzs-update-dependencies`, and dependency-risk assessments route to
`gzs-dependency-risk-audit`. This starter supplies release-family policy, project
bindings, bundle/catalog consistency and preservation requirements. It does not
add a parallel maintenance skill or generic freshness reporter. The pinned
gz-skills v0.8.0 supplies freshness-only assessment and template/plugin inventory
through its maintenance skill. Starter bindings preserve approved Python policy
over upstream profile defaults; no setup invocation or profile selection follows
from changing the bundle pin.

Scheduled dependency scans and update PRs are permitted for this repository's
standard and X-Plane baselines under the
[scanning contract](baseline-policy.md#scheduled-dependency-scanning). They do
not replace compatibility review or gz-skills' maintenance workflows. Adopters
choose their own update sources and timing; no scanning service is installed by
the adoption helper.
