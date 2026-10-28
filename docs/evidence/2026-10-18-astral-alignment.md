# Astral alignment migration — October 18, 2026

Scope: the user required maximal Astral alignment, necessary adopter refactoring
and remediation of this starter's own conformance gaps, then clarified the
Cargo-style workspace model. This is an unpublished 0.4.0 development candidate
under the existing minor-version rule for changed baseline obligations. The
unpublished 0.3.1/0.3.2 changes remain included; published tags stay untouched.

## Policy and implementation

The [alignment contract](../engineering/astral-alignment.md) binds new and
existing Python adopters to `src/` packages, declared builds, centralized Python
configuration, uv-managed locked execution and installed-artifact verification.
Existing layout is not an exemption: full adoption requires refactoring or an
evidenced compatibility exception with an owner and revisit condition. Existing
governance, public behavior, data and rollback evidence must survive migration.
Configuration-only helper requests still preserve project files and report gaps.

The helper now lives in `src/skills_first_starter/cli.py`; tests import that
installed package. `starter.py` is a six-line compatibility launcher for existing
documented commands. uv_build builds wheel/sdist and an installed
`skills-first-starter` console entry point. Four generated resource copies carry
the authoritative root bundle, native catalogs and instructions into wheels;
unittest verifies equality and `tools/package_resources.py` regenerates them.
Editable installs use checkout authorities. Wheels need explicit published SHA
provenance for configure and cannot infer it from an environment or adopter repo.
No upstream skills are packaged or copied.

The starter has one package. A workspace would add no useful package boundary,
so it remains a standard uv project. Adopter guidance includes shared locks and
environments, explicit member dependency/source declarations, editable linking,
member selection and incompatible-runtime/environment exceptions. A shared
resolution detects conflicts; it does not remove incompatible requirements or
prove that each member declares every imported dependency.

## Tool inventory and decisions

Registry metadata was checked directly on PyPI; Python's official release API
was checked for the newest published 3.14 patch. Exact resolutions were generated
by uv, including all development/hygiene groups. No generated lock was hand-edited.

| Surface | Before | Selected | Family / decision |
| --- | --- | --- | --- |
| Python | 3.14.8 | 3.14.8 | Newest published 3.14.x patch; actual managed interpreter verified |
| uv | Unpinned project requirement; installed 0.13.1 | 0.13.1 | Select 0.13.x; exact required-version and CI pin |
| uv_build | Absent | 0.13.1 | Select 0.13.x; exact build requirement, no runtime dependency |
| Ruff | 0.15.18 | 0.15.22 | Newest 0.15.x patch; upstream 0.17.1 is a separate family, deferred |
| ty | Absent | 0.0.89 | Required 0.0.x beta exception; no stable release available |
| pre-commit | Absent | 4.7.0 | Select 4.x; current registry release |
| complexipy | 8.0.1 | 8.0.1 | Select 8.x; retained current registry release |
| Lizard | 1.24.1 | 1.24.1 | Select 1.24.x; retained current registry release |
| actions/checkout | Moving v4 reference | v7.0.1, `3d3c42e5aac5ba805825da76410c181273ba90b1` | Adopt Astral's current documented immutable CI selection |
| astral-sh/setup-uv | Moving v6 reference | v9.0.0, `c771a70e6277c0a99b617c7a806ffedaca235ff9` | Adopt current documented action with explicit uv/Python versions; cache disabled |

The starter maintainer owns the ty beta exception. Revisit at stable release or
the next scoped maintenance; an exact pin does not imply a stable API. The
setup-uv release changes cache-pruning behavior; disabling cache makes that
irrelevant here. Action inputs were reviewed against their immutable manifests;
actual GitHub-hosted execution remains unobserved on this candidate.

SP 7.0.0, deferred Backplane and gz-skills 0.8.0 remain at their existing SHAs.
Plugin updates/installation, other repositories and global tool updates are
outside this implementation scope. No profile was selected or initialized; the
project setup inspection found no settings. Other on-demand analyzer proofs and
shared/local utility ownership remain separate roadmap work.

Sources: [Python release API](https://www.python.org/api/v2/downloads/release/?limit=100),
[uv](https://pypi.org/pypi/uv/json), [uv_build](https://pypi.org/pypi/uv_build/json),
[Ruff](https://pypi.org/pypi/ruff/json), [ty](https://pypi.org/pypi/ty/json),
[pre-commit](https://pypi.org/pypi/pre-commit/json),
[Astral CI guidance](https://docs.astral.sh/uv/guides/integration/github/),
[setup-uv release](https://github.com/astral-sh/setup-uv/releases/tag/v9.0.0),
[checkout release](https://github.com/actions/checkout/releases/tag/v7.0.1).
`uv pip list --outdated --format json` reported only Ruff 0.17.1 beyond the
selected family; it did not update packages.

## Verification and limits

Observed locally on Windows with managed Python 3.14.8:

- 31 routine unittest tests, including wheel-resource drift detection; bundle
  and both native catalog validation; Ruff 0.15.22 check/format and ty checks.
- All four approved local pre-commit hooks pass and are installed in this
  checkout. CI uses the same locked routine commands, plus artifact verification.
- uv lock consistency; wheel built from sdist; isolated wheel installation
  outside the checkout; installed validate/version/preview/apply/status,
  idempotence and refusal to infer missing Git provenance.
- Eleven explicit analyzer tests: ten lizard-functions-v1 CLI cases and a
  legacy-locale regression for the compatibility probe. The probe initially
  failed on Unicode test source under Windows cp1252, then passed using Python
  source-encoding detection. Its fixtures and receipt use explicit UTF-8.
- Cross-platform skill's static line-ending and subprocess-error checks:
  zero findings. Add `.gitattributes` LF normalization and explicit subprocess
  decoding. No macOS/Linux execution is claimed from these local results.
- Ruff/complexipy/Lizard compatibility probe passes with the refreshed Ruff
  patch. Existing CLI complexity violations remain visible. New packaging
  utilities score cognitive 9 and 12, below 15; no thresholds were waived.
- On-demand `uv audit --locked --output-format json`: 17 third-party packages,
  zero reported vulnerabilities/adverse statuses. uv labels this command/schema
  experimental; this is supplementary evidence and does not replace the selected
  pip-audit policy or become a hook/CI gate.

Python 3.14 assessment: the migration benefits from explicit runtime/type targets
and modern generic syntax already supported by the selected family. It needs no
new concurrency, template-string, compression or annotation-introspection APIs;
defer them without a product need. Retain existing postponed annotations to
preserve behavior; use Python's source-encoding detection for source inspection.
Packaging adds no runtime dependency. Native skill discovery, Backplane readiness,
remote CI, and other deeper-tool compatibility remain separate proofs.
