# Dependabot coverage

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
| `[tool.uv].required-version` and CI uv inputs | No configured updater | Review uv releases and reconcile execution pins separately; do not add a fake runtime dependency to make them visible |
| Local pre-commit hooks | Tool packages are scanned through their uv groups | Preserve the four commands; there are no external hook repos to update |
| SP, gz-skills, deferred SP-BP, both native catalogs | Outside these ecosystems | Use the existing stack-maintenance workflow and reconcile full SHAs, catalogs and generated resources |
| Required deeper tools absent from manifests | Not discoverable as package dependencies | Finish the existing adoption/release-analysis work; absence of PRs cannot establish completeness |
| XPPython3/X-Plane installation and embedded Python | Outside package scanning | Inspect actual host runtime and test plugin behavior separately |

Build-only dependencies are supported by the current upstream uv updater source,
but published GitHub documentation still lists uv 0.11 while this checkout pins
0.13.5. Upstream's current updater Dockerfile already selects 0.13.5. The initial
hosted jobs successfully scanned both uv directories and Actions; actual
update-PR generation and lock changes remain unverified. Preserve required
uv pins and inspect the actual job logs for both directories. Do not weaken
locked execution, downgrade uv or change Python families to conceal a bot failure.

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
that does not establish the unobserved PR/update paths.

The first Linux CI attempt could not provision 3.12.16 because uv 0.13.5's
embedded download list predates that patch. The X-Plane project's centralized uv
configuration therefore pins Astral's official download manifest at full commit
`68677f5439c027db17b4db7821882a9881d376f6`, including archive checksums.
This documented uv setting permits the selected managed interpreter without
changing uv or the Python patch. The maintainer should revisit the manifest pin
at the next Python/uv refresh and remove the override once the selected uv's
embedded metadata supplies the runtime. This pin requires manual review alongside
execution pins; Dependabot does not update it.

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
