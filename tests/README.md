# Product tests

The ordinary unittest suite covers configuration, workspace identity/UTF-16
coordinates, framing, lifecycle, saved generations, all nine tools, mutation
planning/transactions/recovery and the official SDK boundary. Integration tests
provision pinned ty before requests and install runtime-only wheels outside the
checkout. The acceptance workspace has shared_runtime/run_shared_cli, three
importing packages and independent expected coordinates. POSIX write tests have
explicit Windows exclusions; Windows disabled/unsupported mutation denials run.
These SDK tests do not substitute for native Codex approval/denial transcripts.
Inherited engineering-tool tests live in `tools/engineering/` and run separately.
