# T1 configuration and workspace evidence â€” 2026-11-01

The approved plan's T1 implements models.py, config.py and workspace.py with
dataclasses/value types, strict project-owned JSON, URI containment and bounded
byte snapshots/manifests. No semantic tool, process owner or write operation is
implemented by this task. See [settings contract](../configuration.md).

Observed negative controls: eight workspace assertion failures before modules
existed; later invalid state-directory/overflow-timeout failures, canonical URI
spelling failure and a byte-exact subprocess-decoding failure were reproduced
before their corresponding fixes. The configuration suite was written before the
loader but its separate first run was green; the observed initial negative control
was the workspace suite's missing configuration/workspace behavior. This is retained
rather than relabeled as an independently observed red for every config assertion.

Observed on managed CPython 3.14.10 / uv 0.13.6, Windows x86_64:

- Seven configuration tests and eight workspace tests pass; no skips occurred.
  Symlink creation/denial was exercised on this host.
- UTF-16/non-BMP offsets, CR/LF/CRLF/vertical-tab/EOF bytes, percent aliases,
  invalid/local/external URI cases, same-name prefix sibling rejection,
  source hashes, excluded directories and unchanged-mtime byte edits are asserted.
- Windows mutation enablement returns UNSUPPORTED; settings load creates no files,
  process or implicit authority. Unknown/duplicate/nonfinite/coerced values fail.
- The changed distribution helper now decodes child diagnostics explicitly as
  UTF-8 with replacement, after a failed byte-exact regression. All ten distribution
  tests and three existing SDK probes pass.
- The separate C901 check against src passes ceiling 20. Qualified cognitive
  acceptance remains unavailable; this is not a cognitive PASS.
- The cross-platform skill's deterministic audit scoped to src/tests/tools returns
  [] after the subprocess-decoding fix. Its initial --path file argument was
  corrected to directory scope, without changing project configuration.
- The four routine hooks pass. Source-independent build and outside-source isolated artifact checks also pass.

Config's schema details fill implementation choices left by the specification:
optional read-only state, explicit nested mutations authority, literal exclusions,
fixed timeout defaults and positive integer limits. Operator authority is validated
without enabling unsupported Windows writes. Snapshots preserve input URIs; checked
physical paths supply canonical aliases.

No POSIX, real-ty, concurrency-generation or Codex semantic result is claimed.
T4 must reconcile scanned source scope with actual ty configuration and demonstrate
generation/readiness behavior. T8/T9 retain filesystem/recovery proof. Native scope
FAIL and cognitive qualification UNKNOWN remain unchanged.
