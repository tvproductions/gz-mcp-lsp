# T5 exact navigation and complete declaration source — 2026-11-01

The approved definition, references and hover production paths are implemented.
Installed SDK stdio → adapter → actual pinned ty assertions pass locally; this
is development evidence for P1/P2/P4/S1/S5, not full platform/native-host acceptance.
CPython 3.14.10, uv 0.13.6, MCP SDK 2.3.0 and ty 0.0.95 remain unchanged.

## Independent fixture and observed semantics

tests/fixtures/semantic_workspace/navigation_expected.json independently lists
three consumers, their exact import/call positions, a same-name unrelated decoy,
the shared declaration, source bodies and Unicode coordinate controls.
No expected location is derived from the server being tested.

- Direct ty and installed MCP agree on all three calls. With includeDeclaration
  false, only calls are returned. True includes the three independently listed
  import declarations and the original function declaration. The initial fixture
  assertion incorrectly included imports with false; actual ty exposed that
  expectation error. It was corrected without rewriting the expected site list.
- Caller coordinates are forwarded unchanged, including a one-line def identifier
  at line 0/character 4. No +4 or declaration-start substitution occurs.
  A real def-keyword control returns no locations.
- LocationLink origin/full/selection ranges remain distinct. The shared function
  target carries its identifier selection; complete source includes its decorator,
  multiline signature, docstring and body. Raw LSP location ranges are retained;
  extracted declaration full/selection bounds are separately identified in source.
- Supported class, decorated nested async and multiline constant fixtures return
  complete saved source. AST UTF-8 columns are independently mapped to UTF-16.
  The third consumer has a non-BMP prefix: its call begins at UTF-16 character 18,
  and a query at character 20 resolves the correct declaration. Character 14
  splits a surrogate and is rejected before a semantic request.
- Empty hover and definition results remain successful null/empty values. All
  legal original hover forms are preserved without parsing server text into a
  guessed machine type. Malformed content/ranges fail PROTOCOL_ERROR.
- Changing the unopened library body restarts the generation and returns the new
  saved source. The declaration/extraction work remains inside that generation.

## Boundaries and negative controls

Four declaration assertions failed before source_text.py existed. Definition/
reference method assertions and the three-tool SDK catalog failed before their
production implementations. Malformed hover content, aggregate source budgeting,
external context-free metadata, malformed raw names and incomplete-syntax
completeness each exposed a failing regression before correction.

Document source attachments borrow the existing generation lease through
Documents.document(); they do not consume a second admission slot. Source
snapshot IO retains its owner through cancellation. Only URI/hash/version
provenance is retained after each target; source attachments are budgeted
incrementally before materializing an oversized full set. Overflow returns
RESULT_LIMIT, never partial successful navigation.

Local source is read only after containment validation. External/nonlocal targets
remain marked metadata and receive no source or document-symbol request. Unknown
source bounds return unavailable; known server bounds for incomplete syntax
preserve text/ranges but explicitly report syntax_incomplete and complete=false.
Symbol/AST ranges never become input positions for another semantic query.

The official SDK registers exactly the three implemented read tools at this
stage. Raw middleware rejects invalid bool/string/float/extra fields and invalid
context/declaration options before coercion; malformed MCP envelopes remain SDK
validation's responsibility. Domain and unexpected operation failures return
source-free structured errors and matching JSON text. Cancellation propagates.

The shared integration setup builds a wheel, exports the exact runtime lock and
installs into an outside-checkout environment before any MCP call. Every installed
invocation uses Python -I and a cwd outside the source checkout.

Both full Windows/Linux gates pass, including all 93 discovered tests;
C901 src and the scoped portability audit pass. The [source/fixture/artifact
hash receipt](2026-11-01-navigation.json) identifies these inputs. The final local
task commit is recorded in the execution receipt/task ledger. macOS arm64 and hosted CI remain UNKNOWN. Actual Codex
definition/references and the full nine-tool/mutation H1-H3 proof remain T11.
