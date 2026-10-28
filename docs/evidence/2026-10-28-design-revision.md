# Reference parity design revision receipt — 2026-10-28

## Authorized work and result

User direction: revise the architecture and prepare a Superpowers implementation
plan for all six reference tools, corrected exact-position semantics, bounded ty
extensions, explicit write safety, real Codex acceptance and a deliberate stop.
This supersedes the initial read-only scope. It does **not** approve implementation.

Changed artifacts: revision-2 [specification](../superpowers/specs/2026-10-28-semantic-navigation-design.md),
[pinned parity assessment](../discovery/reference-parity.md),
[acceptance matrix](../discovery/acceptance-matrix.md),
[implementation plan](../superpowers/plans/2026-10-28-reference-parity.md), and
root governance/README/contribution/security/roadmap/changelog to remove conflicting
scope language. Product metadata description now reflects guarded source changes;
version, dependencies, lock and runtime sources remain unchanged. No new runtime,
test harness, settings loader, dependency installation or semantic fixture was
implemented in this repository. Test snippets in the plan are unexecuted design.

The plan is expressly requested before approval. This overrides normal Superpowers
spec-approval-before-planning order only for authoring the draft; execution remains
prohibited. Applied using-superpowers, brainstorming, writing-plans, gzs-router and
gzs-plan-audit, with OpenAI Docs for host approval options. A fresh builder reviewer
read specification/parity and reported no consequential unanswered questions beyond
the explicit human-review decisions. Plan self-review checks coverage/signatures/
proportionality; [alignment audit](2026-10-28-plan-audit.md) distinguishes alignment
from approval/readiness. All implementation task checkboxes remain unchecked.

## Verified reference findings

- Latest published upstream remains v0.1.1, commit
  `46e2950b7969334780675e7797e13f140d2d42ac`, publication 2025-05-16.
- Current default main commit is `e4395849a52e18555361abab60a060802c06bf50`.
  Git/gh compare shows one commit ahead and **only** go.mod/go.sum changed:
  x/text 0.24.0→0.25.0, x/sync 0.13.0→0.14.0, go-spew reclassified direct.
  All tool/configuration/transport/lifecycle/test implementations are unchanged.
  This does not assert dependency updates have no behavior effects.
- Inspected actual six registrations, tool implementations, JSON contract parsing,
  workspace-edit utilities, client initialization/synchronization, transport,
  callbacks, watcher, main process lifecycle, unit/integration tests and CI.
- Corrected an initial-review overstatement: code-lens tools are commented out in
  registration, even though implementation files exist. Six public tools register.
- Definition uses workspace-symbol search and returns complete declaration code;
  it is not textDocument/definition navigation. Revised P1 retains source retrieval
  and adds precise navigation rather than reducing parity to locations.
- References supplies workspace-symbol full range start as its LSP position.
  Exact URI/position in the Python contract structurally removes this inference.
  No private-project repro was copied or run; public semantic fixture proof remains future.
- Diagnostics discards pull output and reads push cache after sleep; public
  contextLines boolean conflicts with handler's int expectation. Both are corrections,
  not behavior to reproduce. Rename directly applies generic WorkspaceEdit; file
  edits slice bytes, clamp some bounds and apply without a multi-file transaction.
- Incoming tool context is not used consistently for cancellation; request wait
  ignores ctx; no write serialization across header/body; duplicate initialized
  and callback-registration ordering are source-grounded risks. They were not
  all reproduced as runtime failures during this assessment.

[Reference assessment JSON](2026-10-28-reference-assessment.json) records exact
source hashes and bounded test evidence. Upstream code stayed in a temporary
checkout. Executed `go test -json ./internal/logging ./internal/tools
./internal/utilities ./cmd/generate` on assessed main using Go 1.27.3 darwin/arm64:
exit 0, four package passes, 86 test/subtest pass events, two skipped generator
tests requiring vscode-languageserver-node. No reference language-server
integration or watcher suite, Go/ty run, Python adapter or Codex runtime test
was performed. Unit evidence is not a six-tool working-behavior certificate.

## Verified external inputs and maintained gaps

