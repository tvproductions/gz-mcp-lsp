# T0 runtime inputs — 2026-11-01

Execution authority: [approval record](2026-11-01-execution.md). SDK adoption is
setup work, not an accepted adapter capability. Runtime input inventory and source
hashes are in the [JSON receipt](2026-11-01-runtime-inputs.json).

## Selected dependencies and source review

The sole direct runtime dependency is official mcp==2.3.0, source
2118f14f8a19bc158d8a1cf90af58d85d187f849. Its MCPServer constructor, tool registration,
lifespan, stdio transport, metadata/schema conversion and cancellation paths were
read at that immutable revision. Three installed source blobs exactly match that
Git tree; their SHA-256/Git blob hashes are retained in JSON. ty 0.0.95 resolves
48c5ea1baf6144dc9918ae60040aaa4198b251ce. Managed Python remains 3.14.10, uv 0.13.6.

Reviewed the 30-package union of locked SDK dependencies and requested extras,
including conditional platform branches. It is not a claim that all 30 install on
every OS. PyJWT's requested crypto extra is included. Published license metadata
identifies MIT, MIT-0, BSD-3-Clause, Apache-2.0 / dual Apache-BSD and PSF-family
licenses. Retain each dependency's own notices; the product wheel does not vendor
their source. No copyleft or unknown-license node was identified in this bounded
metadata review. Vulnerability/deeper acceptance remains T12, not inferred here.

The official SDK necessarily brings HTTP/auth/native dependencies even though the
adapter will use stdio only. No CLI extras, alternate server framework, application
environment overrides or request-time installer were added. uv resolved 102
packages for the full project; unchanged existing tool selections are retained.
No transport beyond the approved stdio path is exposed by the product.

## Negative control and compatibility

Before touching the verifier or adding mcp, the new synthetic distribution tests
failed at assertion level: the old guard rejected intended SDK metadata and
accepted missing-SDK metadata. After updating the guard and obsolete fixtures,
all nine archive tests passed, including exact/unique requirement checks,
case/whitespace normalization and retained development/starter/source leakage guards.
Then uv add regenerated project metadata/lock and locked sync installed the SDK.

Three SDK contract tests pass on actual managed Python 3.14.10: stdlib dataclass
schema and structured result roundtrip; incoming cancellation unwinds a running
handler; public SDK middleware sees raw boolean coordinates and rejects them before
Pydantic coercion. This proves the required boundary can be implemented without a
direct Pydantic dependency. T3/T4 must apply raw validation to every product tool;
SDK annotations alone do not enforce the product's strict input contract.

Inspection also established that Client.list_tools returns ListToolsResult.tools
and negotiated newer tool results require a discriminator; use the SDK's typed
CallToolResult rather than constructing incomplete protocol dictionaries. SDK
schema/introspection/cancellation compatibility is not real-ty or Codex acceptance.

## Native discovery and external acceptance gaps

Fresh read-only Codex app-server initialize/skills/list with forceReload, following
[official OpenAI documentation](https://learn.chatgpt.com/docs/app-server#skills),
observed on this Windows host:

- Project: 40 gz-skills entries (20 duplicated), 15 Superpowers, no Backplane,
  zero discovery errors.
- Outside-project temporary control: 20 gz-skills and 15 Superpowers remain visible.
- Both gz-skills 0.8.3 managed sources independently byte-match all 44 release files
  at d6acc26e28ca1c4f43e5bb46d8973021d7d006c3.

Thus source identity passes, but duplicate/project-only discovery is **FAIL**.
The extra globally loaded marketplace is distinct from the project's retained
starter marketplace. Global defaults and native caches were preserved; this task
did not install, disable, delete or refresh plugins. Configured Git-source refresh
remains UNKNOWN in this host. Owner: operator/native manager; revisit before E4
strict acceptance through the owning maintenance workflow.

The upstream cognitive-engine issue remains OPEN with no qualified candidate.
Owner: starter maintainer/upstream; revisit on availability. No scorer substitution,
private fork or dependent-repository edit was performed. E3/E4 and terminal strict
acceptance remain incomplete, independently of the passing runtime-input checks.

## Verification

Observed: locked sync; 12 tests (nine distribution guards, three SDK probes);
source-independent sdist-to-wheel build; outside-source clean installation imports
both product and SDK at their declared versions. Ruff check/format and ty pass.
The full locked sync, four-hook gate, source-independent build and outside-source verification all passed before the T0 commit. G0 runtime inputs are tested; strict E3/E4 remain incomplete. No accepted
semantic operation, application settings loader or ty query exists at this step.

Python 3.14 opportunity review used the versioned official release notes at
https://docs.python.org/3.14/whatsnew/3.14.html#pep-649-and-pep-749-deferred-evaluation-of-annotations.
The relevant risk is deferred annotation introspection, exercised by the actual SDK
schema test. Use current stdlib dataclasses/typing; defer unrelated interpreter
pools, template strings and free-threading with no demonstrated adapter consumer.
