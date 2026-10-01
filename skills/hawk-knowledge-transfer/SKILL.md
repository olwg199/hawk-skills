---
name: hawk-knowledge-transfer
description: >-
  Create or refresh human-readable project documentation in docs/ from verified
  code and existing records, and maintain shared Codex and Claude Code
  instructions. Use when the user requests knowledge transfer, documentation
  organization, or a project handoff. Do not use for ordinary build work or a
  read-only code review.
---

# Hawk Knowledge Transfer

Turn verified project knowledge into concise documentation people can navigate
and either coding agent can use. Invocation authorizes documentation and project
instruction edits within the requested scope; it does not authorize production
code changes, tests, installation, user settings, commits, or external actions.

## Scope and discovery

Use the requested area, recent task, or supplied records as the default scope.
Document the whole project only when requested. Ask one targeted question if no
scope can be resolved. Follow the user's preferred structure, tone, and detail;
otherwise reuse the existing docs layout and write short explanations with
concrete paths, commands, ownership, and reasons.

Read applicable root and directory-local `AGENTS.md`, `AGENTS.override.md`,
`CLAUDE.md` and explicitly linked instructions before editing. Read `CODEX.md`
only if present; its absence requires no action.
Inspect existing docs and relevant indexes under `docs/generated/`, then inspect
current source and configuration for each material claim. Use legacy `.codex/`
memory and `.build/` records only when the new location lacks the needed record.
Records are evidence of past work, not proof of current behavior. Do not load
the full archive or copy chat transcripts, raw logs, secrets, or private reasoning.

Read the shared [instruction layout](references/agent-instruction-layout.md)
and [shared-agent setup](references/shared-agent-setup.md) for every run. Verify
current official OpenAI and Claude Code documentation when a platform-dependent
claim or detected version/configuration could change the result. Keep source
links and the verification date with the compatibility guidance.

## Documentation placement

- Put human explanations under `docs/`, following established names. Use
  `docs/README.md` as the navigation page when none exists; create `docs/` if needed.
- Keep skill-maintained working records under `docs/generated/<skill>/`.
  Preserve their content, IDs, status fields, and purpose. Do not replace build
  records with polished prose or introduce another memory format.
- Use the existing Hawk storage contract when relocating its artifacts:
  `.codex/hawk-build.md` becomes `docs/generated/hawk-build/project.md`;
  `.codex/hawk-build/design/` becomes `docs/generated/hawk-build/design/`;
  `.build/` records and index become `docs/generated/hawk-build/builds/` with
  their filenames unchanged; `.codex/mobile-ui-builder.md` becomes
  `docs/generated/hawk-mobile-ui-builder/project.md`. Other skills keep their
  established filenames inside `docs/generated/<skill>/` unless instructed otherwise.
- If migrating known legacy records, preserve historical facts, repair actual
  navigation links, and leave historical path mentions intact as provenance.
  Inspect destination conflicts before moving; never silently overwrite or
  merge contradictory records. Leave unrelated tool configuration alone.
- Create `docs/generated/README.md` only when using that folder and it is
  missing. Explain that skills maintain these working records, humans may read
  them, and current source and project instructions take precedence.

Update existing pages instead of creating duplicates. Preserve manual prose
and confirmed decisions; correct demonstrated stale facts in scope. Ask only
when conflicting decisions cannot be resolved from source or user instructions.
Do not invent design rationale. Label uncertainty and unfinished implementation.
Use links for details already explained elsewhere. Add diagrams only when they
clarify a cross-file relationship.

## Shared instructions and compatibility

Apply the shared instruction layout rather than inventing separate rules here.
Thin `CLAUDE.md` into a pointer to `AGENTS.md`; turn `AGENTS.md`
into an explicit routing index for rule files under `docs/`. Move existing
substantive instructions into those maintained files before thinning the
entrypoints, preserving scope, host conditions, manual rules, and required commands.
`CODEX.md` is optional: do not create or require it. If present, preserve its
applicable rules while thinning it to an ordinary pointer to `AGENTS.md`.
Update rule documents when verified reusable rules change, and entrypoints only
when their routes change. Preserve directory-specific instructions and keep
factual generated records separate from project policy.

Always create or refresh a **Knowledge and Codex/Claude compatibility** section
in the applicable working-with-agents page, defaulting to
`docs/working-with-agents.md`. Cover actual instruction entrypoints and scoped
rules, docs/generated locations, skill discovery if used, verification commands,
and safe handoff/concurrent-edit ownership. Record verified facts, known gaps,
source links, and date. Do not claim both tools were executed from file inspection
alone. Keep the section short and leave unrelated docs unchanged.

Only the coordinator edits shared docs, generated records, and instruction files.
If independent writers are already active, coordinate ownership before changing
their files; use separate worktrees or exclusive paths for concurrent code work.

## Verify and report

Check relative links, import targets and case, actual command definitions, source
references, and that retained manual rules survived consolidation. Check the
scoped compatibility section against both tools' loading behavior. Do not execute
documented setup commands that mutate the project just to validate their text.
If host execution is unavailable, distinguish static checks from runtime proof.

Report changed doc paths and a short **Knowledge and Codex/Claude compatibility**
status: `passed`, `blocked`, or `not verified`. List concrete unresolved gaps and
the next repair, with supporting paths. Blockers must prevent a ready-to-commit
conclusion. Do not run a separate review, commit, or install a Git hook automatically.
