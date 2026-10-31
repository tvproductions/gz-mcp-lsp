# Approved execution: runtime inputs (T0), 2026-10-31

The user explicitly approved revision-2 specification and plan on 2026-10-31.
Native isolated worktree; implementation uses the inline Superpowers workflow and
unittest red/green verification. Original source checkout/main was not changed.
Plan headings were mechanically changed from T0 to Task 0 so upstream task-brief
scripts can consume them; no requirement or acceptance ceiling changed.

Selected/runtime-tested inputs: managed CPython 3.14.10 arm64; uv/uv_build 0.13.6;
official mcp 2.3.0; ty 0.0.93. Runtime direct dependency is exactly mcp==2.3.0,
without CLI extras. uv regenerated the lock (102 resolved packages, 100 installed
for all groups), retaining dev/hygiene separation. MCP requires async/HTTP/schema/
crypto dependencies even for stdio; none is a reason to enable network transports.
No automatic dependency installation is added to runtime requests.

Test-first packaging change: old verifier rejected the approved MCP Requires-Dist;
observed negative run retained in execution ledger. The verifier now requires exactly
that dependency and continues rejecting unexpected requirements, starter code,
development payloads and environment leakage. Five distribution tests pass; locked
Ruff check/format, ty, unittest, source-independent build and clean outside-source
runtime-only wheel installation pass. No MCP adapter capability is claimed.

SDK tag/signatures and installed metadata inspected. A bounded Python 3.14 smoke
probe verifies dataclass input schemas, structured values and actual asyncio task
cancellation propagation: see SDK qualification JSON. SDK Python fields use snake_case
(input_schema/structured_content); wire aliases remain the SDK's responsibility.
This is SDK compatibility evidence, not MCP stdio/ty/Codex interoperability acceptance.

License review: installed SDK and mcp-types are MIT; direct SDK dependency metadata
identifies MIT/BSD-3-Clause, Apache-2.0 and PSF-2.0 licenses. Full installed metadata
inventory retained in the execution workspace. No dependency licenses are changed
or source redistributed. Resolved all-group vulnerability scan reports no known
vulnerabilities; graph-wide license/source acceptance remains a T12 obligation,
not a claim inferred from a top-level MIT field.

Independent gz-skills update: v0.8.3 at
`d6acc26e28ca1c4f43e5bb46d8973021d7d006c3`, via official gz-skills native marketplace.
Both project catalogs, bundle selection and adoption lock reconciled; starter
provenance stays v0.7.1 at `27594dbaec853e6bde037b0aaf3f0427a3f053f9`.
component-overrides.json records previous revision/rollback and new source.
The old gz-skills@skills-first-starter identity is disabled only in this project.
Native manager refresh/add and fresh app-server discovery select 0.8.3; all 44 skill
files match the pinned upstream tree. Native add's new user enablement was corrected
to disabled; outside-project fresh process discovers neither starter identity.
Stale Superpowers marketplace cache was refreshed to pinned 7.0.1; Backplane remains
disabled. See native-discovery JSON. No shared cache was hand edited.

This intentional independent override differs from the published starter-managed
content; original starter configure/status will report a content conflict rather
than certify exact-baseline identity. Do not overwrite the reviewed selection to
make helper status green. Template revision is not relabeled as an app revision.

Open blocker: starter issue #1 remains open; selected shared cognitive scorer is
not available/qualified. Complexipy remains an explicitly failing reproducer.
No private scorer fork, replacement, score waiver or strict engineering acceptance.
Approved bounded implementation continues; E3/E4 and final milestone remain incomplete
until independent qualification is possible. Owner: tvproductions/starter maintainer.

T0 runtime input gate: observed SDK/runtime/distribution checks pass; cognitive strict
acceptance remains external/incomplete and separately recorded. All actual adapter,
LSP semantic, safe mutation and Codex-host acceptance rows remain NOT RUN.
