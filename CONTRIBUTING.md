# Contributing

The revised implementation plan was approved on 2026-11-01 and execution has begun.
Discuss substantial scope changes in an issue and obtain approval before changing
the approved runtime contracts. Keep PRs small and
link the owning intent, relevant acceptance cases, actual checks and limitations.
Use the PR template. Public issues must use synthetic reproductions.

Follow README.md for locked setup and AGENTS.md for engineering policy. Install
pre-commit locally; CI uses the same four routine checks plus artifact verification.
Use unittest, current Python 3.14 idioms, narrow domain/adapter boundaries and
explicit lifecycle/error contracts. Do not add pytest, Makefiles, environment
application settings, runtime auto-installation or copied upstream source. Diagnostics and guarded
rename/edit are included in the revised parity objective; they require authority/conflict/recovery tests and real ty/host evidence before acceptance.

New semantic capabilities need red/green tests at their public seam, deterministic
structured results, Unicode/URI edge cases, real pinned-ty fixture evidence and
an installed-artifact check. The unittest hook includes distribution guards,
actual pinned-ty and runtime-only outside-checkout tests of all nine tools.
The acceptance fixture contains shared_runtime/run_shared_cli and three importing
packages with independently enumerated identifier positions. Platform-specific
write tests run on Linux x86_64/macOS arm64; Windows verifies reads and mutation
denial. Keep skip inventories visible in CI. Native host acceptance additionally
requires real Codex transcripts and approval/denial evidence; direct SDK tests
cannot substitute for it. See [T11 acceptance](docs/evidence/2026-11-01-codex-acceptance.md).
Deeper analysis runs at adoption/release acceptance separately from routine CI.
See the initialization record for unresolved requirements.

Keep license notices, starter provenance and attribution. Version public contracts
with SemVer; every major including 1.0.0 needs a new PRD. Contributors do not
publish releases as part of ordinary PRs. Maintainer review controls merge.
