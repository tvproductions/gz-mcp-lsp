# T4 saved documents and production hover — 2026-11-01

Implementation task T4 of the approved reference-parity plan. G1's first real
MCP → installed adapter → pinned ty hover passes on Windows x86_64 and Linux
x86_64 (WSL2, native Linux filesystem). This is partial development evidence,
not nine-tool, mutation, hosted-CI or release acceptance.

Managed CPython 3.14.10, uv 0.13.6, MCP SDK 2.3.0 and ty 0.0.95 were used.
The independently authored fixture is tests/fixtures/semantic_workspace; its
expected.json identifies main.py line 2, UTF-16 character 2. Installed SDK stdio
hover returns the original plaintext "int". Changing unopened dependency.py's
return annotation to str yields "str" and a different generation. Creating
ty.toml changes the generation again. Imports and execution originate outside
the source checkout; fixture code is never imported or executed.

## Observed controls

- Thirteen generation assertions failed before documents.py existed; four
  navigation assertions failed before navigation.py existed. Production SDK
  catalog assertion failed while hover was absent, then passed with the real tool.
- Generation/read leases share one admission counter. Empty workspaces need no
  fabricated URI or didOpen. Contexts retain their original RpcClient. Barriers
  verify stale-reader invalidation, bounded admission, cancellation release,
  same-mtime dependency changes, create/delete/rename and nested configuration.
- Reconciliation invalidates outstanding RPCs, drains readers, reaps the old child,
  and only then starts its replacement. Actual child handles independently prove
  reaping before spawn. Unexpected child failure cannot trigger semantic restart,
  including when source also changed. Failed replacement startup is sticky rather
  than silently retried by later reads. Both regressions failed before correction.
- Final manifest validation rejects a late success from an invalid generation.
  didOpen is sent once at version 1; bounded eviction/shutdown sends didClose.
  Exclusive saved changes honor full/incremental sync with increasing versions.
- A failing deadline regression established that the reader-drain deadline must
  end before the transaction body. Exclusivity remains held through its body.
  T9 still owns actual commit/rollback/recovery tests and cancellation shielding.
- A cancelled thread scan originally outlived its admission owner. An observed
  failing barrier regression now passes: synchronous bounded IO finishes before
  cancellation releases ownership.
- SDK middleware rejects bool/float/string coordinates, JSON-string positions
  and extra argument fields before coercion. Structured results and JSON text
  agree. URI/position forwarding and original server type text are asserted.
- ty initialization explicitly sets untrustedWorkspace=true and
  experimental.useUv=off, preventing external command/installation integrations.
  This control was absent in its failing initialization assertion.

## Scope and verification

Nested pyproject.toml, ty.toml, .gitignore and .ignore join the existing source/
configuration manifest. Dependency environments remain immutable during a session.

Freshness fails UNSUPPORTED when custom adapter exclusions cannot be reconciled
with ty indexing, inherited/user ty configuration is outside the tracked scope,
configured first-party roots escape tracked source, custom typeshed is selected,
or a baseline is not an explicitly tracked configuration input. Source patterns
cannot escape the root. These are deliberate fail-closed limitations, not claims
that arbitrary ty configurations have been covered. Native APPDATA/XDG_CONFIG_HOME
are consulted only to identify ty's own external configuration and reject it;
they never override product JSON settings.

The required four-command gate passed on Windows and native Linux, including
installed-distribution checks. The isolated installed interoperability setup
exports the exact runtime lock graph as pylock.toml and synchronizes it offline
before calls. A fresh Linux cache exposed the previous pip resolver's missing
index metadata; the lock-based correction passed on both systems. This setup
installs nothing during MCP requests.

C901 against src passes ceiling 20. The selected cross-platform skill's scoped
src/tests/tools audit returns []. The existing four routine hooks are retained.

CI now declares ubuntu-24.04 x86_64, macos-15 arm64 and windows-2025 x86_64
with exact interpreter/architecture assertions and pinned actions/tools.
New-branch hosted CI and macOS runtime execution remain UNKNOWN: nothing has
been pushed. Linux WSL evidence is local evidence, not a GitHub runner receipt.

The [actual Codex checkpoint](2026-11-01-codex-feasibility.md) establishes installed
invocation and native allow/deny interaction. Full H1–H3 remains T11.
