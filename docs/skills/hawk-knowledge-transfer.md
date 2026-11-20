# hawk-knowledge-transfer

Organizes a project area into short human docs under `docs/` and shared agent instructions (`AGENTS.md`, imported by
`CLAUDE.md`), from verified project evidence.

## When to use

- Only when you name the skill. Ordinary documentation requests go to [hawk-docs](hawk-docs.md). Codex enforces
  this; Claude Code follows the description.
- Name the area to document, or ask for the whole project for onboarding docs.

## How it works

- Keeps essential rules in `AGENTS.md` and detailed area guidance in linked docs; `CODEX.md` is optional.
- Shows new rule-file wording before changing it; other requested doc edits are made directly for Git review.
- Moving old skill records is a separate explicit request: full-file copies, an equality check, then only link and
  path fixes.
- Never changes production code and never commits.

The layout it follows is in [instruction layout](../agent-instruction-layout.md).

## Invoke

- Claude Code: `/hawk-knowledge-transfer Document order synchronization and its agent handoff`
- Codex: `$hawk-knowledge-transfer Document order synchronization and its agent handoff`

The full workflow is in [SKILL.md](../../skills/hawk-knowledge-transfer/SKILL.md).
