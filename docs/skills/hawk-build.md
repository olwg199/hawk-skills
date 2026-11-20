# hawk-build

Plans and carries out a feature, fix, refactor or technical investigation, and keeps a record of it.

## When to use

- Any request to build, implement, fix, refactor or investigate, also in plain words ("Fix the signup keyboard
  spacing").
- Not for explanations, read-only reviews or documentation-only requests (that is [hawk-docs](hawk-docs.md)).

## How it works

- **Lightweight path:** a clear, localized change is made, verified and logged as one entry in the build history.
- **Full lifecycle:** research, a plan in the shared plan shape for your approval, implementation, verification and a
  build record. Work items can be approved, revised or excluded by ID.
- Tests are run but never changed unless you asked for that test change.
- Resume unfinished work with "Continue the next item of <record or plan path> that is not done."
- Independent workstreams can go to subagents; the main agent consolidates them.
- Finished work closes the project docs it settled. Commits only with your approval, never automatic.

## What it writes

- `docs/generated/hawk-build/builds/`: build records and the history index.
- `docs/generated/hawk-build/project.md`: a short reusable project map.

## Invoke

- Claude Code: `/hawk-build Add account rate limiting`
- Codex: `$hawk-build Research, plan, and build account rate limiting`

The full workflow is in [SKILL.md](../../skills/hawk-build/SKILL.md).
