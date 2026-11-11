# Dependabot coverage

## Current product compatibility correction — November 11, 2026

This product has root uv and GitHub Actions jobs only; the X-Plane/helper
descriptions below remain inherited starter context. Its November 9
[uv scan failed](https://github.com/tvproductions/gz-mcp-lsp/actions/runs/42641967556)
because updater uv 0.13.7 could not satisfy exact required-version ==0.13.6.
The project now accepts >=0.13.6 under the adopted starter v0.9.0 policy;
CI tests 0.13.7. Package/backend pins remain independent. See the
[compatibility receipt](../evidence/2026-11-11-uv-compatibility.md).
Fresh hosted scanning on the corrected default branch must be observed separately;
local compatibility checks alone do not prove a hosted repair.

## Historical starter coverage

The repository's `.github/dependabot.yml` proposes updates weekly on Mondays
at 09:00 America/Chicago. It has three independent jobs:

| Job | Inputs | Scope |
| --- | --- | --- |
| Standard Python | Root `pyproject.toml` and `uv.lock` | Declared package requirements and resolved transitive packages for Python 3.14 |
| X-Plane/XPPython3 | `baselines/xplane/pyproject.toml` and its own `uv.lock` | Standalone tool requirements and transitive packages for Python 3.12 |
| GitHub Actions | `.github/workflows/` | Action references, including tagged full-SHA pins and their version comments |

Each job permits up to five open version-update PRs. Package jobs include direct
and transitive dependencies, excluding each local project's own version, which
is not an upstream package to upgrade. GitHub's default three-day version-update
cooldown remains in effect; a newly published release may not immediately yield
a PR. Major tool updates are proposed for review rather
than silently excluded; Python support remains constrained by each project's
metadata. There is no automerge configuration. A PR must pass applicable checks
and maintainer compatibility review; a resolver result alone is insufficient.

The existing four routine hooks remain unchanged. A separate CI job synchronizes
the independent X-Plane environment and runs bounded positive/negative Ruff, ty
and unittest probes. It does not run deeper hygiene analysis. The dependency-only
reference ships no runtime package, so source layout, entry points and an installed
artifact are inapplicable to that project. An adopter's real package still needs
the full Astral acceptance proof and host-specific testing.

## Limits and review work

| Surface | Dependabot coverage | Remaining responsibility |
| --- | --- | --- |
| `uv_build` | Package requirement in the root build-system and X-Plane dev group | Verify the root build-only update path in an actual bot PR; reconcile any affected execution references |
| Python `.python-version` and CI Python inputs | No configured updater | Check latest patches within each approved family; synchronize exact selections and test them |
| `[tool.uv].required-version` and CI uv inputs | No configured updater | Maintain the uv compatibility minimum separately from CI's tested version; do not add a fake runtime dependency to make them visible |
| Local pre-commit hooks | Tool packages are scanned through their uv groups | Preserve the four commands; there are no external hook repos to update |
| SP, gz-skills, deferred SP-BP, both native catalogs | Outside these ecosystems | Use the existing stack-maintenance workflow and reconcile full SHAs, catalogs and generated resources |
| Required deeper tools absent from manifests | Not discoverable as package dependencies | Finish the existing adoption/release-analysis work; absence of PRs cannot establish completeness |
| XPPython3/X-Plane installation and embedded Python | Outside package scanning | Inspect actual host runtime and test plugin behavior separately |

The November 7 [diagnosis and resolution](https://github.com/tvproductions/gz-skills-first-starter/blob/3f76acf0038b030bf5abd85ce4a419e890d3e420/docs/evidence/2026-11-07-dependabot-uv-compatibility.md)
supersedes the initial scan observations: both November 2 uv jobs failed because
their preinstalled uv 0.13.5 could not satisfy the former exact 0.13.6
requirement. The Actions scan succeeded. Reviewed upstream source selects
0.13.7, which also failed that former requirement in local read-only controls;
source state does not establish the deployed hosted image. Hosted configuration
offers no documented uv-version override. Successful initial scans do not prove
current reliability, update-PR generation or lock changes.

The maintainer subsequently authorized minimum-only uv compatibility. Both
baselines now accept `>=0.13.5` without an upper bound; CI remains on tested
0.13.6. This removes the demonstrated version-only rejection without replacing
Dependabot or changing package locks. Keep executable provenance, locked execution
and separate Python families. Newer uv admission does not prove every future
release compatible; investigate actual behavioral failures on their merits.
Fresh scans on `e918dbb` now pass for both Python projects and Actions. Both
Python logs report actual uv 0.13.7, and ten real PRs show the expected manifest/
lock updates with green CI. Their scopes were inspected; no upgrade was merged.
The receipt records exact PR heads, CI links and remaining compatibility review.
The root build-only uv_build PR path remains unverified. See the
[uv compatibility policy](../baseline-policy.md#uv-executable-compatibility).

An update to root `uv_build` may need an additional X-Plane PR, and vice versa.
Review each against its own environment; they are not one shared resolution.
If maintained files change, regenerate wheel resources through
`tools/package_resources.py` and keep dated candidate-specific evidence. The
bot cannot write a compatibility receipt or prove native skill discovery.

## Activation and evidence

The configuration takes effect when merged into the default branch, subject to
repository/organization Dependabot settings. This local change does not push or
enable a remote service through an API. After merge, inspect GitHub's dependency
update logs for both uv jobs and the Actions job. Verify their manifest paths,
actual updater versions, preserved runtime constraints, generated locks and CI
results on a real update PR. The initial hosted scans completed successfully;
the later uv failures and November 7 recovery above supersede that observation
for current reliability. Actual PR generation and CI are now observed; merging
still requires applicable compatibility checks.

Historically, the first Linux CI attempt could not provision 3.12.16 because uv
0.13.5's embedded download list predated that patch. The X-Plane project used an
official Astral download manifest pinned at commit
`68677f5439c027db17b4db7821882a9881d376f6`, including checksums. Release 0.8.0
adopted uv 0.13.6 and removed that override after provisioning succeeded with
its embedded metadata. See the [release receipt](https://github.com/tvproductions/gz-skills-first-starter/blob/3f76acf0038b030bf5abd85ce4a419e890d3e420/docs/evidence/2026-10-31-0.8.0-release.md).
Do not restore the historical override to address an unrelated bot version
mismatch. Python and uv execution pins still need separate manual review.

The [October 26 receipt](../evidence/2026-10-26-dependabot.md) records the initial
inputs, official sources, local checks and remaining UNKNOWNs. This receipt is
not a release-wide freshness certification. Adopters choose starter updates,
direct upstream updates or both, and their own timing; copying this scaffold
does not require retaining its Dependabot configuration.

Official references: [Dependabot options](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference),
[ecosystem and SHA support](https://docs.github.com/en/code-security/reference/supply-chain-security/supported-ecosystems-and-repositories),
[uv updater Dockerfile](https://github.com/dependabot/dependabot-core/blob/main/uv/Dockerfile),
[build-only dependency update path](https://github.com/dependabot/dependabot-core/blob/main/uv/lib/dependabot/uv/file_updater/lock_file_updater.rb),
and [uv dependency-only project configuration](https://docs.astral.sh/uv/concepts/projects/config/#project-packaging).
