# Reconcile an adopter with the zero-skill template

Template 0.3.0 changes the adoption contract. It stops installing `skills-first-start` and moves starter-authored
adoption and Python guidance into ordinary documentation. SP, SP-BP and gz-skills
remain independent components. SP/SP-BP pins and activation policy are retained;
gz-skills advances to released v0.7.0 while Python/tool requirements remain binding.

There is no automatic migration or force overwrite. Configure refuses legacy
starter skill names in `.agents/skills`, `.codex/skills`, `.claude/skills` and
`.github/skills` before writing; it does not delete them. A name collision is a
review requirement, not proof that a project-owned skill is disposable.

1. Record the previous template version/SHA, lock, configuration, loaded sources
   and local changes. Retain recovery copies outside active skill discovery.
2. Read the desired reviewed starter revision's changelog and
   [structure contract](structure.md). Compare copied starter material with its
   original revision, preserving project edits and authorities.
3. Replace references to `skills-first-start` with direct routing in project
   instructions. Use SP for feature work, gz-skills for engineering and generic
   maintenance, and project-owned skills for application operations. Move any
   useful project-specific routing into project instructions.
4. Preserve the adoption and Python guidance using the new locations below.
   Link the reviewed checkout at the recorded revision, or maintain reviewed
   project-owned documentation with source provenance. Do not link a copied
   fragment's paths as though they were relative to the adopting repository.
5. After comparing content and preserving local changes, retire obsolete
   starter-owned skill copies from active discovery within the authorized
   project migration. If a name now identifies a real project-owned workflow,
   review its identity and routing rather than discarding it. Upstream plugin
   skills and other application skills retain their owners and discovery paths.
6. Reconcile the managed lock, marketplace ref and instructions together against
   the desired reviewed starter. Preview configure, review its concrete diff and
   apply only within the authorized upgrade. Different managed records still
   block writes until reconciled. Preserve app dependencies, settings and profiles.
7. Run the project's required checks and verify upstream skill loading in a fresh
   host session. File validation cannot prove removal from host caches or actual
   discovery. Record the results and any remaining gaps in existing project
   decisions/handoff material.

| Previous location | Current location |
| --- | --- |
| `skills/skills-first-start/SKILL.md` | Routing in `AGENTS.skills-first.md`, with ownership in `docs/structure.md` |
| `skills/adopt-skills-stack/SKILL.md` | `docs/adoption-workflow.md` |
| `skills/python-engineering/SKILL.md` | `docs/engineering/python.md` |
| `skills/python-engineering/references/` | `docs/engineering/` |
| `skills/python-engineering/scripts/` | `tools/engineering/` |

The analysis scripts keep their existing counting contract. Relocation does not
establish a new clean complexity baseline; historical receipts and source hashes
remain evidence of the original paths/revisions. On-demand analysis remains
outside routine hooks and CI. No plugin installation, SP-BP activation, profile
setup, automatic schedule or release publication follows from this migration.
