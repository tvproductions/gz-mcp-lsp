# Contributing

The adapter is in design discovery. Discuss substantial changes in an issue and
obtain design approval before implementing runtime behavior. Keep PRs small and
link the owning intent, relevant acceptance cases, actual checks and limitations.
Use the PR template. Public issues must use synthetic reproductions.

Follow README.md for locked setup and AGENTS.md for engineering policy. Install
pre-commit locally; CI uses the same four routine checks plus artifact verification.
Use unittest, current Python 3.14 idioms, narrow domain/adapter boundaries and
explicit lifecycle/error contracts. Do not add pytest, Makefiles, environment
application settings, runtime auto-installation or copied upstream source.

New semantic capabilities need red/green tests at their public seam, deterministic
structured results, Unicode/URI edge cases, real pinned-ty fixture evidence and
an installed-artifact check. The current unittest hook runs distribution guards. Semantic tests must join
the routine gate with approved implementation.
Deeper analysis runs at adoption/release acceptance separately from routine CI.
See the initialization record for unresolved requirements.

Keep license notices, starter provenance and attribution. Version public contracts
with SemVer; every major including 1.0.0 needs a new PRD. Contributors do not
publish releases as part of ordinary PRs. Maintainer review controls merge.
