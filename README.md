# hawk-skills

Personal AI CLI skills — reusable across Claude Code and Codex CLI.

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

If this repo was cloned with SSH earlier, switch it to HTTPS first so update
checks do not require GitHub authentication:

```bash
git -C ~/hawk-skills remote set-url origin https://github.com/olwg199/hawk-skills.git
```

If you maintain this repo and want pushes to keep using SSH, set a separate push
URL:

```bash
git -C ~/hawk-skills remote set-url --push origin git@github.com:olwg199/hawk-skills.git
```

That gives you the best of both paths: unauthenticated public fetches over HTTPS
and authenticated writes over SSH.

Restart your CLI after updating so it reloads changed skill instructions.

---

## Skills

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

### `hawk-skills-update`

Check GitHub for updates to this repo, normalize the remote to HTTPS when
needed, preserve SSH pushes for maintainers, and pull new skill changes without
SSH auth hassles.

**Invoke:**
- Claude Code: `/hawk-skills-update`
- Codex: `/hawk-skills-update`

---

## Install

Clone the repo and run the install script:

```bash
git clone https://github.com/olwg199/hawk-skills.git ~/hawk-skills
cd ~/hawk-skills
chmod +x install.sh
./install.sh
```

Use the HTTPS clone URL above. SSH remotes (`git@github.com:...`) require an
SSH key even when the repository is public, while HTTPS can fetch public repos
without GitHub authentication.

Install for a specific CLI only:

```bash
./install.sh --claude    # Claude Code only
./install.sh --codex     # Codex CLI only
```

The install script creates symlinks — changes you pull automatically take effect without reinstalling.

### Auto-update on Claude Code startup

Run the install script with `--autoupdate` to get instructions for adding a startup hook that pulls the latest skills every time Claude Code launches:

```bash
./install.sh --autoupdate
```

### New machine setup

```bash
git clone https://github.com/olwg199/hawk-skills.git ~/hawk-skills
~/hawk-skills/install.sh
```

---

## Adding a new skill

1. Create `skills/<skill-name>/SKILL.md`
2. Add frontmatter: `name`, `description`, and optionally `allowed-tools` (Claude Code)
3. Write the prompt body
4. Run `./install.sh` again — the new symlinks are created automatically
