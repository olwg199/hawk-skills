# hawk-environment-setup

Applies the repository owner's personal agent environment from `environment/` to this computer: global Claude and
Codex rules, the hooks that keep AI names out of commits and PRs, Claude settings and git settings. If you use these
skills yourself, ignore `environment/` or replace its rules with your own.

## When to use

- When you ask to set up, sync, check or repair your environment or global rules.
- Not for the skill set ([hawk-skills-update](hawk-skills-update.md)) or project rules
  ([hawk-project-rules-review](hawk-project-rules-review.md)).

## How it works

- Pulls on `main` (otherwise uses the files as they are), checks the home folder, applies and reports. Home files are
  copies, so a branch switch never breaks a running session.
- A home file edited at home is replaced only after you agree, and the old one is backed up first.
- Rules for one computer live outside git; the skill proposes them and offers to drop what the shared rules already
  cover.
- `check` mode only reports, and fails when `environment/` holds anything personal, so it is never pushed.
- Shared rules are edited in `environment/`; some sections come from `docs/`
  ([which ones](../working-with-agents.md#maintaining-these-skills)).

## Invoke

- Claude Code: `/hawk-environment-setup` (or `/hawk-environment-setup check`)
- Codex: `$hawk-environment-setup`

What it copies, merges and sets, and where backups and local rules go, is in
[SKILL.md](../../skills/hawk-environment-setup/SKILL.md).
