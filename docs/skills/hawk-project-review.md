# hawk-project-review

Reviews an existing feature, subsystem, file, symbol or reported problem without a commit diff: how it works now,
what is wrong, and what to improve.

## When to use

- Only when you name the skill.
- For uncommitted changes use [hawk-quick-review](hawk-quick-review.md); to make the fixes use
  [hawk-build](hawk-build.md).

## How it works

- Traces the area through its callers, data flow, contracts, tests, configuration and error handling, and stays there.
- Defects get `F1` IDs and priorities; non-blocking improvements get `I1` IDs. Each has locations, required behavior,
  trade-offs and verification.
- Structural advice follows the nearest comparable code in the project.
- Read-only: it never edits files.

## Invoke

- Claude Code: `/hawk-project-review Review how order synchronization works and how it can be improved`
- Codex: `$hawk-project-review Determine why session refresh can log users out and recommend a fix`

The full workflow is in [SKILL.md](../../skills/hawk-project-review/SKILL.md).
