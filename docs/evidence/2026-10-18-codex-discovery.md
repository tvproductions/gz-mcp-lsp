# Codex discovery attempt — October 18, 2026

Result: **UNKNOWN** for the intended SP + gz-skills fresh-session acceptance.
The user authorized proceeding with the next adoption milestone after the
v0.4.0 release and Cosmic Ray work. The attempt uses invented disposable project
data and preserves existing native installations. It does not authorize an
FDAU pilot, Claude/OpenCode changes, plugin publication or another release.

## Verified setup

Host: Windows, native `codex-cli 0.163.0`; app-server initialization reports
0.163.0 as well. A separate shallow clone of the published `v0.4.0` annotated
tag resolves to `b6f76dd75b4e6e779d6364cce0ff65bd73fda93a`. Its helper is run with
locked uv execution and managed Python 3.14.8. Both native catalogs validate.
No current 0.4.1 worktree files supply the tested configuration or provenance.

From that clean published checkout, configure preview reports four writes and
no runtime readiness; apply writes the disposable Git project's config, lock,
adopter fragment and AGENTS entry. The lock records starter 0.4.0 and its exact
SHA. The generated project config selects the Git marketplace at that SHA,
enables SP/gz-skills and disables Backplane. It creates no skill tree or profile.

The user already has an enabled `gz-skills@gz-skills` installation, plus disabled
SP/gz-skills installations associated with other marketplaces. No existing source
is removed or overwritten. An additional disabled-source entry is appended only
to the disposable project's config to keep the user's independently installed
gz-skills source inactive there once project configuration is permitted to load.
That fixture-only reconciliation remains inactive while the project is untrusted.

## Native observations

Native CLI inventory did not expose the project marketplace. Rather than
registering it globally, the attempt used a newly launched native app-server
process and its installed version's generated schemas. The documented JSONL
`initialize` / `initialized` handshake precedes `config/read`, `skills/list`
(with the adopter cwd and `forceReload: true`) and an ephemeral read-only
`thread/start`. New thread IDs were returned; no model turn or skill invocation
was run. A second fresh process tested the host-reported canonical lowercase
Windows path for invocation-only trust, with the same outcome.

`config/read` confirms the actual project layer exists but reports a
`disabledReason`: the disposable adopter must be added as a trusted project in
the user's Codex config. The effective configuration omits its marketplace,
retains the existing user-disabled `*@skills-first-starter` entries, and retains
the separately enabled user `gz-skills@gz-skills`. Supplying a trust entry via
`-c` did not activate the project layer in these observed processes. This is a
bounded observation, not a claim about every Codex version or trust mechanism.

Runtime `skills/list` reports `gz-skills:gzs-router` owned by
`gz-skills@gz-skills`, not `gz-skills@skills-first-starter`. No skill owned by the
desired starter marketplace appears. This illustrates why finding the expected
name, a version label, configuration or a cache directory alone is insufficient.
The [redacted receipt](2026-10-18-codex-discovery.json) retains the relevant
effective settings, layer state and identity/source distinction. Unrelated
project names, private configuration, credentials and machine paths are omitted.

| Acceptance dimension | Result | Evidence / limitation |
| --- | --- | --- |
| Published starter version and exact revision | PASS | Separate v0.4.0 clone at the released SHA |
| Bundle and both catalogs | PASS | Published helper validation |
| Disposable configure preview/apply/provenance | PASS | Four expected writes; version and SHA recorded |
| Project config loaded under native trust | UNKNOWN | Host explicitly skips its untrusted layer |
| Native installation from the selected marketplace | UNKNOWN | Not attempted while project layer is disabled |
| Fresh-session SP/gz-skills identities from that source | UNKNOWN | Only unrelated user gz-skills is observed; no model turn |
| Exact loaded SP/gz-skills source revisions | UNKNOWN | Desired sources never loaded; catalog pins are intentions |
| Enablement confined to adopter project | UNKNOWN | Requires trusted positive case plus outside-project comparison |
| Existing user config preservation | PASS | Before/after byte SHA-256 matches; no install or enablement change |
| Backplane / Claude / OpenCode acceptance | UNKNOWN | Deferred or separate harness work, outside this attempt |

## Approval boundary and resumption

The proposed next action was a native `config/value/write` for exactly one
disposable project's `trust_level = "trusted"`, retaining a byte-for-byte backup
and existing entries. Automatic approval review rejected execution before it
started, stating that persistent trust in the user config weakens a security
boundary beyond the disposable request and recommending an invocation-only
alternative. No trust marker/backup was created and no config-write request was
sent. The invocation-only variants had already left the layer disabled.

The required next user decision is explicit permission to trust only the
disposable adopter through the native manager. After that decision, recheck
effective project-layer loading and duplicate sources, then use the native
installer. Inspect any installer writes before claiming project-only enablement;
preserve existing defaults and unrelated installs. Start another new host
session, verify the actual model-visible SP/gz-skills entry identities and their
owning installed full revisions, and compare an outside-project control. Record
PASS/FAIL/UNKNOWN independently; do not promote this attempt to a passing receipt.

## Guidance correction and validation

`docs/adoption.md` still expected a starter-owned `skills-first-start` identity,
contradicting the shipped zero-authored-skills contract. Remove that stale item
and require upstream identities with source ownership. No helper implementation,
bundle pin, generated input, routine hook or CI behavior changes for this attempt.
The existing unreleased Cosmic Ray work remains intact and uncommitted.

The repository's locked routine gate, bundle/catalog validation, source/wheel
build and isolated installed CLI verification pass after these documentation
changes. These checks validate the repository changes; they cannot substitute
for the blocked native discovery acceptance.

Official references checked through the OpenAI Docs workflow:
[project enablement and trust](https://developers.openai.com/plugins/build/plugins#enable-or-disable-a-plugin-for-a-repo)
and [native app-server lifecycle](https://developers.openai.com/codex/app-server).
Local generated schemas and observed host responses determine the exact tested
0.163.0 behavior. The docs and runtime support project-scoped configuration;
this attempt stops at establishing its trust prerequisite, not a demonstrated
inability to maintain project scope.
