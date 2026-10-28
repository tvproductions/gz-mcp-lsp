# Starter tooling freshness review — October 24, 2026

Result: **STALE**. Pinning made the 0.6.0 release reproducible; it did not make
its toolchain current. This read-only review checks actual official releases.
New-version compatibility is untested. No package, pin, lock, interpreter,
CI action, native plugin or cache was updated. The machine's global uv is also
outside this project's upgrade scope.

The [structured receipt](2026-10-24-tooling-freshness.json) records source URLs,
upload/publication dates, actual project input hashes, and the baseline commit.
The active skill catalog did not supply gzs-update-dependencies, so this review
used the existing documented direct-source fallback. No reusable competing
maintenance script or scheduler was added.

| Scope | Current pin | Latest within selected family | Finding |
| --- | --- | --- | --- |
| Python 3.14.x | 3.14.8 | 3.14.9 | STALE; expedited security release |
| uv 0.13.x | 0.13.1 | 0.13.5 | STALE; includes certificate-store/managed-Python security updates |
| uv_build 0.13.x | 0.13.1 | 0.13.5 | STALE |
| Ruff 0.15.x | 0.15.22 | 0.15.22 | Current in selected family; upstream 0.17.2 requires separate family review |
| ty 0.0.x | 0.0.89 | 0.0.91 | STALE; existing beta exception remains |
| pre-commit 4.x | 4.7.0 | 4.7.0 | Current in selected family |
| complexipy 8.x | 8.0.1 | 8.1.0 | STALE; analyzer compatibility checks required |
| Cosmic Ray 8.x | 8.7.0 | 8.7.0 | Current in selected family |
| Lizard 1.24.x | 1.24.1 | 1.24.3 | STALE; checker explicitly binds 1.24.1, so revalidate its counting contract before changing that requirement |

Primary evidence: [Python 3.14.9](https://www.python.org/downloads/release/python-3149/),
[uv 0.13.5](https://github.com/astral-sh/uv/releases/tag/0.13.5), and the
per-package official PyPI JSON sources retained in the structured receipt.
These are release observations, not tested upgrade recommendations disguised
as completed work.

## CI and independent plugin sources

- actions/checkout v7.0.1 is the latest release; its resolved tag matches the
  current immutable CI pin.
- setup-uv is pinned to v9.0.0, the latest observed release in major 9. Latest
  upstream is v10.3.2. Review that action-major change separately; a current pin
  does not itself define a permanent approved support range.
- SP is pinned to v7.0.0; v7.0.1 is published and needs scoped compatibility review.
- gz-skills v0.8.0 remains the latest published release observed.
- Backplane's repository access and release list were verified: no published
  release exists. Current development HEAD differs from its recorded snapshot.
  That is not readiness or activation approval; Backplane stays disabled.

No full transitive dependency freshness or vulnerability audit was performed.
No claim is made that the complete stack is current or compatible with the
new targets. Resolve the stale same-family selections, assess newer families
independently, run changed-tool and repository acceptance, then pin the verified
selections and document retained exceptions. Publish a separately authorized
maintenance release after classification of the actual verified changes.

## Process correction

The local AGENTS change now calls for an explicit read-only freshness review
before each starter release, in addition to scoped/quarterly maintenance, with a
linked dated receipt. Those instruction edits and the greenfield/brownfield
clarifications remain uncommitted/unreleased at this review point. Passing the
existing helper tests neither enforces the full adoption contract nor proves
freshness. No future release should describe unreviewed retained pins as current.
