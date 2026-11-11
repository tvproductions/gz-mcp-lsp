# Minimum-only uv compatibility backport — 2026-11-11

During explicit Git sync, the user identified the repeated exact-uv blocker and
directed prioritizing its correction. Rollback base is product
`05aa14b9885e511f04340e422298d784e8a74174`; the clean local main fast-forwarded
33 remote commits from `922bd62` before this scoped correction.

## Source and adoption decision

Reviewed published starter [v0.9.0](https://github.com/tvproductions/gz-skills-first-starter/releases/tag/v0.9.0),
published November 8, in a separate clean checkout. Tag resolves to
`3f76acf0038b030bf5abd85ce4a419e890d3e420`, matching HEAD and bundle version.
Read its release/changelog, baseline, Python/versioning policy, adoption workflow
and canonical update runbook. The source policy is
[uv executable compatibility](https://github.com/tvproductions/gz-skills-first-starter/blob/3f76acf0038b030bf5abd85ce4a419e890d3e420/docs/baseline-policy.md#uv-executable-compatibility),
introduced by `f0f5428c3f9146c4caaab209822b1f5d5fd57daa`.

Backport only minimum-only uv compatibility. This product selects >=0.13.6,
retaining its verified floor rather than adopting the starter's lower 0.13.5.
CI keeps tested uv 0.13.6. Record actual callers and nested-hook provenance;
admission of future uv versions does not certify their behavior or freshness.
Preserve Python 3.14.10, uv_build 0.13.6, uv.lock, all dependency/plugin pins,
native defaults and disabled Backplane. No application/runtime code changes.

Starter provenance remains v0.7.1 at
`27594dbaec853e6bde037b0aaf3f0427a3f053f9`. This backport is not a complete
v0.9.0 migration; unrelated helper/platform/release-policy updates are deferred.
The unpublished product stays 0.1.0; no tag or release is authorized. Current
project policy/fragment/README/handoff supersede inherited exact-uv instructions;
historical receipts remain historical. Initialization links this correction.

## Causal controls and verification

The November 9 [Dependabot failure](https://github.com/tvproductions/gz-mcp-lsp/actions/runs/42641967556)
reports detected requirement ==0.13.6 versus updater-supported 0.13.7.
Actual local uv 0.13.7 `lock --check` fails before editing with exit 2 and the
same exact-version mismatch. After editing, that binary passes `lock --check`;
uv 0.13.5 still rejects the >=0.13.6 floor with exit 2. No lock regeneration is
needed for this executable constraint. Tool invocations use
`uv tool run --from uv==VERSION uv ...`, without changing user-wide uv.

The initial uv 0.13.6 run completed 186 unittest cases (one Windows-only skip)
but pre-commit correctly returned nonzero because this correction was edited
during its run. It is not counted as a passing final gate. Before the correction,
source-independent build and outside-source distribution verification passed.
Final uv 0.13.7 verification passed on managed CPython 3.14.10 / macOS arm64:

- `uv lock --check` and `uv sync --locked --all-groups`.
- `uv run --locked pre-commit run --all-files`: all four hooks passed.
- `uv build --no-sources`: sdist and wheel built.
- `uv run --locked python tools/verify_distribution.py`: archive identity and
  isolated installed import/CLI checks passed outside the checkout.
- Nested `uv run` resolves the actual 0.13.7 tool environment executable, not the
  user's default 0.13.6 binary. Python stays managed 3.14.10.
- `git diff --check` passed; lock, interpreter, CI and starter-provenance files
  have no diff. No analyzer/test implementation changed, so separate inherited
  utility/deeper analyzer reruns are outside this compatibility correction.

Normal commit hooks and final Git/CI observations are reported in the sync response.

The baseline commit's [three-platform CI](https://github.com/tvproductions/gz-mcp-lsp/actions/runs/41358262222)
passed Linux x86_64, macOS arm64 and Windows AMD64. The backport requires its own
exact-commit CI. Hosted Dependabot scanning must be observed on corrected
default-branch inputs before claiming the hosted service repaired. Existing
T12/T13 engineering/cognitive/native-discovery gaps remain separate and open.

Rollback restores the reviewed files from the base commit, reinstating its
exact-uv restriction; it needs no history rewrite, cache changes or plugin action.
