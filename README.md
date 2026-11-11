# gz-mcp-lsp

An independent Python counterpart to Isaac Phi’s mcp-language-server, focused on
reliable ty-backed semantic navigation for Codex through MCP.

**Status: plan approved on 2026-11-01; implementation and native host evidence complete through T11; paused at a stage boundary.
All nine tools have installed MCP/ty evidence and actual Codex invocation/approval checks;
the full milestone remains unaccepted.**

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

Continue from the [bounded implementation handoff](docs/handoff.md); T12 is next
after the final exact-commit platform gate. See
[T11 acceptance evidence](docs/evidence/2026-11-01-codex-acceptance.md) for verification limits.

Read the [revised architectural specification](docs/superpowers/specs/2026-10-28-semantic-navigation-design.md),
[version-pinned parity assessment](docs/discovery/reference-parity.md),
[acceptance matrix](docs/discovery/acceptance-matrix.md), and
[approved implementation plan](docs/superpowers/plans/2026-10-28-reference-parity.md).
Current [design-revision evidence](docs/evidence/2026-10-28-design-revision.md)
is separate from the historical [initialization evidence](docs/evidence/2026-10-28-initialization.md).
See the [license review](docs/discovery/licenses.md) for attribution/dependency boundaries.

## Development

Use uv >=0.13.6 and managed CPython 3.14.10. CI tests uv 0.13.7. The exact interpreter
is in `.python-version`; dependencies and tools are resolved in `uv.lock`. This is a
standalone `src/gz_mcp_lsp` package using uv_build. Version `0.1.0` identifies the
unreleased development package, independent of starter version 0.9.0.

```bash
git clone https://github.com/tvproductions/gz-mcp-lsp.git
cd gz-mcp-lsp
uv sync --locked --all-groups
uv run --locked pre-commit install
uv run --locked pre-commit run --all-files
uv build --no-sources
uv run --locked python tools/verify_distribution.py
```

Supported local and hosted uv versions need not match CI. Record the actual
executable/version and ensure nested hooks resolve it consistently. If uv is below
the minimum, use `uv tool run --from uv==0.13.6 uv ...` or another supported version.
See the [compatibility policy](docs/baseline-policy.md#uv-executable-compatibility).
The four routine hooks run Ruff check/format, ty and unittest, including actual
pinned-ty and outside-checkout installed nine-tool integration tests. Fixture setup
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
and Linux x86_64 gates pass; verify hosted platform results for the exact branch
commit through the Actions link in the handoff.

## Codex registration (development)

The CLI, JSON schema and all nine tools exist in the development package.
The [T11 acceptance record](docs/evidence/2026-11-01-codex-acceptance.md) distinguishes
installed/runtime checks, native host approval protocol evidence and platform results.
This example requires a separately installed development wheel.
Provision the adapter and ty before registration; do not use request-time `uvx`
or another launcher that may fetch dependencies.

```toml
[mcp_servers.gz_mcp_lsp]
command = "/absolute/path/to/preinstalled/bin/gz-mcp-lsp"
args = ["--config", "/absolute/path/to/settings.json"]
startup_timeout_sec = 30
tool_timeout_sec = 60

[mcp_servers.gz_mcp_lsp.tools.rename_symbol]
approval_mode = "prompt"

[mcp_servers.gz_mcp_lsp.tools.edit_file]
approval_mode = "prompt"
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
For a supported Linux adapter launched by a Windows host, see the
[isolated WSL registration example](docs/examples/codex-wsl.toml).

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
Its adopted published baseline is v0.9.0 at
`3f76acf0038b030bf5abd85ce4a419e890d3e420`, recorded in
`.skills-first/bundle.lock.json`. The inherited policy and analysis tools retain
their provenance and notices. Historical starter documents describe that project,
not delivered adapter behavior; see [documentation scope](docs/README.md).
Superpowers and gz-skills remain independently owned native plugins; Backplane
is deferred and disabled. The user selected the lite lane.

The project independently selects Superpowers v7.0.2 and gz-skills v0.10.1 with
starter v0.9.0. Backplane v0.2.0 remains disabled. The existing
`skills-first-starter` marketplace identity reads
this repository's project-owned catalog on `main`; every component in that catalog
has an immutable full commit pin. See the
[November 11 maintenance receipt](docs/evidence/2026-11-11-dependency-update.md)
for rollback pins, source reconciliation, verification and remaining acceptance gaps.

Original project work and inherited starter material use the [MIT license](LICENSE).
Upstream projects and future dependencies retain their own licenses; see [NOTICE](NOTICE).
