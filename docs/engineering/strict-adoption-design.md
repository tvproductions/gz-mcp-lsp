# Strict adoption and release design

Status: design/decision record, October 24, 2026. Version 0.5.0 delivers the
confirmed policy through baseline/engineering instructions and the
[greenfield/brownfield runbook](../adoption-0.5.md). The helper remains
configuration-only; automatic evidence/PRD validation and upgrade merging below
remain proposed. Observations and discussion-save verification retain their
pre-release context. This record does not certify another project's adoption.

Confirmed in the October 24 discussion:

- The template is Python-exclusive in both adoption lanes. Other languages,
  likely including Go, are future scope requiring a separately designed baseline.
  Keep the current conformance work Python-specific.
- The primary audience is the maintainer's own projects and engineering
  consistency; public reuse is welcome. Opinionated choices are intentional.
  Future guidance will cover CLIs, TUIs, web apps and desktop apps per language
  and environment. Model those as target-specific requirements extending a
  shared foundation, with explicit support and proof for each claimed target;
  current CLI support does not establish a completed application-type matrix.
- Make MAJOR.MINOR.PATCH classification explicit for adopter products, including
  the 0.x rule, stable public-contract compatibility and major-release PRDs;
  app, starter and plugin release identities remain independent.

- Keep the intended full/heavy design consistent with Backplane, which is under
  development. Do not invent a replacement full lane to bypass its readiness.
  Track intended composition and observed component readiness separately.
- Require deeper analysis at adoption and release acceptance. Keep the ordinary
  four-hook routine distinct; this changes the former on-demand-only execution
  policy and needs corresponding implementation and released adopter guidance.
- Work existing and underway projects through migration to compliance, retaining
  explicit incomplete results until the required evidence is established.

## Required outcomes

The user requires strict, extensive uv Projects alignment for adopters, mandatory
lite or full/heavy lanes, a practical route for underway projects to conform,
and release rules that deliver approved policy to adopters. Release planning
must retain a newly written PRD for every major, including 1.0.0. Discuss the
other opinionated choices before silently extending their scope or enforcement.

Both lanes must meet the same applicable Python foundation. Lite reduces
workflow/governance weight; it does not waive packaging, configuration, runtime,
dependency, artifact, or verification requirements. An absent/null lane is
pending adoption, never a completed third lane.

## Observed gaps

- Published v0.4.1 already requires maximal Astral alignment, but main adds
  stronger acceptance requirements while still declaring 0.4.1. The two commits
  after that release were synchronized without a new release. The implementation
  plan explicitly deferred publication to a future minor.
- `profile_check()` accepts absent settings and a null profile. Instructions
  explicitly separate profile selection from adoption. Tests preserve this
  behavior; it is a designed gap relative to the user's clarified intent.
- `configure` and `status` concern managed files and cannot prove Python
  acceptance. The A01–A18 acceptance record is prose, not an enforced release
  prerequisite. Routine CI does not validate an adopter's evidence.
- Default source provenance accepts a clean canonical checkout HEAD, including
  unreleased main. A supplied 40-character SHA is not by itself proof of a
  published tag, matching resources, or trusted upstream origin.
- Existing managed-file conflicts stop writes, but there is no supported
  reconciliation command that previews a three-way policy upgrade.
- The pinned upstream heavy profile calls for SP and Backplane; this starter
  enables SP even without a lane, but deliberately defers Backplane. Full/heavy
  readiness cannot honestly follow from a profile string alone.
- Deeper analyzers are required selections but execution is prohibited in hooks
  and CI. Some compatibility and allowed-family decisions remain unsettled.

