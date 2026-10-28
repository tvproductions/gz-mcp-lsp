# Astral acceptance implementation plan

Authorized by the user's October 18, 2026 instruction to address the
[uv deep-dive findings](uv-deep-dive.md). Intent is maximum applicable Astral
alignment for this starter and adopters, with demonstrated behavior and owned
exceptions. Preserve existing authorities and the configuration-only helper.

## Scope and execution

1. Add a binding adopter acceptance guide mapping requirements to evidence,
   applicability, results and exceptions. Cover uv/Ruff/ty effective configuration,
   runtime/executable provenance, locks, exact environment selection, installed
   artifacts, workspace boundaries and triggered advanced cases.
2. Write worked flat-application, typed-library and multi-package migrations.
   Include before/after files, behavior checks, resource/typing/dependency metadata,
   installed-artifact commands and rollback. Execute all three in temporary
   invented projects using the pinned interpreter and tools; retain a receipt.
3. Reconcile alignment/Python policy: maximum applicable recommendations,
   namespace/stub/coordinator distinctions, root/member selection, source
   independence, build isolation and the approved Ruff selection.
4. Link acceptance/examples from adoption, backport, configuration, README,
   AGENTS and the adopter fragment; regenerate packaged fragment resources.
5. Apply acceptance to this checkout. Retain the five declared check commands
   and four routine hooks; execute an additional source-independent build for
   this change and record its result without adding a hook or CI gate.
6. Update roadmap, changelog and continuation status; preserve historical
   analysis and receipts. Classify new adoption obligations for a future bundled
   minor under the existing version policy, without selecting/publishing one.
7. Validate local links, resource drift, all required checks and artifact behavior.
   Review the completed diff for omissions and claims exceeding evidence.

## Plan audit

Direct-document fallback under `gzs-plan-audit`; no project plan-audit command
exists. Citations refer to the linked artifacts' named sections to remain usable
as documentation grows; audited line anchors are recorded here for traceability.

| Intent to scope | Result | Authority |
| --- | --- | --- |
| Maximum alignment, especially Projects | Aligned | Deep dive: What maximum alignment means here, Projects, What changes in our assessment (lines 47, 61, 403 at audit) |
| Acceptance plus executed migrations | Aligned | Earlier proposal: Proposed bounded implementation; deep dive: Next implementation boundary (line 422 at audit) |
| Configuration/lock/workspace/build findings | Aligned | Deep dive: Projects items 3–9; supporting concepts |
| Preserve ownership, hooks, pins and helper seam | Aligned | AGENTS.md; architecture: adoption helper and Python ownership |

| Scope to plan | Result | Implementation/verification |
| --- | --- | --- |
| Acceptance and triggered cases | Aligned | Steps 1, 3, 5; checklist and starter receipt |
| Three actual migration paths | Aligned | Step 2; before/after and installed behavior receipt |
| All entry points and packaged instructions | Aligned | Step 4; link check, regeneration and resource drift tests |
| Scope containment and completion | Aligned | Steps 5–7; unchanged CLI/hooks/CI/pins and full gate |

Verdict: **PASS**. No missing or drifted requirement identified in this scope.
Real adopter pilots, host discovery, dependency upgrades, upstream changes,
new generic utilities and release publication are excluded. No delegation is
required. Python 3.14 adds no needed runtime feature to this documentation work.

## Implementation outcome

Steps 1–6 are implemented in the acceptance/migration guides, reconciled policy
and navigation, packaged adopter fragment and starter record. The migration
receipt records 64 commands; the artifact supplement verifies eight inventories
from four builds. Step 7's observed final gate is retained in the
[command receipt](../evidence/2026-10-18-astral-acceptance-checks.json).
Audit source anchors include `AGENTS.md:10` (zero skills), `AGENTS.md:36`
(Python/Astral policy), `AGENTS.md:76` (routine tools), and
`docs/engineering/astral-guidance-evaluation.md:103` (proposal at pre-edit audit).
No CLI, tool pin, hook or CI contract changed. No profile selection, pilot,
dependency refresh or publication was performed.
