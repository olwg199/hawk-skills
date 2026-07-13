# Hawk Build Project Map

## Architecture and boundaries

- Personal skills live under `skills/hawk-*`; each skill keeps its workflow in `SKILL.md` and optional supporting resources inside its own folder.
- Shared repository documentation belongs in `README.md`; task-specific build history belongs in `.build/`.

## Placement

- Skills: `skills/hawk-<name>/`
- Skill UI metadata: `skills/hawk-<name>/agents/openai.yaml`
- Skill-specific assets: `skills/hawk-<name>/assets/`
- Durable Hawk Build research: `.codex/hawk-build.md`
- Tests: no repository-local automated skill test suite is currently present.

## Reference features

- `skills/hawk-mobile-ui-builder/SKILL.md` — demonstrates concise project-local memory in `.codex/<skill>.md`.
- `skills/hawk-build/SKILL.md` — demonstrates the durable research, planning, implementation, and finalization lifecycle.

## Verification

- Run the active `skill-creator/scripts/quick_validate.py <skill-folder>` — validate skill metadata and structure.
- `git diff --check` — detect whitespace errors in repository changes.

## File organization

- Use the `hawk-` prefix for personal skill folders and `name:` values.
- Keep `SKILL.md` concise and place only genuinely reusable supporting material in `assets/`, `references/`, or `scripts/`.