Authorities: [acceptance](astral-acceptance.md), [implementation plan](astral-implementation-plan.md),
[adoption](../adoption-workflow.md), [versioning](../versioning.md),
[configuration](../project-configuration.md), `src/skills_first_starter/cli.py`,
`tests/test_starter.py`, and the
[pinned upstream setup skill](https://github.com/tvproductions/gz-skills/blob/75bcd11ee9371ecff1a7b3432d2af29d4bdbb788/skills/gzs-project-setup/SKILL.md).

## Define complete uv Projects coverage

The policy must inventory every section in the nine linked Projects concept
pages, not only the introductory page or a fixed subset of CLI switches. Retain
source URL/section, review date, content digest, tested uv version, requirement
ID, applicability trigger, selected supported behavior, verification method,
and result. Preserve a reviewed local source inventory so later documentation
changes can be compared without silently changing an adopter's policy.

The following coverage map was checked against live documentation on October 24.
It is a design map; it is not a completed new conformance certificate.

| Projects authority | Required contract and evidence |
| --- | --- |
| [Structure and files](https://docs.astral.sh/uv/concepts/projects/layout/) | Project identity, pyproject authority, project-owned environment, uv-managed committed lock; distinguish universal resolution from executed platform coverage. Review centralized environments if proposed. |
| [Creating projects](https://docs.astral.sh/uv/concepts/projects/init/) | App/library/native/coordinator kind; packaged src baseline, entry points and typing where applicable; inspect pinned-version generated output. Document why unpackaged/bare alternatives are excluded from ordinary runtime packages. |
| [Dependencies](https://docs.astral.sh/uv/concepts/projects/dependencies/) | Runtime/extras/groups/build inputs, markers, bounds, indexes and Git/URL/path/workspace sources; editable/virtual semantics, group Python constraints, conflict declarations, and published metadata independent of development sources. |
| [Running](https://docs.astral.sh/uv/concepts/projects/run/) | Selected project/environment, interpreter and executable origin; wrappers, external executables, overlays, inline scripts, platform wrappers and signal behavior when used. Baseline proof must use the selected locked tools. |
| [Locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/) | Lock consistency, exact selected environments, extras/groups, update boundaries, editables, partial installations and exports. Frozen/no-sync/inexact controls cannot substitute for the required proof. Review preview malware checks explicitly. |
| [Configuration](https://docs.astral.sh/uv/concepts/projects/config/) | Supported Python, all used entry-point kinds, effective packaging/environment settings, isolation and build augmentation, deployment editability, conflicts and supported/required resolution environments. |
| [Building](https://docs.astral.sh/uv/concepts/projects/build/) | Default sdist-to-wheel build, source-independent build, inventories, exact build inputs distinct from runtime lock, clean installed behavior; assess build constraints/hashes and private publication controls. |
| [Exporting](https://docs.astral.sh/uv/concepts/projects/export/) | Identified downstream consumer and locked generation where exports exist; uv.lock remains authoritative. No competing hand-maintained requirements lock. Explicit decisions for pylock and preview SBOM. |
| [Workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/) | Membership, root kind, source precedence, explicit dependency edges, selected members, shared compatibility, isolated member distributions and undeclared-import negative control. Use independent projects where environments conflict. |

Each applicable requirement needs observed evidence. Every N/A requires a
trigger-based reason. Missing, inconclusive, stale, or failed evidence blocks
strict acceptance. Supported alternatives are evaluated against the chosen
starter contract; mutually exclusive options need not all be enabled. Preview
features require a reviewed decision, not blanket activation. Follow linked
configuration/backend/integration references wherever a selected behavior needs
them. Documentation coverage alone cannot establish runtime correctness.

An exception must never count toward a “100% conformant” claim. If departures
are retained for host compatibility, expose a separate nonconforming/exception
result with owner, evidence and revisit condition. Decide whether such a result
may release; it cannot silently become strict acceptance. XPPython3 needs
separate host proof and a declared scope, not an invented standalone replacement
for its embedded interpreter.

## Mandatory lanes and honest acceptance

Record the selected lane explicitly using the upstream settings contract. Keep
starter-specific policy/evidence outside `.gz-skills/settings.json`; do not
extend its two-field schema or rewrite upstream skill semantics locally.

Track declared lane, configuration, Python conformance, native discovery and
release eligibility as separate results. Completing one cannot imply another.
Use the existing project authority for planning; these are observable results,
not a replacement backlog system.

Allow read-only inspection and bounded configuration while lane or migration is
pending. Require an explicit lane before completing adoption. For both lanes,
strict completion requires all applicable baseline evidence and required native
capabilities. Lane changes require an inspected diff and repeat acceptance of
affected requirements. Do not silently infer a lane from installed plugins.

0.5 binding: upstream lite omits heavy management tooling; starter-mandated
SemVer/PRD/analysis evidence still applies in both lanes. Preserve current SP +
gz-skills activation in both lanes without silently promoting lite or requiring
heavy backlog tooling there. The runbook makes this distinction explicit.

Confirmed: retain the intended upstream heavy composition, including Backplane.
Backplane is under development; preserve that intended design and expose its
observed readiness separately. Selecting heavy does not certify component
readiness. Existing project authorities support work while Backplane remains
deferred; they do not redefine the intended stack. No Backplane activation
follows from this proposal.

## Existing and underway projects

1. Inventory original starter release/SHA, declared lane, local edits, supported
   products/platforms, dependency intent, current configuration, and existing
   project/release authorities. Capture rollback and dirty-state boundaries.
2. Compare the original published baseline, target published baseline and current
   project files. Generate a reviewed reconciliation plan and exact diff;
   unknown provenance or edited managed files require explicit resolution.
3. Select a lane and assign each missing requirement a bounded migration task
   with owner and verification. Preserve public behavior and operational data.
   Existing architecture is not an automatic waiver of required conformance.
4. Apply authorized slices: packaging/imports, metadata/dependencies, effective
   tools/config, hooks/CI, artifacts and applicable host/workspace/deployment
   checks. Preserve unrelated edits; recheck preimages before writes and retain
   rollback. Never force-overwrite conflicts or silently change native caches.
5. Reconcile generated instructions and provenance together. Retain old and target
   policy identities and actual acceptance evidence. Report migration pending
   until the required checks pass; partial work must remain usable and visible.
6. Re-run affected acceptance after changes to policy, source, lock, configuration,
   tool/runtime, deployment or supported platform scope. A receipt for a different
   input population cannot authorize the current release.

Already released adopter products do not need their history rewritten or a
retroactive 1.0 PRD. Require a new PRD for the next major, and reconcile current
minor/patch release practice prospectively. The open exception-release decision
must determine how an underway project can ship during an incomplete migration.

## Release design for starter and adopters

One shared release contract applies in both lanes, with independent app,
template and plugin identities:

- Every major, including 1.0.0, has a newly written, explicitly accepted PRD
  naming that major's scope, requirements, exclusions and measurable acceptance.
  Link it to the selected change bundle and evidence; file presence alone is
  insufficient. A prior major's PRD is not reusable for this requirement.
- Minors select coherent related changes in the existing backlog; patches are
  compatible fixes/clarifications. Preserve the documented 0.x classification
  rule and stable-version compatibility guarantees. No unpublished candidate
  retroactively changes a published release.
- Advance development identity when the public adoption contract changes; do
  not continue identifying stronger policy as the preceding released version.
  Report development/candidate versus published explicitly. Numeric next-version
  metadata can be retained; adding prerelease syntax would need a separate
  manifest/Python-version mapping decision.
- Ordinary adoption uses a verified published tag/full commit with matching
  manifest and packaged policy inputs. Development testing is explicit and
  cannot claim published adoption or satisfy stable-release provenance.
- Release preparation validates version/classification, lane, required PRD,
  selected bundle, changelog/adopter impact, migration instructions, source-
  independent artifacts and required evidence for the exact candidate inputs.
  Changed inputs invalidate affected evidence. Define a precise hash scope to
  avoid self-referential receipts and unnecessary invalidation by unrelated text.
- Separate prepare/check from publish. A release check fails on required missing,
  unknown, failed or stale results. Publishing uses the checked committed
  candidate, verifies remote checks and the immutable tag, and reports the
  distribution identity. User authorization governs publication; commit/push
  never substitutes for it. A blocked publication remains an explicit delivery
  gap, not a completed adopter update.
- Release completion includes an adopter-facing policy delta and migration path.
  Adopter reconciliation records the actual adopted target; publishing the
  starter cannot silently update another project.

These are starter-specific binding/provenance checks. Generic dependency
maintenance and release execution should compose the upstream workflows;
generic engineering remains upstream-owned. Version 0.6's sole
owned skill is the canonical template-update entry; it does not vendor upstream logic.

## Other opinionated choices to settle

| Current choice | Existing authority | Design question |
| --- | --- | --- |
| Python 3.14.x; host-bound 3.12.x exception | baseline-policy; Python engineering | Retain these families and separate host scope? How do exception adopters release? |
| Latest verified stable within selected families; exact pins afterward | baseline-policy | Establish currently missing tool families and evidence freshness/invalidation rules. |
| uv-managed runtime, src packaging, uv_build for pure Python, centralized tool config | Astral alignment | Keep mandatory in both lanes; enumerate genuine native/namespace/coordinator variants. |
| Ruff check/format, ty, unittest; never pytest | Python engineering | Retain this strong tool choice for all adopters? |
| Exactly four routine pre-commit checks; deeper tools formerly on demand only | Python engineering | Confirmed: require deeper analysis at adoption/release acceptance; retain the ordinary four-hook routine. Design separate execution/integration. |
| C901 20, cognitive 15, Lizard 20/20/20; non-growing legacy debt | complexity/counting contracts | Decide whether over-limit legacy debt blocks strict adoption/releases or only regressions. |
| Required on-demand analyzer assortment, including cohesion and Cosmic Ray | Python engineering | Resolve installation/compatibility gaps; distinguish required capability from a required clean result. |
| Stdlib first, sqlite3 for SQLite, Pydantic allowed | Python engineering | Confirm package approval/justification boundaries rather than silently prohibiting product needs. |
| Hexagonal domain/adapter boundaries; TDD/BDD/DDD for consequential behavior | Python engineering | Clarify applicability in small lite projects, libraries and simple scripts. |
| Review current Python idioms and advances, with documented adopt/defer decisions | baseline-policy; 3.14 opportunity guide | Define bounded evidence so current syntax alone cannot be mistaken for completion. |
| SP feature work, gz-skills engineering/maintenance; Backplane deferred | architecture; adoption | Confirmed: retain intended heavy composition including Backplane; expose current readiness separately. Lite activation mapping remains to settle. |
| One native template-update skill; other skills upstream/project-owned; no vendoring or gzkit adoption | structure; architecture | Version 0.6 is the narrow user-directed exception to the previous zero-skills rule. |
| Conflict preservation; no forced upgrades or automatic app refactor | helper; configuration | Add a supported reviewed reconciliation path rather than treating refusal as migration support. |
| Independent versions, immutable full-SHA pins, no automatic publication | versioning | Enforce release identity and delivery status in normal adoption paths. |
| Quarterly on-demand freshness; no automatic schedule | baseline-policy | Decide whether freshness must be current at every release or only affected maintenance scope. |

## Proposed implementation and proof

Apply the confirmed decisions above; settle remaining lite activation and
exception-release semantics before finalizing their implementation:

1. Reconcile the policy/instruction authorities around one versioned requirement
   catalog and lane mapping; preserve historical receipts. Include source-section
   inventory and review triggers for updated Astral guidance.
2. Design a minimal versioned starter adoption/evidence record outside upstream
   settings. Validate requirement IDs, applicability, input identity, results and
   evidence references. Automated checks verify observable facts; attributed
   human review remains explicit for architecture, PRD adequacy and other semantic
   decisions. A self-reported PASS string is not execution proof.
3. Add bounded helper support for mandatory lane completion, explicit development
   provenance, published-release verification, read-only reconciliation planning,
   and adoption/release eligibility. Specify compatibility and schema migration
   before implementing writes; reuse existing conflict/rollback protections.
4. Implement release preparation checks and project-owned integration examples
   for both lanes. Resolve the desired CI boundary explicitly instead of adding
   deeper analyzers to routine hooks through implication.
5. Verify public behavior with unittest: missing/null lane, stale/failed evidence,
   edited managed files, unknown provenance, unpublished/mismatched revisions,
   changed inputs, missing/reused major PRD, real conflicts/rollback, both lanes,
   and genuine N/A cases. Execute flat-app, typed-library and workspace migrations
   plus a deliberately nonconforming underway project and negative controls.
6. Run the repository's required checks and source-independent/installed proof;
   record actual platform scope. Prepare the coherent next minor release with
   adopter delta and migration instructions. Complete authorized publication and
   remote identity verification; reconcile a real adopter only in its authorized
   project scope.

Done means tested conformance behavior, honest blocking states, an actionable
existing-project migration and a delivered release identity. Writing stricter
prose or passing the existing configuration-only tests is insufficient.

## Discussion-save verification

October 24, macOS arm64, managed Python 3.14.8 and isolated uv 0.13.1:
regenerated adopter resources, locked all-group sync, bundle/both-catalog
validation, sdist-to-wheel build and isolated installed CLI checks passed.
Ruff check/format, ty and all 35 adoption tests passed with a canonical
`TMPDIR` under `/private/tmp`. With the default macOS temporary path, six
subtest failures expose fixture comparisons between unresolved `/var` paths
and resolved `/private/var` paths (rollback injection and source provenance).
That test portability defect remains open; no fixture or helper code was
changed in this documentation clarification. The broader enforcement design
above remains unimplemented and unreleased.

Subsequent 0.5 preparation resolves the temporary-path fixture defect and
delivers the confirmed policy/runbook. The
[release receipt](../evidence/2026-10-24-0.5.0-release.md) supersedes the earlier
save-point limits for those checks; the proposed automatic enforcement remains
unimplemented.
