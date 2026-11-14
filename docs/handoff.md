# Project handoff — 2026-11-14

## Resume point: pre-1.0 release readiness; cognitive gap stays open

Observed **2026-11-14 22:24 UTC**, clean primary checkout **main**, from
`a0a0e5184558031fe6911b0e3e8d42ef326616f9`, aligned with origin/main before
this handoff. The user requested evaluation of making the working server
consumable through **PyPI, GitHub releases, GitHub Pages and Read the Docs**,
then requested this handoff and Git sync. The final synchronization response
records this save point's commit, gate, hosted CI and alignment; do not create
a CI-receipt-only follow-up commit.

**First action:** read the [releasability assessment](evidence/2026-11-14-releasability-assessment.md)
and resume Superpowers brainstorming at the unresolved docs-hosting choice.
The agent recommended Pages for discovery/quickstart and RTD as the canonical
versioned manual; a full manual on both is the alternative. **The user has not
selected either.** Expected next result: a bounded design and actionable readiness
backlog, separating user decisions from recommendations. This is a design
continuation, not approval to implement/publish or create external projects.

The user explicitly said this is **not 1.0**, the version should advance to
**at least 0.2.0**, and cognitive qualification should stay open. Package/lock
metadata remains **0.1.0**; no bump was applied in this documentation save point.
Version completed backlog items appropriately; do not freeze every future item
in one unpublished bundle. The starter is already handling the shared versioning
correction separately. Preserve its adopted v0.9.0 provenance, independent plugin
selections/caches and disabled Backplane; do not repeat upstream changes here.

**T0–T11 implemented; T12 engineering/native evidence recorded; strict G5/E3/E4
incomplete because qualified cognitive is UNKNOWN; T13 NOT RUN.** The user now
directs independent consumability work with that gap retained. This supersedes
the earlier handoff's stop-all-continuation instruction at the unavailable engine.
Do not poll the unchanged cognitive issue as the first action, substitute
complexipy, weaken ceiling 15, mark G5 PASS or claim strict acceptance. T13 is
the final capability/evidence report, not a runtime feature or release permission.
No tag or public publication is authorized.

## Findings and proposed work

The [assessment](evidence/2026-11-14-releasability-assessment.md) contains source
references, service observations and recommendations. Carry forward:

- No product tags/releases, publishing workflows, docs generator, Pages deployment
  or RTD configuration. Pages is disabled. PyPI/RTD public lookups returned 404;
  names/ownership/accounts remain unverified. No deployment environments returned;
  review release protections rather than assuming they are established.
- Clean product wheel; metadata/URLs/registry-facing README need work. Ty requires
  separate provisioning. Consumer dependency resolution does not follow uv.lock
  automatically; prove a clean install through an actual Codex query.
- Create maintained onboarding/tool/configuration/recovery/support docs. Host
  roles, generator/theme and exact docs dependency pins remain undecided.
- GitHub's read-only description and package awaiting-approval docstring are stale.
  Review sdist historical handoffs/engineering config while retaining notices,
  source-build and meaningful-test requirements. Consider a direct --version CLI.
- Proposed order: authority/version reconciliation; installation/package polish;
  documentation; publication automation; rehearsal and registry-installed proof.
  These are recommendations, not completed or implementation-approved backlog.

## Existing evidence and boundaries

- [Current native receipt](evidence/2026-11-14-native-acceptance.md) and JSON:
  Codex 0.169.0/default gpt-6.1-sol with ty 0.0.104; fresh runtime-only installation
  outside checkout; seven model reads, disabled denials, five mutation calls with
  programmatic approval/denial, exact bytes/fresh semantics and four failure/EOF
  scenarios pass on macOS arm64. User config unchanged; no GUI-click claim.
- [Exact native-evidence base CI](https://github.com/tvproductions/gz-mcp-lsp/actions/runs/43626902632)
  passed a0a0e5184558031fe6911b0e3e8d42ef326616f9 on Linux x86_64, macOS arm64,
  Windows AMD64: 189 tests per lane, POSIX skip 1, Windows skip 26. Windows writes
  remain unsupported. This prior CI does not certify this new handoff commit.
- [November 14 dependencies](evidence/2026-11-14-dependency-update.md): ty 0.0.104,
  Grimp 3.20, 103-entry universal inventory, local gate, 29 utility regressions,
  import-contract controls and zero-known-vulnerability audit at observed inputs.
- [November 13 maintenance](evidence/2026-11-13-dependency-update.md) and
  [November 11 engineering acceptance](evidence/2026-11-11-engineering-acceptance.md)
  preserve deeper measurements, findings, coverage, bounded mutation and acceptance
  traceability. Reuse unchanged-input evidence; do not reissue dated freshness.
- [Shared cognitive issue](https://github.com/tvproductions/gz-skills-first-starter/issues/1)
  was last checked OPEN/unscheduled November 14 with no versioned candidate in
  its integration workflow. Owner: starter maintainer/upstream engine delivery.
  The [consumer contract](engineering/cognitive-integration.md) requires 42
  independent fixtures and actual corpus ceiling 15 when available.

The runtime [specification](superpowers/specs/2026-10-28-semantic-navigation-design.md),
[plan](superpowers/plans/2026-10-28-reference-parity.md),
[acceptance matrix](discovery/acceptance-matrix.md) and
[execution evidence](evidence/2026-11-01-execution.md) retain their existing-behavior
contracts. [ROADMAP.md](../ROADMAP.md) records the newer readiness direction and
current metadata separately from the unimplemented target.

## Environment and verification

Managed CPython **3.14.10**, standalone build **20261110**; uv/uv_build **0.13.8**,
uv minimum **>=0.13.6**; MCP **2.3.0**; Ruff **0.17.5**. Preserve the existing
outside-checkout managed-Python installation root from `.venv/pyvenv.cfg` in
`UV_PYTHON_INSTALL_DIR`; nested hooks must resolve the same supported uv.
That is tool provisioning, not application environment configuration. New clones
provision their own environment; ignored private probes/install paths are not
portable prerequisites.

Required gate: `uv sync --locked --all-groups`, four pre-commit hooks,
`uv build --no-sources`, `uv run --locked python tools/verify_distribution.py`.
Documentation-only sync may reuse checks on unchanged relevant inputs; normal
commit hooks stay enabled. The final synchronization response records fresh checks
and exact-commit CI. Deeper analysis stays outside the four hooks/routine CI.

Continue on main in the primary checkout. Linked implementation/reference-parity
at fc3fb7dfbecd6258c1141d6c300e04c1d8e90fa9 was observed and left untouched.
Use gh for GitHub and git for repository operations. Preserve native caches,
unrelated defaults, one-workspace/one-ty stdio, JSON application configuration,
no request-time installation, explicit operator writes/recovery and POSIX-only
writes. No hosted runtime, second server, generic LSP expansion or incidental
cleanup. Public package/docs hosting is the newly discussed delivery scope.
