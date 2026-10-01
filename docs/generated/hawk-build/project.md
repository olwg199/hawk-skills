# Hawk Build Project Map

## Architecture and boundaries

- Personal skills live under `skills/hawk-*`; each skill keeps its workflow in `SKILL.md` and optional supporting resources inside its own folder.
- Shared repository documentation belongs in `README.md` and `docs/`; task-specific build history belongs in `docs/generated/hawk-build/builds/`.

## Placement

- Skills: `skills/hawk-<name>/`
- Skill UI metadata: `skills/hawk-<name>/agents/openai.yaml`
- Skill-specific assets: `skills/hawk-<name>/assets/`
- Durable Hawk Build research: `docs/generated/hawk-build/project.md`
- Human documentation and shared agent setup: `docs/README.md` and `docs/working-with-agents.md`
- Instruction routes: essential project-wide rules are in root `AGENTS.md`, imported by `CLAUDE.md`; detailed area guidance is linked under `docs/`; `CODEX.md` is optional and its absence never blocks review
- Shared layout: `docs/agent-instruction-layout.md`, packaged for both Knowledge Transfer and Quick Review by `scripts/sync-agent-instructions.py`
- Tests: no repository-local automated skill test suite is currently present.

## Reference features

- `skills/hawk-mobile-ui-builder/SKILL.md` — demonstrates concise project-local memory in `docs/generated/hawk-mobile-ui-builder/project.md`.
- `skills/hawk-knowledge-transfer/SKILL.md` — explicitly invoked docs/instruction maintenance and requested native-copy record migration.
- `skills/hawk-quick-review/references/knowledge-compatibility.md` — defines the mandatory blocking knowledge/setup pass, including empty code diffs.
- `skills/hawk-build/SKILL.md` — demonstrates the durable research, planning, implementation, and finalization lifecycle.

## Verification

- Run the active Skill Creator validator for portable skill metadata; check Knowledge Transfer’s supported Claude invocation field and Codex policy separately.
- `git diff --check` — detect whitespace errors in repository changes.
- `python3 scripts/sync-agent-instructions.py --check` — verify shared-reference packaging when layout or packaged references change.

## File organization

- Use the `hawk-` prefix for personal skill folders and `name:` values.
- Keep `SKILL.md` concise and place only genuinely reusable supporting material in `assets/`, `references/`, or `scripts/`.
