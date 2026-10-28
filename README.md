# gz-mcp-lsp

Read-only semantic code navigation for AI coding agents, using existing language
servers through the Model Context Protocol (MCP).

**Status: initialization and design discovery. No adapter runtime or accepted MCP
capabilities exist yet. Human design review precedes implementation.**

The intended path is:

```text
Codex → MCP (stdio) → gz-mcp-lsp → LSP (stdio) → ty server
```

The initial proposal covers one workspace and one Astral ty process. Definition,
references, hover, document symbols, workspace symbols and implementations are
candidates, not shipped features. Canonical semantic queries use document URI and
explicit line/character positions. No editing, refactoring, diagnostics tool,
automatic dependency installation, network service or hosted infrastructure is planned.

Read the [architectural proposal and acceptance matrix](docs/superpowers/specs/2026-10-28-semantic-navigation-design.md),
[initialization evidence](docs/evidence/2026-10-28-initialization.md),
[reference review](docs/discovery/reference-review.md), and
[license review](docs/discovery/licenses.md).

## Development

Use uv 0.13.6 and its managed CPython 3.14.10. The exact interpreter is in
`.python-version`; dependencies and tools are resolved in `uv.lock`. This is a
standalone `src/gz_mcp_lsp` package using uv_build. Version `0.0.0` is an
unreleased scaffold marker, independent of starter version 0.7.1.

```bash
git clone https://github.com/tvproductions/gz-mcp-lsp.git
cd gz-mcp-lsp
uv sync --locked --all-groups
uv run --locked pre-commit install
uv run --locked pre-commit run --all-files
uv build --no-sources
uv run --locked python tools/verify_distribution.py
```

If machine uv differs, use `uv tool run --from uv==0.13.6 uv ...`; ensure nested
hooks resolve uv 0.13.6 too. Do not bypass the project version check.
The four routine hooks run Ruff check/format, ty and unittest. At this stage,
the unittest hook runs distribution guard tests. There are no semantic runtime
tests yet; packaging tests are not semantic adapter acceptance. Inherited
engineering utility tests run separately, outside the routine gate. Deeper adoption/release
analysis remains outside routine hooks and CI; see the evidence record.

Install only the scaffold wheel for packaging inspection with
`uv pip install --python /path/to/clean/venv/bin/python dist/gz_mcp_lsp-0.0.0-py3-none-any.whl`.
There is no usable MCP command or published installation yet. No PyPI release or
tag has been published. Development was observed on macOS arm64; CI verifies
Linux. Windows runtime support remains a proposed validation target.

## Codex registration proposal

The following is a **future example**, not an executable installation instruction.
It assumes the review approves a `gz-mcp-lsp --config` command and settings schema.
Provision the adapter and ty before registration; do not use request-time `uvx`
or another launcher that may fetch dependencies.

```toml
[mcp_servers.gz_mcp_lsp]
command = "/absolute/path/to/preinstalled/bin/gz-mcp-lsp"
args = ["--config", "/absolute/path/to/settings.json"]
startup_timeout_sec = 30
tool_timeout_sec = 60
```

Example proposed application `settings.json`:

```json
{
  "schema_version": 1,
  "workspace_root": "/absolute/path/to/workspace",
  "ty_executable": "/absolute/path/to/preinstalled/bin/ty",
  "request_timeout_seconds": 20
}
```

No settings loader exists. Application configuration will use JSON, without
environment-variable overrides. Codex's native TOML remains its own contract.
The host supports stdio launch commands in trusted project `.codex/config.toml`;
see [official Codex MCP documentation](https://learn.chatgpt.com/docs/extend/mcp).
Do not add this hypothetical entry to the adopted engineering plugin configuration yet.

## Contribution and security

Read [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md) and [AGENTS.md](AGENTS.md).
Keep private code, paths, logs and credentials out of public fixtures and issues.

## Acknowledgments and license

Isaac Phi's [mcp-language-server](https://github.com/isaacphi/mcp-language-server),
reviewed at [v0.1.1](https://github.com/isaacphi/mcp-language-server/tree/v0.1.1),
informed the idea of exposing language-server navigation through MCP and provided
an architectural comparison. gz-mcp-lsp is an independent Python implementation;
no upstream source has been ported or copied. It is not an official fork or
upstream continuation, and is not affiliated with Astral or OpenAI.

This repository was generated directly from
[tvproductions/gz-skills-first-starter](https://github.com/tvproductions/gz-skills-first-starter).
Its adopted published baseline is v0.7.1 at
`27594dbaec853e6bde037b0aaf3f0427a3f053f9`, recorded in
`.skills-first/bundle.lock.json`. The inherited policy and analysis tools retain
their provenance and notices. Historical starter documents describe that project,
not delivered adapter behavior; see [documentation scope](docs/README.md).
Superpowers and gz-skills remain independently owned native plugins; Backplane
is deferred and disabled. The user selected the lite lane.

Original project work and inherited starter material use the [MIT license](LICENSE).
Upstream projects and future dependencies retain their own licenses; see [NOTICE](NOTICE).
