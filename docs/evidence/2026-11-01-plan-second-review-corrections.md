# Second-review plan corrections — 2026-11-01

The user authorized correcting the three second-review findings. Prior working-tree
documentation over main `922bd622e5d0d21f833eba70550c01fe07616a90` is preserved;
the preceding [audit](2026-11-01-plan-execution-corrections.md) retains its historical
observations and hashes. Applied writing-plans and gzs-plan-audit, with the existing
repository quality gate and verification-before-completion workflow.

## Intent → scope

| Requirement | Evidence | Assessment |
| --- | --- | --- |
| Retain architecture and all nine tools | Specification unchanged; plan architecture, global constraints and final catalog assertion | Aligned |
| Correct exactly the three reviewed execution gaps | T0/T4/T9/T10 and acceptance S3/D1/W6 | Aligned; no runtime, dependency, configuration or CI change |
| Preserve implementation approval boundary | Plan status and specification human decisions | Aligned; every implementation task remains unexecuted |

## Scope → plan

| Finding | Correction and required future evidence | Assessment |
| --- | --- | --- |
| Production recovery admission was not assigned | [T9](../superpowers/plans/2026-10-28-reference-parity.md#t9-renameedit-mcp-tools-and-post-commit-semantics) assigns the real MCP lifespan startup gate, transaction-owned lock and recovery lockout. Installed-CLI stdio tests seed incomplete journals and prove recovery before mutation admission, conflict/corruption lockout, pending-startup cleanup and disabled/unsupported zero restoration. T8 remains the recovery engine owner | Aligned |
| Workspace symbols had no URI-free read context | [T4](../superpowers/plans/2026-10-28-reference-parity.md#t4-saved-file-documents-bounded-generations-and-real-interoperability-fixture) defines GenerationContext and Documents.generation(); document reads compose one shared lease with snapshot/open handling. T10 holds it across search/resolve and tests empty workspace plus mid-search/resolve change without inventing a document | Aligned |
| T0 ordered guard mutation before its negative control | [T0](../superpowers/plans/2026-10-28-reference-parity.md#t0-close-setupversion-prerequisites-and-establish-runtime-test-contract) now orders inspection, synthetic metadata-policy assertion red against unchanged verifier, verifier/fixture green, then uv-managed SDK adoption and real archive/installed verification | Aligned |

**Verdict: PASS for closure of these three plan findings and retained scope alignment.**
This is a document audit, not approval or proof of implementation behavior. Initial
write platforms, recoverable multi-file guarantees, performance tradeoffs and the
remaining human decisions are unchanged. Cognitive and actual host/platform
acceptance still require their own evidence; no strict acceptance is claimed.

## Verification and identities

Observed on Windows x86_64 with uv 0.13.6 and managed CPython 3.14.10:

- `uv sync --locked --all-groups`: exit 0; unchanged 76-package resolution.
- `uv run --locked pre-commit run --all-files`: exit 0; all four hooks passed
  (Ruff check, Ruff format, ty, unittest).
- `uv build --no-sources`: exit 0; sdist and wheel built.
- `uv run --locked python tools/verify_distribution.py`: exit 0; archive identity
  and isolated installed import outside the checkout passed. No runtime tested.
- `git diff --check`: exit 0. In-memory checks verified local Markdown links and
  anchors, unchanged specification/architecture/nine-tool catalog/T0–T13 headings,
  all acceptance IDs retained and all implementation checkboxes unchecked. They
  also checked T0's negative-control ordering, both lease contracts, assigned
  startup-recovery/disabled-mode tests, documentation-only changes and empty
  runtime dependency declarations.

The proposed SDK adoption, generation tests and recovery tests remain future work.
No new tests, code, lock, configuration or workflow changes were made, and no
commit, push, release or new hosted CI result is claimed. This scaffold gate is
not runtime or Windows/POSIX product acceptance.

Audited SHA-256 identities:

- Plan: `2a7ec5749bf3a87fb4df2a8d0e525efb305704aca9959f442548210fba7379f2`
- Acceptance matrix: `1e33415e436e6fbfaab226f09476aa4ceaa8fa1be612394400d06556834e8c7c`
- Specification (unchanged): `e8894f291eb7681525d39f8b502fc4be635ac98504defb77cfd7f30ff7ef8719`
