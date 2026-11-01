# Application settings

Application settings are project-owned JSON with no environment-variable overrides.
The stdio CLI supervises one ty process. Native Codex TOML remains a separate format.

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
creates no state, launches no process and writes no source. The runtime's T8/T9
transaction and startup-recovery evidence is recorded separately.

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
for its dated evidence; current platform conclusions require exact-commit CI.


## Symbol and implementation requests

`document_symbols(uri)` returns result.symbols with hierarchy, full range and
selection_range. Flat server symbols retain selection_range=null. Names, kinds,
detail, containers and server data remain available; duplicates are preserved.

`workspace_symbols(query, resolve=false)` searches without opening a synthetic
document. URI-only results retain range=null and selection_range=null. Explicit
resolve=true requires advertised server resolution; a returned location range
still does not imply an identifier selection. Search, resolution, normalization
and final workspace validation share one generation lease. Changed workspaces
return STALE_DOCUMENT rather than old-generation symbols.

`implementations(uri, position)` forwards exact UTF-16 positions and returns
result.locations with separate full/selection ranges where supplied by ty.
Pinned ty includes the queried declaration with its subclass/member overrides.
Empty results are successful; absent advertised capability returns UNSUPPORTED.
External targets remain marked metadata without external source reads.
See [T10 evidence](evidence/2026-11-01-symbols.md).

## Mutation requests

The catalog includes definition, references, diagnostics, hover, rename_symbol
and edit_file, plus document_symbols, workspace_symbols and implementations.
Both mutation tools remain destructive in their MCP annotations,
including preview requests. They require enabled operator authority even for
preview. Model-supplied approval flags are rejected.

Use action=preview with these exact fields:

- rename_symbol: uri, position and new_name.
- edit_file: uri, expected_hash and edits, where each edit has range and new_text.
  Ranges address the original saved file; an empty new_text deletes, a zero-width
  range inserts, and an explicit EOF range appends.

Apply uses only action=apply and plan_id, with no preview fields. Successes use
the common schema_version/operation/position_encoding/result/workspace_generation/
documents/complete envelope. Preview metadata is under result: read result.plan_id
for apply, with affected files, base/post hashes, diffs, annotations and expiry. A plan
token identifies content; it does not authenticate human approval. Configure
native host approval policies separately. Apply never silently replans a stale
preview. Restart expires in-memory previews but preserves durable receipts.

For enabled writes, recovery runs before mutation admission. The private state
directory and sources must share a verified durable local filesystem. Linux
x86_64 and macOS arm64 are supported; Windows writes remain unsupported.
A quiescent workspace is required. Changes are recoverable, without a cross-file
atomicity promise. External writer conflicts require operator recovery.

Apply returns the disk receipt in result and semantic_state separately. A
committed receipt remains committed even if semantic_state is unavailable;
the old semantic transport is invalidated. Retrying the same plan retrieves its
receipt before expiry/session checks. Receipts are retained for explicit operator
acknowledgment/cleanup; quota exhaustion rejects new writes. Disabled startup
never restores source merely because recovery files exist.
