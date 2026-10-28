# gz-mcp-lsp

Read README.md, AGENTS.skills-first.md and the current initialization evidence at
`docs/evidence/2026-10-28-initialization.md` before work. The adopted starter
engineering policies in `docs/engineering/`, `docs/baseline-policy.md` and
`docs/versioning.md` remain authoritative. Historical starter implementation
instructions do not make its helper part of this product.

## Current boundary

Initialization and design discovery only. Do not implement MCP/LSP runtime,
semantic operations, a settings loader or a server entry point until human
review approves the design. The candidate proposal is
`docs/superpowers/specs/2026-10-28-semantic-navigation-design.md`.
Do not infer approval from scaffolding, documentation, CI or this file.

Use adopted Superpowers for feature design and gz-skills gzs-router for portable
engineering selection. The user explicitly selected lite through gzs-project-setup.
Keep Backplane disabled; preserve native manager caches and unrelated defaults.
Use the project update-gz-template skill for starter maintenance. No gzkit lifecycle.
Project issues/PRs and review documents are the current planning authority.

## Product constraints

Independent Python implementation using the official MCP Python SDK at its
MCP boundary. One workspace, one ty process, stdio only. Read-only semantic
navigation; no edit/refactor/code action/execute command/diagnostics tools,
request-time installation, network service or orchestration framework.
Prefer URI and explicit position inputs. Never infer an identifier position from
a symbol's full range start. Preserve selection ranges separately.
No private source or project data in this public repository.

## Engineering and configuration

Python 3.14 family; exact verified managed patch 3.14.10 in `.python-version` and CI.
uv 0.13.6, project-owned lock, src packaging and uv_build. Centralize Python/tool
metadata in pyproject.toml. Application settings will be project-owned JSON;
**no environment-variable-based application configuration**. This explicit product
rule overrides inherited suggestions for environment overrides. Native host config
retains its own format. No Makefile. unittest only, never pytest.

Preserve routine Ruff selection E4/E7/E9/F/I/UP/B/SIM/RUF and ceilings: C901 20,
qualified cognitive 15, Lizard function/module/overall 20. C901 and deeper checks
remain outside routine hooks/CI. Cognitive qualification is unresolved upstream;
complexipy is a defect reproducer, never passing cognitive authority.
Freshness, configuration, native discovery, Python acceptance and product
capability acceptance are separate conclusions. Missing evidence stays UNKNOWN.
Required missing/failed/stale results block strict adoption/release acceptance.
Do not replace policies with copied upstream profile defaults.

## Gate

```bash
uv sync --locked --all-groups
uv run --locked pre-commit run --all-files
uv build --no-sources
uv run --locked python tools/verify_distribution.py
```

The four hooks are Ruff check, Ruff format, ty and unittest. The unittest hook
runs tests/ (distribution guards); semantic tests are absent until implementation.
Inherited utility tests remain outside routine CI and run explicitly:
`uv run --locked --group hygiene python -m unittest discover -s tools/engineering -p 'test_*.py' -v`.
Verify relevant effective configuration, interpreter/tool provenance and artifacts
outside the checkout. Use the separate published starter checkout for helper
validation/configuration/status, with its own uv 0.13.5; never relabel product HEAD
as a starter revision. Product runtime has no starter dependency.

Every major including 1.0.0 requires a new PRD. Use SemVer for the eventual
CLI, configuration, schemas and behavior. No tag/release publication without
explicit authorization. Initialization is not release acceptance.

## Git synchronization

Follow the starter's preserved Git synchronization ritual in
`docs/STARTER-AGENTS.md#git-synchronization-ritual`: inspect/fetch and review the
complete diff, run the gate with matching uv in nested hooks, commit without
bypass, push without force, observe exact-commit CI, and verify local/remote SHA
alignment. Report remaining gaps independently of Git sync. Keep changelog and
initialization evidence current. Do not manufacture CI receipt-only commit chains.
