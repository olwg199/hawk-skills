# hawk-mobile-ui-builder

Builds mobile UI from screenshots as pure, reusable presentation components that follow the project's structure.

## When to use

- Only when you name the skill. An ordinary "build this screen" request does not load it.

## How it works

- Breaks the screenshots into screens, sections, reusable components and the UI states that matter.
- Reuses the project's components, tokens and placement; asks only about real ambiguity or a new convention.
- Actions become props and callbacks; non-UI integration is left as `TODO:` comments.
- Verifies the reference and extra states, then reports the props and callbacks to wire later.

## What it writes

- UI components and preview fixtures in the project's own folders.
- `docs/generated/hawk-mobile-ui-builder/project.md`: confirmed UI conventions for later runs.

## Invoke

- Claude Code: `/hawk-mobile-ui-builder`
- Codex: `$hawk-mobile-ui-builder`

The full workflow is in [SKILL.md](../../skills/hawk-mobile-ui-builder/SKILL.md).
