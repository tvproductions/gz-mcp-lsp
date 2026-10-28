# Python work through gz-skills

The starter requires code to follow the selected Python family's relevant idioms
and advances. gz-skills supplies reusable workflows; the starter supplies the
[runtime and code policy](baseline-policy.md). Choose the smallest workflow that
fits the task, confirm discovery, and preserve project scope and authorities.
This guide reinforces and highlights those upstream behaviors for adopters;
it is not another skill or an implementation of their discovery/workflow logic.

## Current selection: v0.8.0

The bundle and both catalogs now select released gz-skills v0.8.0 at
`75bcd11ee9371ecff1a7b3432d2af29d4bdbb788`, checked October 18, 2026.
Compared with v0.7.0, it adds the explicit-only `gzs-release` primitive and release
routing; the Python workflows described below are unchanged. Release invocation
does not grant publication authority. The earlier installation receipt below
belongs to v0.7.0 and is not v0.8.0 host-acceptance evidence. Verify native loading
and actual discovery separately in each adopter.

## Verified coverage in v0.7.0

| Need | Existing skill | Actual scope |
| --- | --- | --- |
| Find unnecessarily elaborate Python patterns | `gzs-pythonic-pattern-detect` | Read-only review of concrete pattern roles and simpler Python alternatives, accounting for runtime, public contracts and architectural boundaries |
| Implement a selected simplification | `gzs-pythonic-pattern-apply` | One authorized candidate, with unchanged before/after behavior evidence and relevant verification |
| Review or fix operating-system assumptions | `gzs-cross-platform-python` | Paths, explicit text encodings, subprocesses, temporary resources, cleanup and tests across Windows/macOS/Linux; includes deterministic portability checks |
| Inspect or choose a project profile | `gzs-project-setup` | Explicit lite/heavy choice and Python environment guidance; adopted project policy takes precedence over defaults |
| Check freshness or update a runtime/toolchain/template/plugin | `gzs-update-dependencies` | Separate review/update modes, approved family preservation, project additions and exception handling; review mode changes no environments or pins |
| Survey a bounded source population for debt | `gzs-tech-debt-review` | Existing project probes and direct source/history review; reports missing coverage rather than inventing a clean assessment |
| Review an implementation diff | `gzs-change-review` | Evidence-backed defects and maintainability/compatibility risks in a bounded change; not a style rewrite or broad modernization audit |

SP remains the feature design and implementation workflow. The pattern pair is
appropriate when the concrete problem is pattern scaffolding, not as a mandatory
entry for every Python change. Portability review fits code at OS seams. Setup
does not follow automatically from inspecting these skills or adopting this
starter; it does not select a profile or install the combined stack for us.

## Apply project policy, preserve upstream scope

Ask the selected workflow to use the project's allowed Python family, official
versioned documentation and relevant opportunity guide. Assess concrete code
against meaningful improvements and record adopt/defer/retain decisions and
behavior verification. For changes outside a skill's scope, ordinary authorized
agent work can use the same policy and SP workflow without creating a local skill.

Runtime discovery belongs in gz-skills. This starter reinforces the outcome:
upstream workflows must obey adopted runtime/engineering policy, distinguish
support constraints from execution evidence and report conflicts. It does not
repeat the runtime discovery procedure in copied adopter instructions.

The inspected release does not supply a dedicated comprehensive Python-version
idiom/stdlib-advance audit. Pattern simplification, portability and debt/change
review cover different parts of that requirement. Their presence is not proof
that every 3.14 opportunity or deprecation was assessed. State the reviewed scope
and remaining coverage, and reconsider a future upstream skill only after its
released instructions are reviewed. The current release reinforcement is
described below and is selected by the starter pin.

The setup/update skills' ordinary Python default is 3.13.x where no project
policy has been adopted. They explicitly preserve a different approved family.
Our binding chooses 3.14.x normally and host-compatible 3.12.x for XPPython3 code.
Their default assortment also includes Radon/Xenon; our retired-tool decision and
routine/on-demand boundaries take precedence. Keep these differences in project
guidance; do not propagate them into upstream plugins or infer a heavy profile
from the stack.

## Released upstream reinforcement

[gz-skills v0.7.0](https://github.com/tvproductions/gz-skills/releases/tag/v0.7.0)
at `6ebf803e4a2775d3742c84984a03548275b7c926` adds project-version/policy discovery to the existing Python pattern
detect/apply, cross-platform, setup and dependency-update skills. Those skills own
runtime discovery and scoped version-aware idiom, stdlib and deprecation
assessment. Project policy takes precedence over defaults; no starter-specific
Python family or tool assortment is introduced upstream.

This was the starter's previous selected release. Tagged
installs passed in disposable Codex and Claude configuration, and the uvx snapshot
installer; changed instruction bodies matched the release source. See the
[installation evidence](evidence/2026-10-11-gz-skills-0.7.0.json). Installation
is distinct from fresh-session workflow execution and combined stack readiness.
The release adds no comprehensive version-audit skill and preserves existing
workflow scope and authorization boundaries. Adopter updates remain explicit.

Authoritative current [Python workflow instructions](https://github.com/tvproductions/gz-skills/tree/75bcd11ee9371ecff1a7b3432d2af29d4bdbb788/skills)
remain upstream-owned; this template supplies emphasis and policy bindings.

## Historical v0.6.0 inspection evidence

Checked October 11, 2026 against gz-skills v0.6.0 at
`e722e808647481c4c9d2feab61f1843aa8e0b19a`, previously selected in this starter's bundle.
The GitHub Git-tree API returned nineteen skill entries. The seven inspected
installed `SKILL.md` bodies matched their Git blob hashes at that commit after
normalizing checkout CRLF to LF. This verifies source contents, not fresh-session
host loading or combined-stack readiness.

Historical inspected instructions: [pattern detection](https://github.com/tvproductions/gz-skills/blob/e722e808647481c4c9d2feab61f1843aa8e0b19a/skills/gzs-pythonic-pattern-detect/SKILL.md),
[pattern application](https://github.com/tvproductions/gz-skills/blob/e722e808647481c4c9d2feab61f1843aa8e0b19a/skills/gzs-pythonic-pattern-apply/SKILL.md),
[cross-platform Python](https://github.com/tvproductions/gz-skills/blob/e722e808647481c4c9d2feab61f1843aa8e0b19a/skills/gzs-cross-platform-python/SKILL.md),
and the [pinned catalog](https://github.com/tvproductions/gz-skills/tree/e722e808647481c4c9d2feab61f1843aa8e0b19a/skills).
