# License and attribution review — 2026-10-28

This is a bounded engineering review of observed licenses, not a completed audit
of a future runtime dependency graph. No MCP runtime dependency is declared yet.

| Material | Observed license | Disposition |
| --- | --- | --- |
| Starter v0.7.1 LICENSE | MIT, Copyright (c) 2026 tvproductions | Retain for copied engineering material and independently authored product; permissive public distribution fits the stated project |
| Starter NOTICE and analysis fixtures | Upstream ownership plus MIT gzkit example notice, Copyright 2026 g0 | Preserve verbatim required notices; utilities/fixtures remain engineering assets, not adapter runtime |
| mcp-language-server v0.1.1 and assessed main e4395849 | BSD-3-Clause; root copyright text says 2025 Phil Isaac; ATTRIBUTION also identifies Go Authors protocol generator | Reference only, no copied material. Acknowledge Isaac Phi/project accurately without rewriting upstream copyright or inheriting its generated code |
| Official MCP Python SDK | MIT, Copyright (c) 2024 Anthropic, PBC | Compatible candidate for independent adapter; retain relevant notices if redistributing it; inspect selected v2.3.0 dependency graph before runtime adoption |
| Astral ty | MIT, Copyright (c) 2025 Astral Software Inc. | Launch separately provisioned executable; no source or binary redistributed. Any future bundled delivery needs its own notices/license audit |
| Superpowers/gz-skills/Backplane | Independently maintained native plugin sources | Not vendored into product distributions; preserve source ownership and installed manager boundaries |

Sources inspected directly: starter LICENSE/NOTICE at the adopted commit;
[reference LICENSE](https://github.com/isaacphi/mcp-language-server/blob/v0.1.1/LICENSE)
and [ATTRIBUTION](https://github.com/isaacphi/mcp-language-server/blob/v0.1.1/ATTRIBUTION);
[SDK LICENSE](https://github.com/modelcontextprotocol/python-sdk/blob/main/LICENSE);
[ty LICENSE](https://github.com/astral-sh/ty/blob/main/LICENSE).
The SDK license was also verified at v2.3.0 and ty at 0.0.93, with the same
MIT copyright notices. Runtime dependency acceptance still needs the dependency graph audit. Tool dependency licenses/transitive packages are
not relicensed by the project MIT file. No affiliation or endorsement is implied.

Revision-2 assessment rechecked LICENSE and ATTRIBUTION at exact main
`e4395849a52e18555361abab60a060802c06bf50`; neither differs from v0.1.1.
Functional counterpart design does not change independent implementation or MIT
product/starter licensing. The six-tool scope does not authorize source copying.
