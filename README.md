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

The installer creates symlinks, so updates pulled by `/hawk-skills-update` take
effect without reinstalling. Restart your CLI after installing or updating.

## Update your skills

After installing, use the update skill any time you want the latest version:

```text
/hawk-skills-update
```

The update skill checks this GitHub repo, pulls new commits when available, and
tells you which skills changed. It also makes sure this repo uses the public
HTTPS remote so updates do not require an SSH key.

Manual fallback:

```bash
git -C ~/hawk-skills pull --ff-only origin main
```

Restart your CLI after updating so it reloads changed skill instructions.

## Skills

### `hawk-skills-update`

Check GitHub for updates to this repo, normalize the remote to HTTPS when
needed, preserve SSH pushes for maintainers, and pull new skill changes without
SSH auth hassles.

**Invoke:**
- Claude Code: `/hawk-skills-update`
- Codex: `/hawk-skills-update`

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
