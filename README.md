# hawk-skills

Personal agent skills for Claude Code and Codex: build, docs, review and fix workflows, versioned in one place.

## Skills

In development lifecycle order; pick the one the work needs.

| Skill | What it does |
|---|---|
| [hawk-build](docs/skills/hawk-build.md) | Plans and carries out a feature, fix, refactor or investigation. |
| [hawk-mobile-ui-builder](docs/skills/hawk-mobile-ui-builder.md) | Builds reusable mobile UI from screenshots. |
| [hawk-docs](docs/skills/hawk-docs.md) | Writes and updates project docs so they are correct the first time. |
| [hawk-knowledge-transfer](docs/skills/hawk-knowledge-transfer.md) | Organizes human docs and shared agent instructions. |
| [hawk-project-rules-review](docs/skills/hawk-project-rules-review.md) | Checks project rules and agent config against your global rules. |
| [hawk-project-review](docs/skills/hawk-project-review.md) | Explains and assesses an existing project area. |
| [hawk-quick-review](docs/skills/hawk-quick-review.md) | Reviews local changes before a commit. |
| [hawk-fix-review-findings](docs/skills/hawk-fix-review-findings.md) | Fixes supplied review findings. |
| [hawk-skills-update](docs/skills/hawk-skills-update.md) | Pulls skill updates and refreshes the installed links. |
| [hawk-environment-setup](docs/skills/hawk-environment-setup.md) | Applies the owner's personal agent environment (owner only). |

Invoke a skill as `/hawk-build` in Claude Code or `$hawk-build` in Codex; Claude Code also loads skills by their
description.

## Install

macOS/Linux:

```bash
git clone https://github.com/olwg199/hawk-skills.git ~/hawk-skills
~/hawk-skills/install.sh
```

Windows (native PowerShell, no Bash or WSL):

```powershell
git clone https://github.com/olwg199/hawk-skills.git "$HOME\hawk-skills"
powershell -ExecutionPolicy Bypass -File "$HOME\hawk-skills\install.ps1"
```

The installer links each skill into `~/.claude/skills/` and `~/.codex/skills/`. Options: `--claude` / `-Claude` or
`--codex` / `-Codex` for one CLI only; `--claude-commands` / `-ClaudeCommands` adds `~/.claude/commands/` mirrors for
old Claude Code versions. Reload the agent session afterwards; later updates come from
[hawk-skills-update](docs/skills/hawk-skills-update.md).

## More

- [Project documentation](docs/README.md): shared rules the skills follow, and how to maintain them.
- Tests: `python -m unittest discover -s tests`.
