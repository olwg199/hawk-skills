# hawk-skills

Personal AI CLI skills — reusable across Claude Code and Codex CLI.

This repository is a small developer-productivity toolkit for packaging repeatable
AI-assisted engineering workflows as versioned skills. It focuses on practical
local automation: code review routing, skill installation, update management, and
project-aware UI implementation support.

## Why this exists

AI coding tools are more useful when repeatable workflows are explicit, portable,
and easy to keep current. This repo keeps those workflows versioned in one place
and installs them into both Claude Code and Codex.

The important foundation is `hawk-skills-update`: once the repo is installed,
that skill can pull the latest version and refresh local links from inside the
agent. Individual skills may be added, changed, or removed over time, but the
update path should stay simple.

## Project highlights

- Cross-CLI skill packaging for Claude Code and Codex.
- macOS/Linux and native Windows PowerShell installers.
- In-agent update workflow that refreshes local skill links after repo changes.
- Adaptive code review skill that chooses focused reviewer roles from the actual
  diff instead of running a generic checklist every time.
- Conservative review behavior: findings are filtered for confidence and tied to
  concrete file/line references.
- Focused review-remediation skill that fixes supplied findings with scoped
  agents and one combined verification pass.
- Documentation and screenshots that show real output in both Codex and Claude
  Code.

## Engineering focus

The repo is intentionally small, but it demonstrates how I approach developer
tooling: make common workflows repeatable, keep automation inspectable, support
multiple environments, and keep a human review point over consequential decisions.

## What it looks like

`hawk-quick-review` is one example of a skill managed by this repo. It reviews
local changes, picks relevant specialist reviewers, and returns concise findings
with file and line references.

Codex output with inline review comments:

![hawk-quick-review output in Codex](docs/assets/hawk-quick-review-codex.png)

Claude Code output with specialist reviewers and simplification leads:

![hawk-quick-review output in Claude Code](docs/assets/hawk-quick-review-claude-code.png)

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

For Claude Code, the installer links each skill into `~/.claude/skills/`.
Current Claude Code exposes those skills to both Claude and you: Claude can load
them automatically when relevant, and you can invoke them directly as slash
commands such as `/hawk-quick-review`.

The installer does not create `~/.claude/commands/*.md` mirrors by default.
Those mirrors are only for older Claude Code versions and can make current
Claude Code list the same skill twice. To opt into legacy command mirrors:

```powershell
powershell -ExecutionPolicy Bypass -File "$HOME\hawk-skills\install.ps1" -ClaudeCommands
```

```bash
~/hawk-skills/install.sh --claude-commands
```

The installer links skill folders into your CLI config. After this first
install, use `/hawk-skills-update` to pull updates or refresh local branch changes.

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
/hawk-skills-update --local
```

```powershell
git -C "$HOME\hawk-skills" switch my-feature
/hawk-skills-update --local
```

Local mode does not fetch, pull, or switch branches. To return to stable skills:

```bash
git -C ~/hawk-skills switch main
/hawk-skills-update
```

```powershell
git -C "$HOME\hawk-skills" switch main
/hawk-skills-update
```

## Skills

All personal skills in this repo use the `hawk-` prefix for folder names,
`name:` frontmatter, and slash commands to avoid collisions with community or
built-in skill names.

### `hawk-skills-update`

Check GitHub for updates to this repo, refresh installed skill links, and sync
local branch changes with `--local`.

**Invoke:**
- Claude Code: `/hawk-skills-update` or `/hawk-skills-update --local`
- Codex: `/hawk-skills-update` or `/hawk-skills-update --local`

### `hawk-quick-review`

Adaptive local code review that picks specialist reviewer roles based on what actually changed.

Reviews uncommitted local tracked changes (`git diff HEAD`) and classifies untracked files from `git status --short --untracked-files=all`, reviewing only likely intentional source/config additions by default.

**How it works:**
1. Reads the diff and selects 1–3 relevant specialists
2. Runs only the selected reviewers (ui, logic, data, security, api, and simplification when the diff warrants it)
3. Merges findings, filters low-confidence issues, and outputs stable `F1` finding IDs and `S1` simplification-lead IDs

The simplification reviewer runs only for explicit simplification/refactor
requests, duplicated or repeated changed code, large refactors, or changed code
that appears to reimplement a nearby project-local helper/pattern. Plausible but
unproven simplification ideas are reported separately as non-blocking
nice-to-have leads.

When the host supports and permits sub-agents, specialist reviewers run in
parallel. In Codex, the skill first discovers the multi-agent tool and falls
back to sequential review if sub-agents are unavailable or not permitted by the
current request. Subagent visibility is best in Codex app and CLI; other
surfaces may use the sequential fallback.

In Codex, model choice follows Codex's normal model-selection policy. In Claude
Code, use Haiku for planning/filtering and Sonnet for routine specialist
review. Expensive Anthropic models are only for explicit user requests or one
targeted follow-up on an unusually complex, high-impact unresolved finding.

The review returns in the assistant response or terminal, depending on the host.

**Invoke:**
- Claude Code: `/hawk-quick-review`
- Codex: `/hawk-quick-review using parallel sub-agents`
- Codex with reviewer focus: `/hawk-quick-review use subagents Make sure data consistency is not compromised`

### `hawk-fix-review-findings`

Fix findings from the preceding `hawk-quick-review` output or from pasted local
review text. It includes reported issues and nice-to-have simplification leads
by default; stable `F1` and `S1` IDs let comments precisely prioritize, skip,
or clarify those items.

The skill starts from each reported file and line, inspecting only directly
related code and expanding context only when necessary. It does not rerun the
review or re-review the complete diff. When separate findings have exclusive
paths or subsystems, it can delegate up to three scoped fixes in parallel;
otherwise it coordinates the edits sequentially.

After all accepted fixes are integrated, it runs the smallest relevant existing
tests, typechecks, linters, or build commands once for the entire batch. It
reports fixed, skipped, blocked, and verification-failed findings with the
changed files and check results. It never commits, pushes, or reruns the review
automatically.

**Invoke:**
- Claude Code: `/hawk-fix-review-findings`
- Codex: `/hawk-fix-review-findings Fix the findings from the preceding review`
- With comments: `/hawk-fix-review-findings Skip F2; prioritize F1 and S1`

### `hawk-build`

Run a durable build lifecycle for features, fixes, refactors, and technical
investigations. It creates one tracked Markdown record per build in `.build/`,
researches and refines the task with you, saves the confirmed plan before
implementation, and records meaningful implementation attempts, delegated work,
verification, deviations, and final results.

When a task can be safely partitioned, it assigns non-overlapping UI, API, data,
test, or research workstreams to subagents and consolidates their compact results
in the build record. Related user-authorized commits use a `Build: <build-id>`
trailer for traceability.

**Invoke:**
- Claude Code: `/hawk-build Add account rate limiting`
- Codex: `/hawk-build Research, plan, and build account rate limiting`

### `hawk-mobile-ui-builder`

Build pure mobile UI from screenshots while reusing the target project's
component and screen structure.

**How it works:**
1. Inspects the project and reads `.codex/mobile-ui-builder.md` when present
2. Decomposes provided screenshots into screens, sections, and reusable UI components
3. Asks where existing and new components/screens should live before implementing
4. Implements only presentation UI and leaves non-UI logic as `TODO:` comments
5. Updates `.codex/mobile-ui-builder.md` with confirmed project conventions

**Invoke:**
- Claude Code: `/hawk-mobile-ui-builder`
- Codex: `/hawk-mobile-ui-builder`
