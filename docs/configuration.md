# Application settings

T1 implements the JSON loader and workspace primitives; T3 adds the stdio CLI and
single-child lifecycle. The intermediate catalog remains empty until T4 adds hover. Application settings
have no environment-variable overrides. Native Codex TOML remains a separate format.

Required keys:

| Key | Value |
| --- | --- |
| schema_version | Integer 1 |
| workspace_root | Absolute existing local workspace directory, resolved once |
| ty_executable | Absolute existing preinstalled executable path; T3 verifies LSP startup |

Optional keys:

| Key | Default / rule |
| --- | --- |
| request_timeout_seconds | 20; positive finite number |
| initialize_timeout_seconds | 20; positive finite number |
| shutdown_timeout_seconds | 3; positive finite number |
| kill_timeout_seconds | 2; positive finite number |
| mutations | Object with enabled=false and writable_roots=[] |
| state_directory | Absent; explicit absolute private directory outside source is required for enabled writes |
| exclusions | Empty list of literal relative directory/file prefixes; no glob syntax |
| project_config_files | ["pyproject.toml", "ty.toml"]; literal relative paths |
| limits | Object overriding positive-integer ceilings below |

Unknown or duplicate keys, bool-as-integer values, nonfinite numbers and escaping
scope paths are rejected. Settings input is bounded to 64 KiB. Enabling mutations
requires explicit contained existing writable directories and state storage;
Windows and other unsupported write platforms return UNSUPPORTED. This loader
creates no state, launches no process and writes no source. T8/T9 must separately
prove guarded application and startup recovery on supported POSIX systems.

| limits key | Default |
| --- | --- |
| header_bytes | 4096 |
| frame_bytes | 16777216 |
| file_bytes | 2097152 |
| workspace_bytes | 67108864 |
| workspace_files | 10000 |
| result_bytes | 1048576 |
| in_flight_reads | 8 |
| mutation_files | 100 |
| mutation_edits | 1000 |
| staged_bytes | 8388608 |
| retained_state_bytes | 268435456 |
| retained_plans | 32 |
| plan_ttl_seconds | 600 |

Operator increases need explicit configuration and acceptance evidence; a larger
number alone does not prove safe capacity. Scans also bound pending directories by
workspace_files and check the request-time budget during traversal.

Workspace manifests include .py/.pyi and selected project configuration bytes and
file identities, including unopened files. VCS/internal state, dependency environments,
node_modules, __pycache__ and execution scratch are excluded. Additional configured
exclusions are literal workspace-relative prefixes. Nonexcluded symlink/reparse
entries fail rather than silently becoming fresh source scope. Source reads require
local file URIs with empty authority, contain no query/fragment/traversal/NUL, and
decode percent escapes exactly once. Source must be regular UTF-8 text.

Positions count zero-based UTF-16 code units; ranges are end-exclusive. Invalid
offsets and surrogate splits fail rather than clamp. Snapshots retain original
URI and exact UTF-8/newline bytes. Canonical URI identity uses checked resolved
filesystem spelling rather than blanket lowercasing.

T4 implements production hover and conservative session freshness. Nested project
configuration and ignore files are tracked. Unsupported external ty configuration,
custom typeshed, escaping roots/patterns, untracked baselines and custom adapter
exclusions fail closed until their indexing scope can be reconciled. Provisioned
dependency environments must remain immutable during a session. ty runs in
untrusted mode with uv integration disabled. No environment variable overrides
product settings; native ty configuration locations are checked only to reject
untracked configuration. See [T4 evidence](evidence/2026-11-01-documents-hover.md)
for local Windows/Linux verification and remaining macOS/hosted-CI gaps.
