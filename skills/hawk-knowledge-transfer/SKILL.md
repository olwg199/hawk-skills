---
name: hawk-knowledge-transfer
description: >-
  Create or refresh human-readable project documentation and shared agent
  instructions from verified project evidence. Use only when the user explicitly
  invokes or names hawk-knowledge-transfer, including $hawk-knowledge-transfer
  and /hawk-knowledge-transfer. Do not auto-trigger from ordinary documentation,
  organization, handoff, or build requests when this skill is not requested.
disable-model-invocation: true
---

# Hawk Knowledge Transfer

Work only when this skill is explicitly requested. Update documentation and
project instructions within the requested scope. Explicit skill invocation does
not authorize unrelated instruction restructuring or record migration; migration
needs an explicit request to relocate existing records. Production code, tests,
installation, global settings, commits, and external mutations remain outside
this workflow unless separately requested.

## Scope and evidence

Use the named area, recent task, or supplied records as the scope. Document the
whole project only when requested. Resolve scope from the request and existing
context; ask a targeted question only when it cannot be resolved or a material
conflict changes the work. Follow the user's detail and organization preferences,
otherwise reuse the existing docs layout and write concise explanations.

Read applicable `AGENTS.md`, `AGENTS.override.md`, `CLAUDE.md`, and linked scoped
instructions. Read `CODEX.md` only if present. Inspect relevant existing docs,
indexes, current code, configuration, and verification results. Discover needed
legacy `.codex/` memory and `.build/` records when canonical records are absent.
Past records are evidence of previous work, not proof of current behavior.
Do not load the whole archive or copy transcripts, raw logs, secrets, or private
reasoning into documentation.

Read the shared [instructions and migration specification](references/agent-instruction-layout.md)
for every run. Use project evidence; this skill does not require online platform
research, vendor-documentation claims, or publication/verification dates.

## Documentation and instructions

Keep human explanations under `docs/`, following existing names; use
`docs/README.md` for navigation when none exists and create missing folders when
needed. Update existing pages rather than making duplicates. Preserve manual
material and confirmed decisions; label incomplete implementation and uncertainty,
and do not invent rationale. Correct demonstrated stale facts only within the
requested documentation scope, separately from any record migration.

Keep essential project-wide rules directly in `AGENTS.md`. Share them through
`CLAUDE.md`'s actual `@AGENTS.md` import. Put detailed area-specific guidance in
docs and link it with read conditions. Preserve essential-rule meaning, host
conditions, and directory scope when organizing instructions. `CODEX.md` remains
optional and is neither created nor required.

Support both Codex and Claude as the standard. Create or refresh the Knowledge
and Codex/Claude compatibility section in the relevant working-with-agents page,
defaulting to `docs/working-with-agents.md`. Cover actual startup rules/imports,
scoped docs, knowledge locations, project skill installation if used, verification
commands, and handoff/concurrent-edit ownership. Record project evidence and known
gaps; do not claim either host executed from file inspection alone.

Only the coordinator edits shared docs, instructions, and records. Coordinate
ownership with existing writers. Perform clearly requested edits directly, then
report them for Git review; do not add a mandatory preview or approval step.

## Requested record migration

Apply the shared specification's native-copy and verification procedure only
when record migration is explicitly requested. Copy complete records unchanged,
verify equality, then edit only references, paths, or routing required by the new
structure. Preserve recorded knowledge with the same meaning and level of detail;
knowledge corrections are separate work. Never recreate records from generated
text. Inspect destination conflicts before copying. Follow the Hawk destination
mapping in the specification and repair actual links without rewriting history.

Create `docs/generated/README.md` if the migration uses that folder and its notice
is missing. Explain that skills maintain these working records, humans may read
them, and current source and project instructions take precedence. Keep existing
record formats, IDs, and filenames unless the new structure needs a rename.

## Verify and report

Check local links, imports and case, actual commands/source references, essential
startup-rule preservation, and directory scope. For migration, report the native
copy command, equality result before edits, source/destination paths, and targeted
structural changes. Check the final diff for preserved recorded knowledge.
Do not execute mutating setup commands just to validate their documentation.

Report changed paths and outcomes, migration results when applicable, and
Knowledge and Codex/Claude compatibility as `passed`, `blocked`, or `not verified`.
List concrete unresolved gaps and their repair. Blockers prevent readiness.
Do not run a separate review, install a hook, or commit automatically.
