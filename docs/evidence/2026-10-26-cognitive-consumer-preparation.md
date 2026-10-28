# Cognitive consumer preparation — October 26, 2026

The operator resumed issue #1 and clarified that the shared engine is coming
from gzkit soon. Preserve that ownership: leave gzkit untouched, create no new
extraction project or private scorer, and await its actual candidate identity.
This work prepares the starter's consumer, not the upstream implementation.

Base: `287e235a0f4aa2ab2a470dbbd25065f3d5691d85`. Published 0.7.0 remains at
`a02635dad451f8f89c7801c2cbc02e2ec453d369`; its tag/assets are unchanged.
Working development metadata moves to unreleased 0.7.1 for this preparation.

The upstream scorer at current gzkit main
`05f6e3db2fa7fd0ffb6795b86263e90a33d056e7` has the same
`bfff5db7014f6000eb35a870f852f9a6c81da50a` blob previously shown to omit
functions under module loops/match. No upstream file, issue or plugin was changed.
No shared engine is installed, and there is no newly passing cognitive result.

Prepared: 42 independently specified cases; an installed-engine provenance and
qualification CLI; a consumer gate with independent function inventory, confined
source selection and ceiling 15. The
[integration contract](../engineering/cognitive-integration.md) owns the intended
interface, semantics, commands and remaining work. The consumer contains no
scoring increments or private scoring algorithm. Fixture answers used by tests
are deliberately rejected as unversioned engines by the public CLI.

Verified on managed CPython 3.14.10, required uv 0.13.5:

- All 16 new fixture/consumer regressions pass. They exercise the historical
  keyword blind spot, module/class loop/match discovery, duplicate names,
  15/16 thresholds, compiler-invalid source, partial scopes and missing/provenance
  failures. Fixture snippets compile or fail as explicitly expected.
- Existing analyzer regressions remain in scope. No routine hook was added;
  Ruff check/format, ty and the existing 39 adoption tests remain the routine set.
- C901 passes; the existing Lizard contract measures 147 functions, maximum 16,
  mean 3.435374149659864, no violations/errors, on src/tests/tools at this point.
  These cyclomatic results do not substitute for missing cognitive measurement.
- Both direct project Python and the uv-wrapped project execution report
  3.14.10 from `.venv/Scripts/python.exe`; `uv==0.13.5` names the package-manager
  version. It is not a Python 3.13 selector.

Final verification passes: locked all-group sync, all four routine hooks,
39 adoption tests, all 29 analyzer regressions (16 new), bundle/both catalogs,
source-independent 0.7.1 build and isolated installed distribution checks. The
sdist contains the qualification/gate code and fixture JSON. The JSON companion
records source hashes and explicitly leaves engine qualification unperformed.
The lock changes only this project's version; existing dependency pins are unchanged.
Exact-commit CI, real engine selection, candidate qualification and
source-corpus scoring remain unperformed for this worktree. Issue #1 stays open;
do not remove the release exception or publish 0.7.1 from this preparation.
