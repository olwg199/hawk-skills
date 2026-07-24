---
name: hawk-skills-update
description: >-
  Check GitHub for updates to hawk-skills and pull them if available. Use when
  the user wants to update their skills, or when asked to check for skill
  updates. Supports --local to refresh installed skill links from the current
  checkout without fetching or pulling.
allowed-tools: Bash(git branch:*), Bash(git diff:*), Bash(git fetch:*), Bash(git log:*), Bash(git pull:*), Bash(git remote:*), Bash(git rev-parse:*), Bash(git status:*), Bash(cat:*), Bash(*install.sh:*), Bash(*install.ps1:*), Bash(pwsh:*), Bash(pwsh.exe:*), Bash(powershell:*), Bash(powershell.exe:*)
---

Update hawk-skills from GitHub, or refresh installed skill links from the current local checkout.

## Clarify ambiguous requests

Resolve material ambiguity before acting on a user message.

- Inspect the current message, relevant recent chat context, and available project evidence before asking.
- If one reasonable interpretation is low-risk and does not materially change scope, behavior, files, output, or external state, state the assumption and continue.
- If two or more plausible interpretations would lead to materially different work, pause and ask a targeted clarification. Name the likely meanings and their practical difference; prefer “Did you mean A or B?” over “Can you clarify?”
- Use the host's questions or structured user-input tool when available. Offer 2–3 mutually exclusive choices, put the recommended interpretation first when evidence supports one, and allow a free-form answer when the host supports it. Otherwise ask the same concise question in normal chat.
- Ask only the smallest set of blocking questions. Do not repeat questions answered by the request or context, and do not treat ambiguity as permission to broaden scope or make a consequential change.

## Modes

- **Default mode** (`/hawk-skills-update`): update from `origin/main`, then refresh installed skill links.
- **Local mode** (`/hawk-skills-update --local`, or if the user asks to update from local changes/current branch): skip fetch and pull, then refresh installed skill links from the currently checked-out branch.

Never switch branches automatically. If the user wants to test a branch, they should switch branches before running local mode.

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
   Report the branch in the final response.

3. Check the `origin` remote:
   ```bash
   git -C <repo_path> remote get-url origin
   ```
   If it is `git@github.com:olwg199/hawk-skills.git` or `ssh://git@github.com/olwg199/hawk-skills.git`, switch fetches to HTTPS first:
   ```bash
   git -C <repo_path> remote set-url origin https://github.com/olwg199/hawk-skills.git
   ```
   Then preserve SSH for maintainer pushes:
   ```bash
   git -C <repo_path> remote set-url --push origin git@github.com:olwg199/hawk-skills.git
   ```
   Public GitHub repos can be fetched without authentication over HTTPS. SSH remotes still require an SSH key, but they are useful for authenticated pushes.

4. If running in **local mode**:
   - Do not fetch.
   - Do not pull.
   - Do not switch branches.
   - Optionally show local skill file changes:
     ```bash
     git -C <repo_path> status --short skills
     ```
   - When reporting changed skills, infer skill names from changed paths under `skills/<skill-name>/...` when possible.
   - Run the installer to refresh Claude/Codex symlinks for the current checkout.
     macOS/Linux:
     ```bash
     <repo_path>/install.sh
     ```
     Windows PowerShell:
     ```powershell
     powershell -ExecutionPolicy Bypass -File "<repo_path>\install.ps1"
     ```
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
   - Run the installer anyway, so new/renamed/deleted local skill links are synced.
     macOS/Linux:
     ```bash
     <repo_path>/install.sh
     ```
     Windows PowerShell:
     ```powershell
     powershell -ExecutionPolicy Bypass -File "<repo_path>\install.ps1"
     ```
   - Report "Already up to date." and tell the user to restart/reload their CLI if links changed.
   - Stop.

9. If **new commits exist**:
   - Show the incoming commit list (the output from step 7).
   - Before pulling, collect changed skill paths when possible:
     ```bash
     git -C <repo_path> diff --name-only HEAD..origin/main -- skills
     ```
     Infer skill names from paths under `skills/<skill-name>/...`.
   - Pull:
     ```bash
     git -C <repo_path> pull --ff-only origin main
     ```
   - Run the installer to refresh Claude/Codex symlinks.
     macOS/Linux:
     ```bash
     <repo_path>/install.sh
     ```
     Windows PowerShell:
     ```powershell
     powershell -ExecutionPolicy Bypass -File "<repo_path>\install.ps1"
     ```
   - Report what was updated (skill names from changed paths) and tell the user to restart their CLI to pick up changes.

10. If fetch or pull fails:
   - If the error mentions authentication or SSH keys, confirm the repo uses the HTTPS remote above.
   - If the error mentions local modifications, tell the user to check `git status` in the repo.
