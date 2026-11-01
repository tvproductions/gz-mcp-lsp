# License and attribution review

The [October 28 source review](../evidence/2026-10-28-reference-assessment.json) and
retained notices cover independently authored product/starter material (MIT),
Isaac Phi's reference project (BSD-3-Clause, reference only; no source port) and
separately provisioned ty (MIT). Product/starter licensing does not relicense
dependencies or imply affiliation.

T0 adopted official MCP Python SDK 2.3.0 (MIT) at
2118f14f8a19bc158d8a1cf90af58d85d187f849 after reading its source/metadata.
The [runtime-input review](../evidence/2026-11-01-runtime-inputs.md) and
[package inventory](../evidence/2026-11-01-runtime-inputs.json) record all 30
conditionally reachable runtime nodes, including requested crypto extras and
published license metadata. MIT/MIT-0/BSD/Apache/PSF-family notices remain owned by
their respective packages. No dependency source or binary is vendored into the
product wheel; retain those notices if a future delivery redistributes dependencies.

Sources: [SDK at the selected revision](https://github.com/modelcontextprotocol/python-sdk/blob/2118f14f8a19bc158d8a1cf90af58d85d187f849/LICENSE),
[reference license](https://github.com/isaacphi/mcp-language-server/blob/v0.1.1/LICENSE),
[reference attribution](https://github.com/isaacphi/mcp-language-server/blob/v0.1.1/ATTRIBUTION),
[ty license](https://github.com/astral-sh/ty/blob/48c5ea1baf6144dc9918ae60040aaa4198b251ce/LICENSE).
Each runtime inventory row links its version-specific published PyPI metadata.
This bounded license review does not substitute for T12 dependency/security acceptance.
