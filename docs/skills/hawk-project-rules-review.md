# hawk-project-rules-review

Checks one project's agent rules and agent config against your global rules.

## When to use

- Only when you name the skill.
- Not for the global or per-computer rules ([hawk-environment-setup](hawk-environment-setup.md)) or for migrating
  project knowledge ([hawk-knowledge-transfer](hawk-knowledge-transfer.md)).

## How it works

- Reads `AGENTS.md`, `CLAUDE.md`, `CODEX.md`, `CLAUDE.local.md`, nested rule files and everything they import or link,
  plus `.claude/settings*.json`, `.codex/config.toml` and `.mcp.json`.
- Reports rules that repeat or contradict the global ones, stale paths and commands, layout gaps, and settings that
  undo global protections, as [rules comparison](../rules-comparison.md) says.
- Changes nothing until you pick Apply; then edits only the project files in its plan, never the global rules, and
  does not commit. Contradictions are always your call.

## Invoke

- Claude Code: `/hawk-project-rules-review`
- Codex: `$hawk-project-rules-review`

The full workflow is in [SKILL.md](../../skills/hawk-project-rules-review/SKILL.md).
