# hawk-skills

Personal AI CLI skills — reusable across Claude Code and Codex CLI.

## Install

Clone the repo and run the installer:

```bash
git clone https://github.com/olwg199/hawk-skills.git ~/hawk-skills
~/hawk-skills/install.sh
```

By default, this installs the skills for both Claude Code and Codex. To install
for only one CLI:

```bash
~/hawk-skills/install.sh --claude    # Claude Code only
~/hawk-skills/install.sh --codex     # Codex CLI only
```

The installer creates symlinks. After this first install, use
`/hawk-skills-update` to pull updates or refresh local branch changes.

## Update your skills

After installing, use the update skill any time you want the latest version:

```text
/hawk-skills-update
```

The update skill checks this GitHub repo, pulls new commits when available, and
tells you which skills changed. It also refreshes the Claude/Codex skill links,
so new, renamed, and deleted skills are synced without rerunning the installer
manually.

Manual fallback:

```bash
git -C ~/hawk-skills pull --ff-only origin main
~/hawk-skills/install.sh
```

Restart your CLI after updating so it reloads changed skill instructions.

### Test local branch changes

Installed skills are symlinks into this repo, so edits to existing skills follow
the branch you have checked out. When you add, rename, or delete skill folders,
refresh the links from the current branch:

```bash
git -C ~/hawk-skills switch my-feature
/hawk-skills-update --local
```

Local mode does not fetch, pull, or switch branches. To return to stable skills:

```bash
git -C ~/hawk-skills switch main
/hawk-skills-update
```

## Skills

### `hawk-skills-update`

Check GitHub for updates to this repo, refresh installed skill links, and sync
local branch changes with `--local`.

**Invoke:**
- Claude Code: `/hawk-skills-update` or `/hawk-skills-update --local`
- Codex: `/hawk-skills-update` or `/hawk-skills-update --local`

### `quick-review`

Adaptive code review that picks specialist agents based on what actually changed.

**Two modes:**
- **Local** — reviews all uncommitted changes (`git diff HEAD`)
- **PR** — reviews a specific pull request (`/quick-review 42` or a PR URL)

**How it works:**
1. A fast agent reads the diff and selects 1–3 relevant specialists
2. Specialist agents run in parallel (ui, logic, data, security, api) + a simplification reviewer that always runs
3. A final agent merges findings, filters low-confidence issues, and outputs results

In PR mode the output is posted as a GitHub PR comment. In local mode it prints to the terminal.

**Invoke:**
- Claude Code: `/quick-review` or `/quick-review 42`
- Codex: `/quick-review` or `/quick-review 42`
