# T12 current-input native acceptance — 2026-11-14

The user requested the next backlog item after Git synchronization. No open
product issue or PR was found; this bounded follow-up closes the outstanding
current-ty native evidence identified in the [handoff](../handoff.md) and approved
[T12 plan](../superpowers/plans/2026-10-28-reference-parity.md#t12-full-affected-input-engineering-acceptance-and-plan-reconciliation).
Runtime source, dependencies, public contracts and the pending 0.1.0 scope are
unchanged. **G5/T12 remains incomplete; T13 is NOT RUN.**

## Observed inputs and isolation

Product commit `2a7ae8023903b5f8fdc1c1f6b55a0286f25de3e4`; managed CPython
3.14.10, build 20261110; uv 0.13.8; official MCP SDK 2.3.0; actual
`ty 0.0.104 (b4bb5b2c8 2026-11-13)`; actual Codex CLI 0.169.0, default model
gpt-6.1-sol, macOS arm64. This supersedes the November 11 native proof's ty
0.0.101 and Codex 0.167.1 inputs only for the scenarios measured here.

The existing integration installer built a fresh wheel with `uv build --no-sources
--wheel`, exported the exact runtime lock graph, and installed both outside the
checkout. Isolated installed imports originate in that clean environment;
Ruff, pre-commit, coverage and tests are absent there. Ty was preinstalled from
the project lock before host calls. No request-time installation occurred.

Current schemas came from `codex app-server generate-json-schema --experimental`.
The host used stdio and ephemeral thread configuration; inherited MCP servers,
apps and plugins were disabled within that profile. Public synthetic acceptance
and hierarchy fixtures were copied outside the checkout. Mutation authority was
limited to that copy and its separate recovery directory. User configuration's
hash remained unchanged; no project/native configuration or managed cache was
edited. The [JSON receipt](2026-11-14-native-acceptance.json) records input,
wheel, ty executable, probe, protocol-schema and private-transcript hashes.

## Semantic and mutation results

The actual host exposed exactly the nine expected tools. One model turn invoked
each of the seven reads sequentially, with no duplicate or unexpected tool call.
Independent fixture assertions verified:

- Definition's exact shared URI/identifier selection and complete declaration.
- References' three expected package calls and exclusion of the decoy.
- Hover's callable signature and the current empty diagnostic report.
- Document symbol identity, both ambiguous workspace symbols, and expected
  implementation locations at lines 4, 9 and 14.

Native calls to both mutation tools with operator authority disabled returned
`MUTATIONS_DISABLED`; the complete recursive byte map stayed unchanged. A fresh
operator-enabled host thread then made exactly five model-driven mutation calls:
rename preview, denied rename apply, approved rename apply, edit preview and
approved edit apply. Actual host decisions were accept/decline/accept/accept/accept.

Both previews and the declined apply preserved every fixture byte. Rename changed
exactly the shared declaration and three importing packages. Edit changed only
the expected `value + 1` expression to `value + 2`. Fresh native definition output
contained the renamed identifier and edited expression. Approval decisions were
programmatic actual-host responses, not GUI/human-click evidence; a preview
plan identifier does not authenticate consent.

## Failure cleanup and transcript audit

Four independent installed-host probes killed ty, killed the adapter, suspended
ty to trigger the host's two-second tool timeout, or closed app-server stdin.
Each preserved recursive workspace hashes, reaped both observed adapter/ty PIDs,
and exited app-server with status zero. No dead request was replayed.

The final transcript audit confirmed seven read calls, five mutation calls and
no unexpected tool items. Two collector-only assumptions were corrected against
saved output: completed turns include their normal `userMessage`, and ty's version
string includes a build commit/date suffix. The corrected collector retains that
suffix and still rejects unexpected tools. No native scenario failed or required
an assertion, product behavior or deadline change. Private logs and disposable
scripts remain ignored under the plan's `t12-2026-11-14` workspace.

## Acceptance boundary

| Row | Result and limit |
| --- | --- |
| H1 | PASS: actual current host/model, installed adapter and pinned ty; all seven semantic reads asserted |
| H2 | PASS: disabled denials, preview/decline/approved writes, complete expected bytes and fresh semantics; programmatic approval boundary |
| H3 | PASS: current native timeout/death/EOF, unchanged hashes and process reaping |
| E2 | Fresh outside-checkout runtime-only installation and installed origin observed; archive verification remains a separate gate |
| E3/E4/G5 | Incomplete: qualified shared cognitive engine remains UNKNOWN; no substitute score or waiver |
| T13 | NOT RUN |

The preceding synchronized product commit's [exact-commit CI](https://github.com/tvproductions/gz-mcp-lsp/actions/runs/43625053546)
passed Linux x86_64, macOS arm64 and Windows AMD64. It ran 189 tests per lane,
with one Windows-only skip on POSIX and 26 POSIX-only exclusions on Windows.
That CI belongs to its exact commit, not these subsequent documentation changes.
The fresh native proof here covers macOS arm64 only. No Windows write support,
other-host native qualification, whole-milestone acceptance or release follows.

Final evidence checks pass: recorded input hashes match the checkout, local links
resolve, the public JSON contains no private filesystem paths or thread/auth
identifiers, and no probe-owned installed adapter process remains. A fresh
`uv build --no-sources` and `uv run --locked python tools/verify_distribution.py`
pass on the evidence tree. The preceding synchronized tree's all-group sync,
four hooks, 189-test suite and 29 analyzer regressions are reused for unchanged
runtime, tests, configuration and dependency inputs; this evidence-only follow-up
does not rerun unrelated deeper analyses or claim new hosted CI. No commit or
push was performed at the native-evidence checkpoint. The user subsequently
invoked `gzs-git-sync`; its final response records the exact evidence commit,
normal commit hooks, hosted CI and local/remote alignment.

The next prerequisite remains a separately versioned shared cognitive candidate
from the [owning issue](https://github.com/tvproductions/gz-skills-first-starter/issues/1).
The November 14 recheck already found it unavailable; no redundant recheck or
deeper measurement was performed in this follow-up. Resume qualification when
that prerequisite changes, then reconcile affected acceptance inputs before T13.
