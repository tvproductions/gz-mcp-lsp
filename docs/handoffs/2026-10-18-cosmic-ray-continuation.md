# Starter continuation after Cosmic Ray and Codex CLI — October 18, 2026

Read AGENTS.md, README.md, docs/architecture.md and ROADMAP.md. Recheck the live
worktree, branch, remote and CI before continuing. This supersedes current-state
and next-work guidance in the [earlier October 18 handoff](2026-10-18-starter-continuation.md);
preserve that document and all historical receipts.

Resume point: Cosmic Ray's bounded compatibility proof and fresh-session Codex
CLI discovery are complete. The next adoption milestone is an authorized FDAU
pilot under [ROADMAP.md](../../ROADMAP.md). First recheck live Git/CI and read
FDAU's current project/runtime authorities without changing that repository;
implementation waits for an explicit pilot scope. Desktop/other-harness proofs
and repository-local tool work remain independent options below.

## Published baseline and development state

Observed before this save point: October 18, 2026, 15:51 UTC; branch `main`,
HEAD and `origin/main` both `b6f76dd75b4e6e779d6364cce0ff65bd73fda93a`.
The worktree contained the completed 0.4.1 code, lock, generated resource,
evidence and guidance changes. The user now explicitly requested this handoff
and Git synchronization of that complete unit. Read live history for the final
synced commit identity rather than treating the pre-sync HEAD as the save point.

The user authorized publishing 0.4.0, then the Cosmic Ray proof. The
[v0.4.0 release](https://github.com/tvproductions/gz-skills-first-starter/releases/tag/v0.4.0)
is published; its annotated tag resolves to
`b6f76dd75b4e6e779d6364cce0ff65bd73fda93a`. Local locked checks and the exact
commit's Ubuntu routine/artifact CI passed. Never move that tag. The release
operation included no package-registry upload or plugin installation; the later
separately authorized native CLI proof is described below.

Post-release development is 0.4.1, unreleased. Cosmic Ray 8.7.0 is pinned in
`hygiene`, selected from 8.x after an isolated Python 3.14.8 proof. The explicit
`tools/engineering/evaluate_cosmic_ray.py` uses invented disposable source and
unittest: two killed/two intentionally surviving mutants, restored source,
passing before/after tests and failed-baseline/timeout/launch-error controls.
Read [the assessment and receipt](../evidence/2026-10-18-cosmic-ray.md).

Local 0.4.1 verification passes: 35 routine adoption tests, twelve explicit
analyzer tests, all four pre-commit hooks, bundle/both catalogs, locked sync/lock
check, sdist/wheel build and isolated installed CLI checks. Static portability
and the three explicit complexity checks pass. The save-point procedure runs
the complete locked gate again before committing, keeps hooks enabled and
verifies local/remote alignment after pushing. CI for the final synced commit
must be checked live; the latest previously observed passing CI was v0.4.0.

Important limitation: Cosmic Ray's baseline CLI returns zero when the test
executable cannot launch. Require structured normal-worker/survived-test
evidence for a clean baseline; reject incompetent/abnormal/pending outcomes and
separate timeouts from genuine kills. The proof does this explicitly. No score
gate, application mutation, routine hook or CI mutation step is added.

Other reviewed pins remain Python 3.14.8, uv/uv_build 0.13.1, Ruff 0.15.22,
ty 0.0.89 and pre-commit 4.7.0. ty's beta exception remains. SP 7.0.0 and
gz-skills 0.8.0 retain their full SHAs; SP-BP is independently pinned, expected,
deferred and disabled. No profile is inferred. Strong Python preferences remain
starter/project-owned; this repository distributes zero agent skills.

## Next work and boundaries

Fresh-session Windows Codex CLI/app-server 0.163.0 discovery is now **PASS** for
published v0.4.0. Preserve the [initial UNKNOWN attempt](../evidence/2026-10-18-codex-discovery.md)
and read the [verified receipt](../evidence/2026-10-18-codex-discovery-verified.md).
After the user explicitly approved only the disposable adopter's native trust
entry, fresh model sessions loaded both expected upstream identities. All 35
discovered SKILL.md files match their pinned Git blobs. An outside-project
control loads no starter-source skills and retains the existing user gz-skills
source; 26 existing plugin records are unchanged. User config differs only by
that approved trust entry. The actual marketplace checkout matches the v0.4.0
SHA after scoped native refresh. Disabled Backplane may be cached by the native
runtime but stays disabled and absent from the model-visible catalog.

The native host state and raw discovery harness/transcripts are local-only.
The disposable fixture is named `gz-starter-codex-discovery-20261018` under the
OS temporary directory; its approved trust entry remains in that user's Codex
configuration. Only the redacted receipts are durable repository evidence.
Do not assume these temporary files, caches or trust exist in another workspace,
and do not commit the local config backups or raw host responses. Reproduce the
Cosmic Ray proof from its tracked script with a new receipt filename; never
overwrite the historical receipts just to refresh their date.

1. Next is an authorized adopter pilot; FDAU remains the primary candidate. Read
   its authorities/runtime constraints and preserve domain behavior, data,
   profile choices and rollback evidence. No cross-repository changes follow
   merely from this handoff.
2. Desktop UI acceptance and other harnesses remain separate from the CLI proof.
   Preserve the existing upstream dependencies for Claude combined-stack and
   OpenCode readiness. Never copy upstream skill trees or infer Backplane readiness.
3. Repository-local open work remains analysis-utility ownership and bounded
   compatibility proofs for the remaining selected deeper tools. Generic tool
   maintenance stays in `gzs-update-dependencies`; no local maintenance skill
   or generic freshness reporter is authorized by this handoff.

Use current AGENTS.md/README checks. After resource-authority edits regenerate
wheel resources; after analyzer changes run the explicit analyzer unittest suite.
Cosmic Ray's proof is on demand, never a hook/CI gate. Windows mutation evidence
does not establish macOS/Linux mutation execution or full Python 3.14 grammar.
Desktop/other-harness discovery and Backplane combined-stack readiness remain
separate proofs; CLI discovery does not establish upstream workflow correctness.

The current authorization covers this handoff, ordinary commit/push and remote
verification in this repository. It does not authorize another release, tag,
adopter implementation, additional native trust/install changes or Backplane
activation. Version 0.4.1 remains unreleased after synchronization. Published
v0.4.0 and all historical UNKNOWN/failing receipts remain intact.
