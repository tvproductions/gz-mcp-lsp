# Backporting structure into existing projects

Follow the [brownfield first-adoption/upgrade runbook](adoption-0.5.md) for
concrete steps, target candidates, three-way review, rollback and acceptance.

The starter can help an existing project adopt the preferred skills-first shape.
Treat this as a translation of useful responsibilities, not a wholesale rewrite
or an imposed framework. FDAU is the primary precedent; its domain and numeric
quality gates are not defaults for other projects.

Python baseline adoption requires [Astral alignment](engineering/astral-alignment.md),
including `src/` packaging and centralized Python configuration. Adopters should
expect necessary refactoring. Preserve public behavior and project authorities;
record evidenced compatibility exceptions with an owner and revisit condition.
The helper's preservation behavior protects files during configuration and does
not waive required reconciliation.

Record the migration against [Astral acceptance](engineering/astral-acceptance.md),
using the [worked application/library/workspace examples](engineering/astral-migrations.md).
Preserve public behavior and original dependency/source intent. Exact development
sync, source-independent builds and clean installed checks prove different parts
of the result; complete all applicable rows rather than stopping at file moves.

Run `uv run --locked skills-first-starter backport --project /path/to/project`. This assessment reads
only bounded top-level names, does not follow symlinks, and writes nothing. It
suggests responsibilities, not a complete migration plan. The agent must read
the target's governing instructions and relevant source before recommending moves.

Record a concrete mapping in the project's existing planning location:

| Existing source | Intended responsibility/location | Disposition | Verification |
| --- | --- | --- | --- |
| Existing agent guide | Short entry linking maintained authorities | Keep or split with links preserved | Instructions resolve correctly |
| Operational skill and helper | Project-owned workflow plus deterministic code | Keep location unless a move adds value | Real operation or representative fixture |
| Architecture and decisions | Project governing documentation, often docs/project | Link or consolidate without changing authority | References and status remain accurate |
| Term/case inputs and products | Existing separate data/evidence storage | Preserve | Saved records and generation reconcile |
| Backlog and handoffs | Current project authority | Preserve while SP-BP is deferred | Current workflow continues |

Choose each move for a demonstrated benefit. Do not create empty constitutions,
PRDs, ADR folders or ports just to match a diagram. Do not translate a candidate
heavy-profile design into binding governance without an explicit project choice.
Preserve stable identifiers, history, user changes, and source precedence.

For authorized refactoring, work in small reversible steps. Update imports,
packaging, links, native skill discovery and verification commands affected by a
move. Verify behavior at the project's real seams before proceeding. Shared
plugins remain separately pinned; never copy their trees into project skills.

`configure` independently previews/applies the bundle configuration and the
adopter instructions fragment. Version 0.6 also seeds the single native
template-update skill; it does not copy upstream skills or perform structural moves. Existing
managed files from an earlier starter revision require a reviewed update diff;
there is no force overwrite. A structural pilot and fresh-session discovery
remain necessary before claiming adoption is verified.
