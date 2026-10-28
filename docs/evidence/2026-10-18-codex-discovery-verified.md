# Verified Codex CLI discovery — October 18, 2026

**PASS** for the published starter v0.4.0 SP + gz-skills pair on Windows,
Codex CLI/app-server 0.163.0. This supersedes the current acceptance result of
the [earlier UNKNOWN attempt](2026-10-18-codex-discovery.md), whose trust-boundary
observations and receipt remain unchanged. The user explicitly approved trusting
only the named disposable adopter, then verification continued.

## Provenance and native state

The separate reviewed starter checkout and the final native marketplace checkout
both resolve to release commit `b6f76dd75b4e6e779d6364cce0ff65bd73fda93a` (v0.4.0).
The published helper validated both catalogs, previewed and configured the
invented disposable Git project, recording version plus full starter SHA.
Current unreleased 0.4.1 changes were not used to generate those files.

The native `config/value/write` API added only the approved disposable project's
`trust_level = "trusted"` entry. A fresh process, without invocation overrides,
then loaded the project config and its pinned Git marketplace. The existing
user-owned gz-skills source is disabled only in the fixture's config to avoid
duplicate discovery there. No profile was inferred or initialized.

Native runtime resolution and `codex plugin list --json` confirm installed
plugins from `skills-first-starter`:

| Plugin | Full source revision | Inside adopter | Outside control |
| --- | --- | --- | --- |
| SP 7.0.0 | `bb92a77741419a4ab5f06e711a283343f1ada0c3` | Enabled; 15 skills discovered | Disabled; no SP skill loaded |
| gz-skills 0.8.0 | `75bcd11ee9371ecff1a7b3432d2af29d4bdbb788` | Enabled; 20 skills discovered | Starter source disabled; existing user source remains enabled |
| SP-BP, pre-release | `d0eeee829c491da02351e793544aa16ad96461bf` | Native installed/cache state reported, disabled; no skills loaded | No starter Backplane skills loaded |

No manual `plugin add` command was needed: the native runtime resolved the
configured entries. Installed/cache presence for the disabled Backplane entry
does not mean activation, readiness, lifecycle acceptance or explicit adoption.
Native managers can materialize configured disabled entries, as the
[official plugin guidance](https://developers.openai.com/plugins/build/plugins#enable-or-disable-a-plugin-for-a-repo)
explains. No source tree was manually copied into discovery or plugin caches.

An intermediate cache inspection initially returned starter revision `f14f3bc`.
Only `skills-first-starter` was selected for a native marketplace refresh. The
command reported no errors; subsequent direct Git resolution confirmed the
released v0.4.0 SHA. The final fresh model check occurred after that confirmation.
Do not assume a configured ref establishes the cache's actual checkout revision.

## Fresh-session and source evidence

Independent new app-server processes used the documented JSONL initialization
handshake, `config/read`, `skills/list` with `forceReload: true`, and ephemeral
read-only `thread/start`. These show enabled project layers, owning plugin IDs
and installed skill paths. The final snapshots use no session trust override.

Separate fresh `codex exec --ephemeral --sandbox read-only --json` sessions
provided model-visible startup-catalog evidence. The outside control additionally
used `--skip-git-repo-check` in an empty sibling directory. The prompts requested
catalog inspection only, forbidding disk searches, skill/workflow invocation,
profile creation, file changes, installs and delegation. Event streams show
completed model turns with no tool calls. The default model was retained.

Inside, the model reports `superpowers:using-superpowers` and
`gz-skills:gzs-router` present. It expands their startup aliases to the exact
native `skills-first-starter` cache paths reported by the runtime. Outside,
Superpowers is absent; `gz-skills:gzs-router` remains present through the user's
independent source. The outside native snapshot confirms ownership is
`gz-skills@gz-skills`, with zero skills from `*@skills-first-starter`. Backplane
is absent from both model-visible catalogs.

To check revision identity beyond labels and config, separate disposable
reference Git checkouts at the full pinned SP/gz-skills revisions supplied
`git show SHA:skills/.../SKILL.md` blobs. All **35 discovered SKILL.md files**
match those blob bytes exactly. The [redacted receipt](2026-10-18-codex-discovery-verified.json)
records each relative path, owning plugin ID and SHA-256, plus final model and
native observations. This comparison covers discovered skill files, not every
supporting file in the upstream packages.

The runtime labels these cached plugin skills' metadata scope as `user`.
That label alone does not establish enablement scope: effective config and the
independent outside-project control establish that this pair is enabled only in
the disposable adopter under the tested settings.

## Preservation and acceptance

The user-config before hash is
`b2119c1a1372e707336cb0dcec9baaeb860ffb046079f6c77f905789d0d15c97`;
after trust it is
`69db19c1a4eb853969e7effaa5e8b53bb2291ec2b60535176b4f2b2d46dec350`.
Parsing both TOML files and removing only the approved new trust entry yields
equal settings. The final user file is byte-identical to the immediate post-trust
snapshot: runtime resolution and scoped marketplace refresh added no further
user-config changes. All 26 previously visible installed-plugin records match
the outside control exactly, including enablement and sources. No unrelated
marketplace, plugin, source pin or existing trust decision was removed/changed.

| Acceptance dimension | Result | Evidence |
| --- | --- | --- |
| Released starter and actual marketplace checkout | PASS | Both resolve to v0.4.0 full SHA |
| Bundle/catalogs and helper configure/provenance | PASS | Locked published helper and four expected files |
| Trusted project-layer loading | PASS | Native effective-config layer enabled after approved trust |
| Native installed pair and owning sources | PASS | Manager records plus runtime plugin IDs |
| Fresh model-visible entry identities | PASS | New model turns; expanded aliases match installed paths |
| Pinned discovered skill content | PASS | 35 exact pinned-Git-blob comparisons |
| Project-only pair enablement and duplicate-source reconciliation | PASS | Inside/outside native snapshots and model turns |
| Existing native defaults/install records preserved | PASS | Only approved trust entry differs; 26 records unchanged |
| Backplane disabled and absent from discovery | PASS | Effective config and both catalogs |
| Backplane readiness/workflows, desktop UI, Claude/OpenCode | UNKNOWN | Outside this acceptance scope |

Repository verification after the evidence/guidance updates: locked sync, all
four routine pre-commit hooks (35 adoption tests), bundle/both catalogs, source
and wheel build, and isolated installed CLI checks pass. Neither these checks
nor this discovery receipt prove upstream workflow correctness, hook trust,
Backplane conformance, cross-harness behavior or an adopter pilot.

The next adoption milestone is a separately authorized adopter pilot; FDAU
remains the primary candidate. Its project/runtime/domain authorities must be
read before work. Repository-local utility ownership and other deeper-tool
proofs remain open. Cosmic Ray and this documentation remain part of the
unreleased 0.4.1 worktree; no later release or Git synchronization is implied.
