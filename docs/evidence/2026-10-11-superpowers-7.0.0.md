# Superpowers scoped update — October 11, 2026

Mode: update, authorized for SP only. The user selected template patch 0.3.2.
The previous SP pin was v6.4.1 at
`5bf4e78011075bcfc0dc295f0724994cd123ee71`, selected for Backplane's historical
compatibility evidence. No SP 6.x-only support range is declared. Backplane is
disabled, so that evidence does not constrain the active SP selection.

## Target and compatibility review

The official [latest-release API](https://api.github.com/repos/obra/superpowers/releases/latest)
returned [v7.0.0](https://github.com/obra/superpowers/releases/tag/v7.0.0),
published October 10, 2026. Both the tags API and the commit endpoint resolved it
to `bb92a77741419a4ab5f06e711a283343f1ada0c3`.
Adopt this stable release; it is not a development HEAD selection.

Reviewed the release notes, the v6.4.1-to-v7.0.0 comparison, README installation
guidance and the native Codex/Claude manifests at the selected tag. Both native
manifests retain the `superpowers` identity and declare version 7.0.0; Codex
references `./skills/`. The queried legacy `.codex/INSTALL.md` is absent;
the current README and `.codex-plugin/plugin.json` supply native plugin evidence.
No bootstrap or synchronization script was executed.

SP 7 changes brainstorming and related review workflows and fixes several
Windows hook/path behaviors. Adopters should review upstream instructions at the
exact revision. The starter's immutable source catalog format remains suitable;
this metadata inspection does not establish host loading or behavioral acceptance.
SP 7/Backplane compatibility is unverified. Backplane stays disabled pending its
separate readiness and compatibility review.

## Inventory and scope

Updated the canonical bundle and Codex/Claude catalog SHAs together, current
adoption guidance, release notes and template version metadata. Refresh `uv.lock`
through uv for the starter metadata only. The Python manifest/hygiene group,
runtime pin, CI actions/tools, gz-skills and deferred Backplane were inventoried
and classified outside this SP-only upgrade scope. No package/profile
reconciliation, vulnerability audit, installed plugin update or unrelated-project
migration is included. This assessment does not claim the entire stack is current.

Python evidence remains `.python-version` 3.14.8, metadata `>=3.14,<3.15`,
Ruff `py314`, CI 3.14.8 and the existing environment's `version_info = 3.14.8`.
This plugin/documentation update changes no Python code. Annotation introspection,
bounded executors, file/compression APIs and template strings have no consumer
here: defer adding machinery, with no API migration risk introduced by the pin.
The existing helper's actual pinned interpreter must still run required checks.

## Verification

Passed all 28 unittest cases, bundle/both-catalog validation, Ruff 0.15.18
check/format and the offline uv lock consistency check. The executing managed
interpreter reported Python 3.14.8. The lock refresh changed only the starter
version from 0.3.1 to 0.3.2; no dependency resolution changed. Fresh-session skill discovery,
native installation behavior and combined Backplane acceptance remain unverified.
