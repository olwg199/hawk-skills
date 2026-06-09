# hawk-skills

Personal AI CLI skills — reusable across Claude Code and Codex CLI.

## Install

Clone the repo and run the installer for your OS.

macOS/Linux:

```bash
git clone https://github.com/olwg199/hawk-skills.git ~/hawk-skills
~/hawk-skills/install.sh
```

Windows PowerShell:

```powershell
git clone https://github.com/olwg199/hawk-skills.git "$HOME\hawk-skills"
powershell -ExecutionPolicy Bypass -File "$HOME\hawk-skills\install.ps1"
```

The Windows installer is native PowerShell; it does not require Bash, Git Bash,
or WSL.

By default, this installs the skills for both Claude Code and Codex. To install
for only one CLI:

```bash
~/hawk-skills/install.sh --claude    # Claude Code only
~/hawk-skills/install.sh --codex     # Codex CLI only
```

```powershell
powershell -ExecutionPolicy Bypass -File "$HOME\hawk-skills\install.ps1" -Claude    # Claude Code only
powershell -ExecutionPolicy Bypass -File "$HOME\hawk-skills\install.ps1" -Codex     # Codex CLI only
```

If Claude shows duplicate entries on Windows, install without Claude command
mirrors and keep only skill entries:

```powershell
powershell -ExecutionPolicy Bypass -File "$HOME\hawk-skills\install.ps1" -NoClaudeCommands
```

The installer links skill folders into your CLI config. On Windows, Claude
command files are symlinked when possible and copied as a fallback. After this
first install, use
`/h-skills-update` to pull updates or refresh local branch changes.

## Update your skills

After installing, use the update skill any time you want the latest version:

```text
/h-skills-update
```

The update skill checks this GitHub repo, pulls new commits when available, and
tells you which skills changed. It also refreshes the Claude/Codex skill links,
so new, renamed, and deleted skills are synced without rerunning the installer
manually.

Manual fallback:

macOS/Linux:

```bash
git -C ~/hawk-skills pull --ff-only origin main
~/hawk-skills/install.sh
```

Windows PowerShell:

```powershell
git -C "$HOME\hawk-skills" pull --ff-only origin main
powershell -ExecutionPolicy Bypass -File "$HOME\hawk-skills\install.ps1"
```

Restart your CLI after updating so it reloads changed skill instructions.

### Test local branch changes

Installed skills are symlinks into this repo, so edits to existing skills follow
the branch you have checked out. When you add, rename, or delete skill folders,
refresh the links from the current branch:

```bash
git -C ~/hawk-skills switch my-feature
/h-skills-update --local
```

```powershell
git -C "$HOME\hawk-skills" switch my-feature
/h-skills-update --local
```

Local mode does not fetch, pull, or switch branches. To return to stable skills:

```bash
git -C ~/hawk-skills switch main
/h-skills-update
```

```powershell
git -C "$HOME\hawk-skills" switch main
/h-skills-update
```

## Skills

All personal skills in this repo use the `h-` prefix to avoid collisions with
community or built-in skill names.

### `h-skills-update`

Check GitHub for updates to this repo, refresh installed skill links, and sync
local branch changes with `--local`.

**Invoke:**
- Claude Code: `/h-skills-update` or `/h-skills-update --local`
- Codex: `/h-skills-update` or `/h-skills-update --local`

### `h-quick-review`

Adaptive code review that picks specialist agents based on what actually changed.

**Two modes:**
- **Local** — reviews all uncommitted changes (`git diff HEAD`)
- **PR** — reviews a specific pull request (`/h-quick-review 42` or a PR URL)

**How it works:**
1. A fast agent reads the diff and selects 1–3 relevant specialists
2. Specialist agents run in parallel (ui, logic, data, security, api) + a simplification reviewer that always runs
3. A final agent merges findings, filters low-confidence issues, and outputs results

In PR mode the output is posted as a GitHub PR comment. In local mode it prints to the terminal.

**Invoke:**
- Claude Code: `/h-quick-review` or `/h-quick-review 42`
- Codex: `/h-quick-review` or `/h-quick-review 42`
