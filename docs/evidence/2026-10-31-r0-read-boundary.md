# R0 read-only boundary — 2026-10-31

The user reviewed the read-first plan in conversation and approved it with
“looks good”. This package completes **R0 only**, preserving one writer and one
bounded package per handoff. It does not implement T10 or advance T8/T9.

## Behavior and negative controls

The JSON parser now rejects mutations.enabled=true with UNSUPPORTED before any
recovery-storage validation or language-server launch. MCP composition separately
rejects programmatically constructed write-enabled Config objects. Disabled
settings retain existing read behavior and no transaction/recovery owner is created.

Before implementation, valid enabled JSON and direct write-enabled composition
both failed their new assertion: AdapterError was not raised. A CLI subprocess
using a disposable synthetic executable then proved that the child actually
launched. All three controls now pass. The CLI returns status 2, no stdout and
UNSUPPORTED on stderr, with no child marker or recovery state created.

An additional real-ty characterization test invokes all four currently registered
read tools and rejects rename/edit previews, with transaction construction trapped,
unchanged fixture source bytes, absent recovery storage and a reaped child. This
protects existing behavior; it is not relabeled as a test that failed before the fix.

## Candidate verification

The [source-hashed receipt](2026-10-31-r0-read-boundary.json) records base revision,
runtime/test source hashes, tool/interpreter provenance, artifact hashes and commands.
Observed macOS arm64, CPython 3.14.10 and uv 0.13.6. Both focused suites passed:
configuration 7 tests; MCP API 6 tests including actual ty. Existing asyncio
slow-task warnings were observed in synchronous subprocess-oriented tests.

The exact four-command gate passed with exits **0 / 0 / 0 / 0**: locked all-group
sync, all four pre-commit hooks, source-independent build and distribution verifier.
The verifier installed outside source and exercised actual-ty MCP hover. It does
not prove all seven tools or actual Codex host acceptance.

Separate runtime C901 passed. Repository-owned Lizard passed on all runtime files:
128 functions, maximum 19, function/module/overall ceilings unchanged at 20.
An earlier changed-file run found parse_config at 21 after adding the guard;
remove its now-unreachable enabled-write authority branch, retaining early rejection.
The changed-file maximum is 18. The final four-command gate was rerun afterward.

Three unfinished T9 drafts were temporarily moved to the Git-common handoff archive
after checking the existing backup manifest. They were restored byte-for-byte after
the candidate gate. No test discovery, hook, threshold or T9 source was altered to
obtain a pass. The restored combined dirty tree is not the passing R0 candidate;
its known draft format/type/unregistered-tool failures remain outside this candidate.
Full logs remain in the ignored workspace for the read-first plan.

## Boundaries and remaining work

Runtime changes are limited to config.py and mcp_api.py, with their boundary tests.
Approval/scope/acceptance documentation now reflects seven reads before write parity.
No dependency, pin, filesystem transaction or mutation draft changed. The next package
is T10's three read extensions, followed later by installed/actual Codex dogfooding
of this repository. No complete read milestone or full reference parity is accepted.

Linux read candidate execution and actual Codex acceptance remain unobserved.
Qualified cognitive scoring remains unavailable and blocks strict engineering
acceptance. T8 remains incomplete with metadata/private-storage and Linux write
gaps; no metadata exception was chosen. Whole-branch independent review remains
later. No implementation push, exact-commit CI, release or tag is authorized here.

The local commit containing this record follows the receipt's base revision;
resolve its exact SHA from Git. Normal commit hooks are required, with the same
temporary draft archive/restore safeguards. A local commit is not remote backup.
