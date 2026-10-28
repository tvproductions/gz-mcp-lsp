# Starter Astral acceptance record — October 18, 2026

Scope: the working tree based on commit
`1c107649154b9e62f87be6416f929b8c76234151`, including the user's authorized
Astral guidance implementation. Template metadata remains 0.4.1; this work is
unreleased. It strengthens guidance/acceptance obligations for a future bundled
minor under the existing version policy; it refreshes no dependency/runtime pin.

This is a single packaged pure-Python CLI: distribution `skills-first-starter`,
import `skills_first_starter`, command `skills-first-starter`. There is no
workspace, private index, external runtime dependency, native extension or
deployment image. The source/lock/configuration rollback authority is Git;
preserve unrelated changes and operational data when restoring a prior revision.

## Results against A01–A18

| ID | Result and scope | Evidence / outstanding work |
| --- | --- | --- |
| A01 | PASS for this bounded documentation/adopter-fragment unit | Plan audit and source mapping; helper, runtime pins, hooks and CI contract unchanged |
| A02 | PASS for helper packaging/import/CLI behavior | `src/skills_first_starter`, declared script; isolated installed verifier exercises validate/version/configure/status, preservation/idempotence/provenance refusal |
| A03 | PASS for selected backend | uv_build==0.13.1, pure Python; source-independent build and artifact verifier |
| A04 | PASS for inspected Windows context | Effective-configuration JSON: only root pyproject among repository Python configs; no discovered user/system uv, user Ruff/ty configs at inspected Windows locations; no relevant environment controls; representative Ruff settings and actual ty context |
| A05 | PASS for local execution selection | Managed CPython 3.14.8, x86_64; actual interpreter/base prefix and tool executables recorded; Ruff py314/ty 3.14/CI 3.14.8 declarations aligned |
| A06 | Historical selection retained; current freshness UNKNOWN | Existing dated runtime/tool selection receipts remain authoritative for their checked dates. This documentation change performs no freshness inventory or upgrade; a new adoption/maintenance event must recheck within approved families |
| A07 | PASS for selected current project environment | Locked all-group exact sync and lock consistency; no conflicting groups in this manifest |
| A08 | PASS for routine checks and provenance | Ruff 0.15.22, ty 0.0.89, pre-commit 4.7.0 in project environment; reviewed Ruff families, unittest and final gate record |
| A09 | Local hooks PASS; current candidate remote CI UNKNOWN | Existing hook file inspected and four hooks executed; CI commands inspected. Latest synchronized base CI passed, but these uncommitted edits have no new remote run |
| A10 | PASS for helper declarations; N/A for runtime dependency migration | No runtime dependencies/source overrides added; mirror identity/catalog/resource checks retained |
| A11 | PASS for local distribution path | Plain and source-independent sdist-to-wheel builds, resource/sdist inventory checks and final artifact verification in gate receipt |
| A12 | PASS for local installed helper contract | Fresh outside-checkout wheel environment, installed CLI behavior and resource checks; no source-path shim |
| A13 | N/A for a published typed-library support claim | Helper is a CLI. Separate executed library example verifies `py.typed` plus installed consumer positive/negative controls |
| A14 | N/A for this single-project helper | Separate executed workspace path verifies declared dependency metadata and isolated math/app runtime installations; earlier negative control retains shared-environment failure evidence |
| A15 | N/A | Public index execution baseline; no private/specialized source adoption or credentials requested |
| A16 | N/A for native/deployed product; ordinary build PASS | No compiler/host/container target. Keep isolated pure-Python backend and exact backend pin |
| A17 | N/A for independent script/tool/export delivery | Engineering utilities run under the project; no PEP 723 metadata, user-tool substitution or secondary requirements authority introduced |
| A18 | Existing wider gaps remain UNKNOWN / owned exception | Required ty beta exception remains starter-maintainer-owned with stable-release/next-maintenance revisit. Remaining deeper-tool compatibility/utility ownership and other host/platform proofs stay in roadmap/handoffs |

The bounded implementation and local packaging/routine contract are verified.
This is **not an unqualified claim that all Python engineering, freshness,
deeper-tool or native-host acceptance is complete**. Required UNKNOWN rows must
be resolved at their applicable adoption/maintenance/CI milestone before making
that broader claim. No private-source/native deployment evidence is implied.

## Evidence and verification authority

- [Effective configuration and provenance](2026-10-18-astral-effective-configuration.json).
- [Executed migration paths](2026-10-18-astral-migrations.json): 64 command records,
  including the expected failing installed typing negative control.
- [Migration artifact supplement](2026-10-18-astral-migration-artifacts.json): four
  source-independent builds, eight inventories, wheel hashes matching the
  installed-behavior receipt.
- [Final local command results](2026-10-18-astral-acceptance-checks.json) own the
  observed exit statuses for regeneration, required checks and source-independent
  build. No remote CI or release claim follows from those local results.
- Earlier [uv execution](2026-10-18-uv-behavior-probe.json) and
  [workspace negative controls](2026-10-18-uv-projects-probe.json) remain historical.

Only invented temporary examples were modified. Their fresh lock/sync and pinned
consumer-tool installation used network access when cache metadata was absent;
runtime verification/builds used the recorded pins and cached inputs. The
temporary examples' locks and fixture contents are retained in the receipt.
No adopter environment or upstream plugin was changed.

Python 3.14 opportunity assessment: use the actual pinned interpreter and
stdlib resources/metadata APIs to prove behavior. No additional runtime feature,
dependency, annotation/concurrency/compression machinery is needed in the helper.
