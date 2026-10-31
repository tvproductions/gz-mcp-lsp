# Product tests

The approved implementation now has distribution, configuration, filesystem
identity, coordinate, JSON-RPC, lifecycle, document, navigation, diagnostics and
pure edit-plan tests. Ordinary unittest discovery includes actual pinned ty and
MCP stdio integration against public synthetic fixtures. Missing ty fails those
tests. No private sources are included.

Mutation transactions/recovery, write-capable MCP tools, the three navigation
extensions and actual Codex host acceptance remain later approved plan tasks.
Passing this intermediate suite does not establish terminal milestone acceptance.
Inherited engineering-tool tests remain in tools/engineering/ and run separately.
