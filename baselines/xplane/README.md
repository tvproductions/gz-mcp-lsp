# X-Plane/XPPython3 dependency baseline

This independent uv project records standalone development tools for the
host-bound Python 3.12 case. The standard Python 3.14 reference is the repository's
root project. Each has its own declarations, exact interpreter pin and lock;
neither is a workspace member of the other. Dependabot is configured to scan
both weekly; hosted operation must be verified separately.

This is a dependency-only reference, so `package = false` is intentional: it
ships no runtime package, entry point or simulator plugin. There is no artifact
to build here. `uv_build` is pinned as a development dependency so adopters have
a reviewed packaging-tool selection and Dependabot can propose its updates.
Applications and libraries created by adopters still need `src/` packaging,
their own build-system declaration and installed-artifact verification. Do not
copy the root helper's Python 3.14 package into a host-bound environment.

The centralized uv settings pin an official Astral interpreter download manifest
because uv 0.13.5's embedded list predates Python 3.12.16. This preserves exact
managed-runtime selection on a clean Linux runner; review the manifest alongside
Python/uv pins during maintenance. It does not change the embedded simulator.

From this directory:

```powershell
uv sync --locked --all-groups
uv run --locked python ../../tools/verify_xplane_baseline.py
```

The verifier runs isolated positive and negative Ruff, ty and unittest probes,
checks the actual interpreter, and launches the selected development tools.
CI repeats these bounded standalone checks on Linux. This does not qualify
the deeper analyzers or complete the adopter minimum: the same outstanding
deeper-tool selections/qualification in the Python policy still apply. Complexipy
remains a defect reproducer, including this newer pin; no cognitive qualification
is claimed. No extra routine hooks or deeper-analysis CI gate is introduced.

No application dependencies are prescribed here. Preserve the adopter's actual
requirements. No XPPython3 binary, simulator or host runtime is installed or
updated by this project. The 3.12.16 selection is for standalone development;
the embedded host's actual Python patch, native packages and plugin behavior
remain separately UNKNOWN until inspected and tested there. See the
[Dependabot coverage record](../../docs/engineering/dependabot.md) and its
linked dated evidence for verified scope and remaining limitations.
