---
name: hawk-skills-update
description: >-
  Check GitHub for updates to hawk-skills and pull them if available. Use when
  the user wants to update their skills, or when asked to check for skill
  updates. Supports --local to refresh installed skill links from the current
  checkout without fetching or pulling.
allowed-tools: Bash(git branch:*), Bash(git diff:*), Bash(git fetch:*), Bash(git log:*), Bash(git pull:*), Bash(git remote get-url:*), Bash(git rev-parse:*), Bash(git status:*), Bash(cat:*), Bash(*install.sh:*), Bash(*install.ps1:*), Bash(pwsh:*), Bash(pwsh.exe:*), Bash(powershell:*), Bash(powershell.exe:*)
---

Update hawk-skills from GitHub, or refresh installed skill links from the current local checkout.

## Clarify ambiguous requests

Before acting on an unclear request, follow [unclear requests](references/report-format.md#unclear-requests).

## Modes

Invocation text: $ARGUMENTS

If that line is empty or shows a literal placeholder (for example in Codex), use any text after the skill name in the user's message. `--local` selects local mode.

- **Default mode** (`/hawk-skills-update`): update from `origin/main`, then refresh installed skill links.
- **Local mode** (`/hawk-skills-update --local`, or if the user asks to update from local changes/current branch): skip fetch and pull, then refresh installed skill links from the currently checked-out branch.

Never switch branches automatically. If the user wants to test a branch, they should switch branches before running local mode.

Write the final report as [report and question format](references/report-format.md) describes: in the user's
language, the update result (skill names, never the commit list) and restart note as statements, and no closing
question. Name the branch only in local mode or when the run stopped because it is not `main`.

## Run the installer

macOS/Linux:
```bash
<repo_path>/install.sh
```
Windows PowerShell:
```powershell
powershell -ExecutionPolicy Bypass -File "<repo_path>\install.ps1"
```

## Steps

1. Read the repo path:
   ```bash
   cat ~/.hawk-skills-repo
   ```
   If the file doesn't exist, stop and tell the user to re-run the installer from their hawk-skills clone.

2. Detect the current branch:
   ```bash
   git -C <repo_path> branch --show-current
   ```

3. Check the `origin` remote:
   ```bash
   git -C <repo_path> remote get-url origin
   ```
   The installer itself switches fetches of the official repository's SSH `origin` to HTTPS and keeps SSH for pushes;
   say so in the report when it did. Never change any other remote on your own. If the fetch in step 6 fails on an SSH URL (`git@github.com:<owner>/<repo>.git`)
   for lack of a key, say that a public repo can be fetched over HTTPS and offer to switch fetches only, keeping SSH for
   pushes; run these only after the user's yes:
   ```bash
   git -C <repo_path> remote set-url --push origin <current SSH URL>
   git -C <repo_path> remote set-url origin https://github.com/<owner>/<repo>.git
   ```

4. If running in **local mode**:
   - Do not fetch.
   - Do not pull.
   - Do not switch branches.
   - Optionally show local skill file changes:
     ```bash
     git -C <repo_path> status --short skills
     ```
   - When reporting changed skills, infer skill names from changed paths under `skills/<skill-name>/...` when possible.
   - [Run the installer](#run-the-installer) to refresh Claude/Codex symlinks for the current checkout.
   - Report that links were refreshed from the current branch and tell the user to restart/reload their CLI.
   - Stop.

5. If running in **default mode**, require the current branch to be `main`.
   - If the current branch is not `main`, stop and tell the user:
     - Default updates only run on `main`.
     - To test this branch, run `/hawk-skills-update --local`.
     - To update stable skills, switch to `main` first.

6. Fetch from origin without merging:
   ```bash
   git -C <repo_path> fetch origin --quiet
   ```

7. Check if there are incoming commits:
   ```bash
   git -C <repo_path> log HEAD..origin/main --oneline
   ```

8. If **no new commits**:
   - [Run the installer](#run-the-installer) anyway, so new/renamed/deleted local skill links are synced.
   - Report "Already up to date." and tell the user to restart/reload their CLI if links changed.
   - Stop.

9. If **new commits exist**:
   - Before pulling, collect changed skill paths when possible:
     ```bash
     git -C <repo_path> diff --name-only HEAD..origin/main -- skills
     ```
     Infer skill names from paths under `skills/<skill-name>/...`.
   - Pull:
     ```bash
     git -C <repo_path> pull --ff-only origin main
     ```
   - [Run the installer](#run-the-installer) to refresh Claude/Codex symlinks.

10. If fetch or pull fails:
   - If the error mentions authentication or SSH keys on an SSH URL, make the HTTPS offer from step 3; change nothing
     without the user's yes.
   - If the error mentions local modifications, tell the user to check `git status` in the repo.
