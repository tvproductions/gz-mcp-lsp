# Project skill deduplication — 2026-11-11

The user requested fixing duplicate gz-skills discovery. The project enabled
gz-skills@skills-first-starter while user configuration also enabled
gz-skills@gz-skills. Add only a project enabled=false override for the latter.
Preserve user settings, native caches, component pins and disabled Backplane.

Observed using codex-cli 0.167.1 with fresh, read-only app-server initialize and
skills/list requests (explicit cwd and forceReload=true), without model turns:

| Probe | Enabled gz-skills entries | Duplicate names | Sources |
| --- | --- | --- | --- |
| Project before | 40 | 20 | starter 0.10.1 and standalone 0.8.3 |
| Project after persisted exclusion | 20 | 0 | starter 0.10.1 only |
| Outside project before and after | 20 | 0 | standalone 0.8.3 only |

All probes report zero discovery errors. The user configuration SHA-256 is
unchanged. A command-scoped exclusion did not affect skills/list; the persisted
project exclusion did. No installation, uninstallation, cache editing or user-wide
disable was performed. Raw probe results remain outside the repository.

The already running conversation retains its previously injected skill catalog;
fresh discovery demonstrates the corrected configuration. Use a fresh session
to start with the deduplicated catalog.

This closes project duplication, not E4 or complete native acceptance. The
starter-managed cache is 0.10.1 while the project component record selects 0.8.3;
source/version reconciliation remains open. Global discovery outside the project
is the user's existing default and remains unchanged. No runtime source, tests,
dependency locks, plugin pins or release state changed.
