# Read-first delivery, then write parity

The user selected this approach on 2026-10-31: accept the seven read tools first,
then address the reference project's write parity. This short design records that
choice. The short two-milestone design presented in conversation was approved by
the user's “yes”; this document records it. The detailed execution-plan revision
was then reviewed in conversation and approved with “looks good”. Implementation
follows that plan one bounded package per handoff; no publication is authorized.

## Intent and approaches

The immediate purpose is to help Codex find and understand Python code through
ty's semantic knowledge. Codex continues to use its existing tools for editing.
Keep the independent Python implementation, official MCP SDK, one workspace,
one ty process and stdio boundaries from revision 2.

The selected approach has two independently assessed milestones. Continuing the
existing order would make useful navigation wait for filesystem write safety.
Permanently removing writes would abandon the agreed reference-parity objective.
Read first delivers the original benefit while retaining a bounded follow-on for
both write tools. No replacement type checker or rename analysis is introduced.

## Milestone R: read capabilities

The exact MCP catalog is `definition`, `references`, `hover`, `diagnostics`,
`document_symbols`, `workspace_symbols` and `implementations`. Preserve revision-2
input/result contracts, exact UTF-16 identifier coordinates, distinct full and
selection ranges, complete bounded declaration source, honest unsupported/empty
results and saved-file generation freshness.

No mutation tools, including preview-only rename/edit tools, are registered.
The read composition does not initialize filesystem transactions, create recovery
storage or perform crash recovery. User-confirmed review decision: explicitly
reject write-enabled application configuration for this milestone, so a setting
cannot activate the unfinished writer. Existing write modules need not be deleted;
they must remain unreachable from the read server's composition.

Acceptance requires asserted results for all seven tools through pinned ty, the
official SDK, an installed distribution outside the checkout and actual Codex.
The primary practical acceptance workspace is this repository's own Python code:
dogfood navigation through the adapter, tests and engineering tools at a recorded
candidate revision. Keep the installed executable outside the source checkout;
its semantic workspace may still be this repository. Use synthetic fixtures for
precise edge cases and a disposable repository copy for saved-change/failure tests.
Dogfooding demonstrates useful navigation on real project code; it does not prove
support for every Python codebase or a speedup without comparative evidence.
Prove exact targeting, same-name decoy exclusion, hierarchy/ambiguity handling,
diagnostic repair, saved dependency/config changes, invalid input, limits,
cancellation, child failure and cleanup. Prove that tool discovery exposes exactly
seven read tools, mutation calls are rejected, and source bytes remain unchanged.
These are measured gates, not claims that they already pass or a quantified speedup.

Use P1–P4, S1–S5, the diagnostic portion of S6, applicable C/D rows, H1/H3 and
E1–E5 from the existing acceptance matrix. C1 expects seven names here; C4/C5/D1/D3
retain their read obligations, with commit/recovery portions assigned to Milestone W.
E5 requires measured behavior on each claimed read platform; Linux write evidence
is not a prerequisite for read capability acceptance. Retain all applicable
engineering checks for code included in the candidate, including dormant modules.
Unknown/failed required evidence blocks the corresponding acceptance conclusion.
The cognitive qualification gap continues to block strict engineering acceptance;
a read capability result must not be described as strict acceptance or release.

Stop for a bounded handoff after read acceptance work. A failed or unavailable
gate is reported explicitly. Neither outcome automatically starts write work.

## Milestone W: remaining reference parity

After the read handoff and a new instruction to resume writes, complete
`rename_symbol` and `edit_file`. ty computes semantic rename edits; our adapter
validates and applies them. Retain operator authority, immutable preview/apply,
all-target validation, durable receipts, rollback/recovery and honest failure
outcomes. Full parity requires P1–P6, S1–S6, the nine-tool catalog, all applicable
C/D/W/H/E rows and the final deliberate stop.

T7's pure edit planner remains existing work. T8 stays incomplete and paused;
T9's three untracked drafts and their backup hashes must remain intact. Preserve
the metadata-loss and inherited-ACL findings, unresolved metadata-policy choice,
and unobserved Linux write/recovery behavior as Milestone W work. This revision
chooses no metadata exception and weakens no write-safety requirement.

## Planning consequences and retained controls

Retain historical task IDs and evidence. The revised plan should finish T10's
three read extensions before resuming T8/T9; split T11 host/distribution work and
T12/T13 engineering/acceptance work into read and full-parity obligations. T10's
catalog assertion becomes seven for Milestone R and nine for Milestone W.
Do not mark unfinished write tasks complete or reinterpret old receipts.

Reconcile the main specification, acceptance matrix, plan, roadmap, README and
active handoff with this design. The old T8-only continuation is
paused by the user's new direction. Continue one bounded package per handoff,
single-writer ownership, lite governance and disabled Backplane. Preserve pins,
JSON application configuration, project engineering policy and the four-hook gate.
No tag, release, push or host registration is authorized by this design record.