Official sources rechecked through gh: starter latest v0.7.1, gz-skills latest
v0.8.3, MCP Python SDK latest v2.3.0, ty latest 0.0.93. Selected SDK tag resolves
`2118f14f8a19bc158d8a1cf90af58d85d187f849`, ty tag resolves
`3db5e4df7becd3ca55fd06c78e98bf7c8a38e469`. Inspected SDK MCPServer/tool/lifespan/
stdio signatures at its tag and ty's language-server feature documentation at
its tag (including diagnostics/rename/implementation). No compatibility proof
or runtime package adoption is implied by that inspection.

OpenAI Docs [MCP host options](https://learn.chatgpt.com/docs/extend/mcp#other-configuration-options)
confirm per-tool approval settings and timeouts. The design does not invent
server-visible authenticated consent fields or assume host approval ensures safe paths.
Upstream LICENSE/ATTRIBUTION unchanged at assessed main; BSD-3-Clause reference,
MIT independently authored product/starter, Isaac Phi acknowledgment retained.
No source was ported or copied. Future SDK dependency graph audit remains required.

Strict acceptance gaps persist:

| Concern | Current evidence | Disposition / owner / revisit |
| --- | --- | --- |
| Qualified cognitive engine | Starter [issue #1](https://github.com/tvproductions/gz-skills-first-starter/issues/1) still open, updated 2026-10-27; selected shared engine not installed/qualified; complexipy defect receipt remains FAIL | T0/T12 named closure work; tvproductions maintainer + upstream availability. No substitution/waiver; required unknown prevents strict milestone acceptance |
| gz-skills reconciliation | Project provenance selects 0.8.0; latest release remains 0.8.3 | T0/T12 use gzs-update-dependencies and documented starter/native reconciliation/discovery; no managed cache/lock rewrite in this design task |
| Real runtime/host correctness | No Python runtime exists | All acceptance rows NOT RUN; actual pinned ty and actual Codex proofs scheduled, not inferred from source/mock tests |
| Write guarantees | No mutation code exists; portable cross-file crash atomicity is not promised | Human must approve recoverable bounded guarantee, quiescent workspace and POSIX initial write scope before implementation |

The lite profile, starter SHA/component selections, disabled Backplane, routine
four hooks, numeric ceilings and Python 3.14/uv/unittest baseline remain intact.
No template/plugin upgrade or unrelated native/global state change performed.

## Verification of this change

Observed local project gate (managed Python 3.14.10, uv 0.13.6):

- `uv lock --check`: passed, same 76-package resolution; no lock change.
- `uv run --locked pre-commit run --all-files`: Ruff check/format, ty, unittest passed.
- Five existing distribution guard tests passed; no semantic/runtime test claim.
- `uv build --no-sources`: sdist→wheel passed.
- `uv run --locked python tools/verify_distribution.py`: archive identity and
  clean outside-source installed import passed; no runtime capability tested.
- `git diff --check`: passed. Product-document local links and required task/acceptance
  coverage are checked during final artifact review; historical starter relative links
  remain historical rather than product-runtime claims.

No new runtime code or deeper analyzer was changed, so initialization's 29 utility
test/deeper-analysis results are not rerun or relabeled as runtime evidence. Current
strict engineering acceptance is incomplete regardless of scaffold gate success.
Git synchronization/hosted exact-commit CI result, if performed, is reported with
the final commit in the final handoff; prior initialization CI is not substituted.

## Operational proposal and strategic boundary

Finite tasks T0–T13 establish prerequisites; interoperability; six-tool parity with
required fixes; exactly three additional navigation tools; installed Codex proof;
engineering closure; milestone report and stop. Definition/source, diagnostics and
both mutation tools are included with positive and negative evidence, not indefinitely
deferred. Live ty capability absence or failed host interaction blocks acceptance.

Human judgment remains: behavioral versus drop-in schema compatibility; preview/apply
and recoverable multi-file guarantee; conservative scan/restart consistency and
external-source/OS/limit policies; owning cognitive/plugin prerequisite closure.
The proposed implementation is a bounded Python counterpart serving dependable
semantic navigation, not a reusable general-purpose language-server framework.
The assignment stops here, with unapproved documents and plan. No runtime work,
release/tag or unrelated project work is authorized by this receipt.
