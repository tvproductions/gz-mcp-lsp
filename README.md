# gz-mcp-lsp

An independent Python counterpart to Isaac Phi’s mcp-language-server, focused on
reliable ty-backed semantic navigation for Codex through MCP.

**Status: plan approved on 2026-11-01; implementation complete through T7; paused at a stage boundary.
Definition, references, diagnostics and hover pass installed MCP/ty checks; the full milestone remains unaccepted.**

The intended path is:

```text
Codex → MCP (stdio) → gz-mcp-lsp → LSP (stdio) → ty server
```

The proposed scope is one workspace and one Astral ty process. Functional parity
includes all six reference tools: definition, references, diagnostics, hover,
rename_symbol and edit_file. Exact URI/identifier positions correct ambiguous
name-resolution behavior. New tools are limited to document symbols, workspace
symbols and implementations; hover carries semantic type information.

Rename/edit use operator-enabled preview/apply with workspace containment,
conflict checks and durable recovery; the design does not promise portable atomic
multi-file changes. No request-time installation, network service, second language
server or general-purpose LSP framework is planned. The complete milestone is
accepted parity, semantic corrections/extensions, real Codex interoperability,
engineering evidence, then a deliberate stop.

Continue from the [bounded implementation handoff](docs/handoff.md); T8 is next.

Read the [revised architectural specification](docs/superpowers/specs/2026-10-28-semantic-navigation-design.md),
[version-pinned parity assessment](docs/discovery/reference-parity.md),
[acceptance matrix](docs/discovery/acceptance-matrix.md), and
[approved implementation plan](docs/superpowers/plans/2026-10-28-reference-parity.md).
Current [design-revision evidence](docs/evidence/2026-10-28-design-revision.md)
is separate from the historical [initialization evidence](docs/evidence/2026-10-28-initialization.md).
See the [license review](docs/discovery/licenses.md) for attribution/dependency boundaries.

## Development

Use uv 0.13.6 and its managed CPython 3.14.10. The exact interpreter is in
`.python-version`; dependencies and tools are resolved in `uv.lock`. This is a
standalone `src/gz_mcp_lsp` package using uv_build. Version `0.1.0` identifies the
unreleased development package, independent of starter version 0.7.1.

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
The four routine hooks run Ruff check/format, ty and unittest, including actual
pinned-ty and outside-checkout installed hover integration tests. Fixture setup
uses the exported runtime lock graph before MCP calls. Packaging checks alone
are not semantic acceptance. Inherited
engineering utility tests run separately, outside the routine gate. Deeper adoption/release
analysis remains outside routine hooks and CI; see the evidence record.

Install the development wheel with
`uv pip install --python /path/to/clean/venv/bin/python dist/gz_mcp_lsp-0.1.0-py3-none-any.whl`.
The development package declares official mcp==2.3.0 and provides the stdio CLI
`gz-mcp-lsp --config /absolute/path/to/settings.json`. T6 implements definition, references, diagnostics and hover with exact URI/UTF-16 positions,
complete authorized declaration source and saved-byte generation checks. See
[navigation evidence](docs/evidence/2026-11-01-navigation.md) and
[pull-diagnostic evidence](docs/evidence/2026-11-01-diagnostics.md). See the [T4 receipt](docs/evidence/2026-11-01-documents-hover.md)
and [actual Codex checkpoint](docs/evidence/2026-11-01-codex-feasibility.md).
There is no published installation, PyPI release or tag. Local Windows x86_64
and Linux x86_64 gates pass; macOS runtime and new-branch hosted CI remain unverified.

## Codex registration (development)

The CLI and JSON schema exist locally; semantic tools and real Codex acceptance
remain under implementation. This example requires a separately installed development wheel.
Provision the adapter and ty before registration; do not use request-time `uvx`
or another launcher that may fetch dependencies.

```toml
[mcp_servers.gz_mcp_lsp]
command = "/absolute/path/to/preinstalled/bin/gz-mcp-lsp"
args = ["--config", "/absolute/path/to/settings.json"]
startup_timeout_sec = 30
tool_timeout_sec = 60
```

Example application `settings.json`:

```json
{
  "schema_version": 1,
  "workspace_root": "/absolute/path/to/workspace",
  "ty_executable": "/absolute/path/to/preinstalled/bin/ty",
  "request_timeout_seconds": 20
}
```

The settings loader implements this JSON contract without environment-variable
overrides; see [configuration](docs/configuration.md). The CLI fixes transport to stdio. Codex's native TOML remains its own contract.
The host supports stdio launch commands in trusted project `.codex/config.toml`;
see [official Codex MCP documentation](https://learn.chatgpt.com/docs/extend/mcp).
Do not add this development entry to the adopted engineering plugin configuration yet.

## Contribution and security

Read [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md) and [AGENTS.md](AGENTS.md).
Keep private code, paths, logs and credentials out of public fixtures and issues.

## Acknowledgments and license

Isaac Phi's [mcp-language-server](https://github.com/isaacphi/mcp-language-server),
reviewed at [v0.1.1](https://github.com/isaacphi/mcp-language-server/tree/v0.1.1),
informed the idea of exposing language-server navigation through MCP and provides
the functional baseline for the revised specification. gz-mcp-lsp is an independent
Python implementation;
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

The project independently selects gz-skills v0.8.3 while retaining the adopted
starter v0.7.1. Its existing `skills-first-starter` marketplace identity now reads
this repository's project-owned catalog on `main`; every component in that catalog
has an immutable full commit pin. This reconciles the newer plugin without a
second discovery source or a shared-starter update. See the
[dependency-update receipt](docs/evidence/2026-10-31-dependency-update.md) for
rollback pins, verification and native loading evidence.

Original project work and inherited starter material use the [MIT license](LICENSE).
Upstream projects and future dependencies retain their own licenses; see [NOTICE](NOTICE).
