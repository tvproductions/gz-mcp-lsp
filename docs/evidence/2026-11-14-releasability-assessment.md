# Pre-1.0 releasability assessment — 2026-11-14

## User direction and authority

Evaluation followed native acceptance/synchronization at product commit
`a0a0e5184558031fe6911b0e3e8d42ef326616f9`. The user requested discussion of
PyPI, GitHub releases, github.io docs, Read the Docs and repository readiness
for actual consumption. This is explicitly **not 1.0**. The version should
advance to **at least 0.2.0**; package/lock metadata still says **0.1.0**.
No version bump or publication was performed in this review.

The user directed leaving cognitive qualification open as a known gap. That
must not stop independent readiness work. Qualified cognitive stays UNKNOWN,
ceiling 15 remains, and strict G5/E3/E4 must not be relabeled PASS. The engine
extraction and shared policy belong upstream. The user reported that
**gz-skills-first-starter is already handling the versioning correction**;
do not repeat that work or change the adopted starter/plugins/caches here.

The user expects a version decision and appropriate increment at completed
backlog boundaries, separately from tagging/publication. Do not use an
unpublished bundle to freeze all subsequent items at 0.1.0 or 0.2.0. Preserve
actual Git history; no fictional historical releases or 1.0 PRD are needed.
Reconcile eventual released starter policy through its proper workflow without
relabeling current recorded provenance.

The user subsequently requested this handoff and Git sync. This authorizes the
documentation save point, not service-account/project creation, implementation
of proposed publication infrastructure, a tag or external publication.

## Observed readiness

| Surface | Observed result | Remaining work |
| --- | --- | --- |
| Runtime | Nine tools, installed MCP/ty and actual Codex proof | Maintain explicit support/compatibility claims |
| Verification | Base commit above has passing three-platform CI; 189 tests per lane, POSIX skips 1, Windows skips 26 | Eventual candidate and registry-installed functional checks |
| Packaging | Source-independent wheel/sdist and installed checks pass; clean product wheel, MIT notices, typing marker | Public URLs/metadata, PyPI description and consumer setup guidance |
| PyPI | Public gz-mcp-lsp JSON lookup returned HTTP 404 | Establish ownership/name eligibility and publishing configuration; 404 does not reserve or guarantee a name |
| GitHub releases | No product tags/published releases found | Release workflow, immutable version tag, notes, wheel/sdist and checksums |
| GitHub Pages | has_pages=false; Pages API returned 404 | Docs build, Pages configuration and deployment workflow |
| Read the Docs | No repository configuration; public project lookup returned 404 | Establish project/integration and versioned build; account state unverified |
| Delivery controls | No deployment environments returned; only product-check/Dependabot workflows | Configure intended deployment environments and review protections; conventional branch protection returned 404, rulesets not assessed |

These are bounded observations, not proof of registry name availability or
service-account/credential access. No credentials were requested or inspected.
No external writes were made during evaluation.

The inspected 0.1.0 wheel had 28 entries under only product/metadata roots.
The inspected sdist had 291 entries, including historical starter handoffs and
native engineering plugin configuration. Review inclusion rules deliberately,
preserving notices and source-build/meaningful-test requirements. Counts apply
to those inspected artifacts, not later rebuilds containing this handoff.

GitHub's read-only description and the package's awaiting-design-approval
introductory docstring are stale. The CLI lacks a standalone --version option.
Package metadata lacks Project-URL entries, classifiers, keywords and
maintainer/author fields. Some are optional metadata: their absence identifies
usability work, not proof that PyPI would reject the wheel.

## Consumer installation and compatibility

The adapter declares official mcp==2.3.0 as its only runtime dependency. Ty is
selected in the development group and passed as an absolute, preinstalled
executable. Installing the adapter alone does not provision ty. Design/test a
clean setup path through adapter installation, compatible ty provisioning,
JSON settings, Codex registration and a meaningful first query. Preserve no
request-time installation, no application environment overrides, default-disabled
mutations, explicit writable roots and native host approval.

Registry consumers do not automatically use the development uv.lock graph.
Verify locked development acceptance and fresh consumer resolution separately.
After authorized publication, install the actual registry distribution outside
the checkout and prove functional Codex behavior. An upload/import-only check
does not establish that behavior.

Retain Python >=3.14,<3.15 unless deliberately changed with evidence. Document
Linux x86_64/macOS arm64 writes and Windows AMD64 reads/unsupported-write denial;
a pure-Python wheel alone does not certify other platform combinations.

## Recommendations, not an approved implementation design

1. Reconcile product/version/readiness authorities and the bounded capability
   review. T13 is a final evidence/report task, not another runtime feature or
   publication permission. Retain the cognitive gap explicitly.
2. Improve metadata, README, distribution contents and installation flow;
   implement at least 0.2.0 and version subsequent completed items appropriately.
3. Build one maintained user-docs source: installation, quickstart, Codex
   registration, nine tool contracts, configuration, mutation safety/recovery,
   supported platforms and troubleshooting. Preserve historical evidence without
   making it the new user's entry point.
4. Prepare GitHub release and PyPI workflows publishing the exact validated
   artifacts through Trusted Publishing, immutable identity and checksums.
   Rehearse before publication and verify each channel separately.
5. Configure/verify the chosen Pages/RTD arrangement, then complete candidate
   and actual published-consumer checks under explicit publication authority.

Two docs arrangements were discussed: the full manual on both hosts, or Pages
as the project/quickstart site with RTD as the canonical versioned manual.
The agent recommended the latter; **the user has not chosen**. Share maintained
content/build inputs rather than independently edited manuals. A Markdown-based
generator such as MkDocs was considered, not selected/installed. Theme, exact
docs pins and deployment design remain open.

Resume Superpowers brainstorming at the docs-hosting choice, then prepare a
bounded design/backlog. Existing runtime approval does not itself approve the
new publication implementation. Do not resume by polling the unchanged cognitive
issue or repeating completed native/deeper measurements. Any eventual release
with the gap retained must disclose it without claiming strict conformance.

## Official references consulted

- [PyPA publishing guidance](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/): Trusted Publishing and separate build/publication jobs.
- [PyPI pending publishers](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/): new project creation through Trusted Publishing.
- [PyPI README guidance](https://packaging.python.org/en/latest/guides/making-a-pypi-friendly-readme/): registry-facing description.
- [GitHub Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages): static build/deployment and permissions/environment.
- [RTD configuration](https://docs.readthedocs.com/platform/stable/config-file/v2.html): repository configuration, Sphinx/MkDocs and uv support.
- [RTD versions](https://docs.readthedocs.com/platform/stable/versions.html) and [canonical URLs](https://docs.readthedocs.com/platform/stable/canonical-urls.html): version and host behavior.

This assessment changes no package metadata, runtime, docs generator, publishing
workflow or service integration. The handoff synchronization response records
the exact evidence commit, gate, hosted CI and local/remote alignment.
