# T7 immutable edit planning â€” 2026-11-01

Eight planner tests failed before edit_plan.py existed, then passed. The planner
accepts saved snapshots and performs no filesystem reads or writes. It is not yet
wired to mutation tools; the public catalog remains four read tools.

Verified controls include original-snapshot offsets, adjacent ranges, overlap and
coincident-insert conflicts, percent-encoded/physical aliases, exact UTF-16/CRLF/
mixed-newline/EOF edits, rejection of an entire resource-operation edit, non-null
document versions, no-op detection and byte/count ceilings. The zero-IO test
forbids file opens and metadata lookups and verifies unchanged source hashes.

EditPlan, PlannedFile, PlannedEdit and ChangeAnnotation are frozen values with
tuple members. plan_id binds generation, actual/claimed before-image hashes,
postimage hashes, physical identity/mode, version, normalized edits, expiry and
confirmation annotations. A forged-before-image regression initially left the
digest unchanged and now passes after actual bytes were bound independently.

Both changes and text-only documentChanges are supported; duplicate or
contradictory forms fail. Confirmation metadata remains visible and is never
treated as authenticated consent.

Keyword-only limits and expires_at preserve the approved three-argument planning
interface. Default expiry is wall-clock now plus configured TTL; explicit expiry
makes deterministic tests possible. The staging ceiling counts before plus after
images, conservatively bounding memory/recovery preparation. No target authority
or filesystem safety is inferred from a valid digest: T8/T9 still own those gates.

All 114 discovered tests and the full Windows/Linux gates pass. Separate
C901 src and scoped portability checks pass. macOS/hosted CI remain unverified.
The task ledger records the local commit. No filesystem
transaction, recovery engine, mutation tool, release or full acceptance is claimed.
