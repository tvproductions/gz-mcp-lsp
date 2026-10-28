# Cosmic Ray compatibility — October 18, 2026

Scope: the user authorized publishing v0.4.0 first, then completing the next
repository-local task: a bounded Cosmic Ray Python 3.14 compatibility proof.
The `gzs-update-dependencies` v0.8.0 workflow supplied scoped dependency selection;
the starter's Python policy overrides upstream profile defaults. Profile
inspection found no settings; none were initialized or inferred.

## Release preceding this work

[v0.4.0](https://github.com/tvproductions/gz-skills-first-starter/releases/tag/v0.4.0)
was published as a non-draft, non-prerelease GitHub release. Its annotated tag
object is `5ca6c18d5477be5f634edd00789983e0f3bdf326`, peeling to release commit
`b6f76dd75b4e6e779d6364cce0ff65bd73fda93a`. Remote tag resolution was verified.
The full locked local gate and twelve explicit analyzer tests passed before
tagging; [Ubuntu CI](https://github.com/tvproductions/gz-skills-first-starter/actions/runs/39138782659)
passed on that exact commit. No package registry upload or plugin installation
was performed. This later work starts an unreleased 0.4.1 patch; published
metadata and tags are preserved.

## Inventory, selection and resource cost

Update mode, limited to the already-selected Cosmic Ray tool and its necessary
transitive dependencies. The project is pure Python, with `pyproject.toml` and
`uv.lock`, managed Python 3.14.8 and uv 0.13.1. Official registry/API checks on
October 18 confirmed the newest stable Python 3.14 patch remains 3.14.8 and uv's
selected 0.13.x family remains 0.13.1. The running interpreter is Windows CPython
3.14.8, matching `.python-version`, package bounds, Ruff/ty and CI targets.

| Surface | Before | Decision |
| --- | --- | --- |
| Cosmic Ray | Selected by policy, absent from environment/lock | Select 8.x family; pin newest published, non-yanked, non-prerelease 8.7.0 in `hygiene` after the isolated proof |
| Transitive requirements | Absent except overlapping existing packages | Resolve through uv, retain exact versions/hashes in `uv.lock`; 43 third-party packages in the complete locked environment |
| Runtime/package manager | Python 3.14.8, uv 0.13.1 | Retain verified current selections within their approved families |
| Other dev/hygiene tools, uv_build, CI actions and routine hooks | Existing reviewed exact pins | Outside this scoped tool addition; preserve all selections and four-hook gate |
| Template and plugin catalogs | Published starter 0.4.0; SP 7.0.0, deferred SP-BP, gz-skills 0.8.0 at full SHAs | Develop 0.4.1 without publishing it; regenerate wheel bundle resource, preserve component pins/defaults and both native catalogs |
| Other selected deeper tools / adopter cohesion | Existing open compatibility work | Outside this proof; no installation or compatibility claim |

Cosmic Ray is a development-only mutation engine. Its 14 direct requirements
include HTTP/distribution, SQLAlchemy session storage, Git/reporting and parser
libraries. They add download, cache, environment and lockfile weight, with no
application runtime dependency. The proof selects the local distributor; it
starts no service, HTTP worker or remote execution. Databases and source copies
exist only in a context-managed disposable directory; only the requested JSON
receipt persists. Full resolved versions/hashes belong to the lock, not a
separately maintained requirements list.

[PyPI metadata](https://pypi.org/pypi/cosmic-ray/json) reports 8.7.0, Python
`>=3.9`, beta development maturity and Python classifiers only through 3.13.
The [8.7.0 release notes](https://github.com/sixty-north/cosmic-ray/releases/tag/release/v8.7.0)
describe a release-artifact version fix, not a Python 3.14 certification. The
absence of a 3.14 classifier prompted direct testing rather than an inferred
support claim. Retain the beta-maturity/limited-platform caveat. The starter
maintainer owns revisiting it and the baseline limitation below at the next
scoped maintenance, new selected-family release or upstream fix.

## Execution and reliable interpretation

The [final checked receipt](2026-10-18-cosmic-ray-compatibility-final.json) records the probe
hash, exact runtime/tool version, fixture contents, command exits, structured
mutation results and readable diffs. The explicit
[probe](../../tools/engineering/evaluate_cosmic_ray.py) mutates only an invented
standalone module. One unittest checks `checked() == 1234`; `unchecked()` returns
4321 and is deliberately untested to supply meaningful surviving mutants.
The [first locked receipt](2026-10-18-cosmic-ray-compatibility.json) is preserved;
the final probe strengthens restoration verification to compare exact bytes.

| Control / execution | CLI exit | Stored interpretation |
| --- | --- | --- |
| Direct unmodified unittest, before/after | 0 | One passing test each time |
| Passing Cosmic Ray baseline | 0 | Normal worker, survived test; required before mutations |
| Deliberately failing unittest baseline | 1 | Genuine killed result |
| Two-second sleep with 0.1-second timeout | 1 | Timeout, kept separate from genuine kills |
| Nonexistent test executable baseline | **0** | Normal worker, **incompetent** test: tool error, never a passing baseline |
| Mutation init / exec / dump / report | 0 | Four complete normal results: two killed, two survived; no pending/error/timeout results |

The zero exit for the launch-error baseline was reproduced both before pinning
in a disposable environment and in the final locked environment. Installed
8.7.0 `cli.py` checks only `KILLED` before treating a baseline as passed, while
`testing.py` returns `INCOMPETENT` for a launch exception. The released source
at [the publishing commit](https://github.com/sixty-north/cosmic-ray/tree/caf9a3193606ddd90cc37126b7fa95acefc47695/src/cosmic_ray)
provides the corresponding implementation. `exec`/`cr-report` success also does
not establish mutation quality or complete valid results. The probe inspects
`dump` output and rejects pending, abnormal or incompetent mutation outcomes;
timeouts are separately classified. Its deliberately invalid controls confirm
these distinctions before the valid mutation session proceeds.

Reviewed diffs: 1234 becomes 1235 or 1233 and both mutants are killed. The
untested return 4321 becomes 4322 or 4320 and both survive. These are observable
output changes, not equivalent mutants. The synthetic gap is intentional; no
application tests/code are changed to manufacture a mutation percentage. Source
restoration and the post-run baseline are verified. There is no score gate.

The proof bounds subprocess work to 120 seconds, individual CLI invocations to
at most 30 seconds and normal test runs to five seconds. It uses UTF-8, argument
sequences without a shell, the current pinned interpreter and explicit session
files. Cosmic Ray parses its test-command string with `shlex.split`, so the
probe quotes a POSIX-form interpreter path with `shlex.join`. Source and database
handles close before disposable-directory cleanup. Receipt paths are exclusive
and existing evidence is never overwritten. No operational records are read.

## Commands and verification

Initial selection used a disposable `uv venv --python 3.14.8` followed by
`uv pip install --python ENV_PYTHON cosmic-ray==8.7.0`; the probe passed there
before `uv add --group hygiene cosmic-ray==8.7.0`. Resolution and synchronization
were performed by uv, without hand-editing `uv.lock`.

Reproduce from the reviewed checkout, choosing a fresh output filename:

```bash
uv run --locked --group hygiene python tools/engineering/evaluate_cosmic_ray.py --output REPORT.json
```

Observed on Windows/Python 3.14.8: the locked probe passes with two killed/two
surviving mutants and all four baseline controls. The routine four-hook gate,
35 adoption tests, twelve explicit analyzer tests, bundle/both catalogs, locked
sync/lock check, sdist/wheel build and isolated installed CLI checks pass.
Static portability checks report zero findings. Explicit Ruff C901 and
complexipy checks pass on the new probe (maximum cognitive score 6); the full
`src tests tools` Lizard check passes with 105 functions, maximum 16, zero
violations/errors. No threshold or measurement contract changes.

Available supplementary maintenance queries: `uv pip list --outdated --format
json` reports only Ruff 0.17.1 beyond the approved 0.15.x family, deferred as
already reviewed. `uv audit --locked --output-format json` reports 43 audited
packages, zero known vulnerabilities/adverse statuses. Its experimental command
and schema do not replace the selected pip-audit proof, which remains open.
No full-stack freshness or vulnerability-free claim follows from these queries.

Python 3.14 opportunity review: the actual interpreter/subprocess/parser path
is the benefit being established over unverified 3.13-only metadata. No runtime
annotation introspection is needed, so defer `annotationlib`; bounded executor
submission, subinterpreters, Zstandard and structured templates add no value to
this serial fixture. Retain context-managed temporary files and exclusive
receipt creation; `Path.copy/move` would add no benefit to generating disposable
source. The [versioned porting notes](https://docs.python.org/3.14/whatsnew/3.14.html)
were reviewed; the probe launches subprocesses, not multiprocessing workers, and
claims no free-threaded/JIT or multiprocessing start-method compatibility.

This is a bounded ordinary-syntax/unittest/local-distributor proof on Windows,
not exhaustive Python 3.14 grammar, descendant-process timeout cleanup, HTTP
distribution, macOS/Linux mutation execution or adopter-code certification.
Neither routine CI nor static portability review establishes those results.
Shared/local analysis-utility ownership and other selected deeper-tool proofs
remain open. Mutation testing stays outside hooks and CI; no upstream plugin,
profile, native manager or adopter repository is changed.
