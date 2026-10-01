# Working with Codex and Claude Code

Use both tools with the same essential project instructions. Keep concise,
always-applicable rules directly in [AGENTS.md](../AGENTS.md), shared through
[CLAUDE.md](../CLAUDE.md)'s actual `@AGENTS.md` import. Detailed area-specific
procedures live under `docs/`, with read conditions in `AGENTS.md`.
The [shared specification](agent-instruction-layout.md) governs this layout
and record migration. `CODEX.md` is optional and is not required here.

## Knowledge and Codex/Claude compatibility

- **Startup rules:** important permissions, deployment boundaries, and critical
  conventions stay directly in `AGENTS.md`. Do not replace them with an instruction
  to open a docs file later. Keep the Claude import working and preserve scoped
  overrides and host-specific conditions.
- **Area guidance:** read [authoring conventions](project-rules.md) for skill and
  README changes. Link other focused procedures with explicit read conditions.
  On-demand docs are useful context; they do not substitute for essential rules.
- **Knowledge:** human explanations live in `docs/`; new working records use
  `docs/generated/<skill>/`. Existing legacy records remain discoverable and
  active until a requested migration. Do not create competing copies by accident.
- **Skill usage:** source lives under `skills/hawk-*/`. Use this repository's
  installer on each machine. Knowledge Transfer is explicit-only: invoke
  `$hawk-knowledge-transfer` in Codex or `/hawk-knowledge-transfer` in Claude.
- **Handoff:** keep task status, verification, unresolved issues, and next
  actions in the existing task record, accessible from the repository.
- **Concurrent work:** use separate worktrees or exclusive paths for code;
  one coordinator owns shared docs, records, and instruction updates.
- **Review:** Quick Review always assesses both tools and current knowledge.
  Critical rules stranded in on-demand docs, broken required imports/links,
  demonstrated knowledge loss, or affected incomplete migration block readiness.
  Missing `CODEX.md` never blocks review. Review reports repairs and migration
  actions without editing files or invoking migration itself.

These are project conventions and static file checks. They do not claim that
both hosts executed this checkout or that instructions physically enforce a
Git operation. No online documentation audit or dated vendor verification is
required by these skills.

## Documentation and migration

Explicitly invoke Knowledge Transfer for an area or the whole project. It makes
requested docs and instruction changes directly, then reports changed paths,
outcomes, and unresolved gaps so you can inspect the Git diff.

Record migration requires an explicit request, for example:

```text
Codex: $hawk-knowledge-transfer Migrate the Hawk records to docs/generated using native copies, verify them, and repair structural links.
Claude: /hawk-knowledge-transfer Migrate the Hawk records to docs/generated using native copies, verify them, and repair structural links.
```

Migration copies complete files with native commands and verifies equality before
editing. Only necessary references, paths, and routing then change. Recorded
facts, decisions, rationale, constraints, status, and history retain their meaning
and detail. Knowledge corrections are separate work. See the shared specification
for destination mapping, conflicts, source retirement, and command examples.

## Maintaining these skills

Edit `docs/agent-instruction-layout.md` once, then run
`python3 scripts/sync-agent-instructions.py --write` to package it for both skills.
Run `python3 scripts/sync-agent-instructions.py --check` to detect drift.
Each installed skill contains its own copy and has no dependency on the other.

Validate skill metadata with the active Skill Creator's validator, and check
host-specific invocation controls separately. Knowledge Transfer includes the
Claude `disable-model-invocation` frontmatter field and Codex's
`policy.allow_implicit_invocation` metadata; a portable-only validator may need
that supported Claude extension checked separately. Check actual local links
and run `git diff --check`. Inspect host loading separately when relevant;
file inspection alone does not establish runtime execution.

For installation or newly added skills, use the [installation guide](../README.md#install)
or the existing update skill's local mode, then start/reload the agent session.
