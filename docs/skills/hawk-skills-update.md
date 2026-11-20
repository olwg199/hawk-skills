# hawk-skills-update

Pulls the latest published skills from GitHub and refreshes the installed links for Claude Code and Codex.

## When to use

- To update the skill set. Not for the personal environment ([hawk-environment-setup](hawk-environment-setup.md)).

## How it works

- **Default:** only on `main`; fetches, pulls new commits and refreshes the links, so added, renamed and deleted skills
  stay in sync. It never switches branches.
- **`--local`:** refreshes the links from the current checkout without fetching, pulling or switching branches; use it
  to try local edits or a branch.
- The installer switches an SSH clone of the official repository to HTTPS fetches and keeps SSH for pushes; any
  other `origin` is changed only after your yes.
- Restart or reload the agent session afterwards.

## Invoke

- Claude Code: `/hawk-skills-update` or `/hawk-skills-update --local`
- Codex: `$hawk-skills-update` or `$hawk-skills-update --local`

The full workflow is in [SKILL.md](../../skills/hawk-skills-update/SKILL.md).
