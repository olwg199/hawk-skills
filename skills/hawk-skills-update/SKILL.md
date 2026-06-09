---
name: hawk-skills-update
description: >-
  Check GitHub for updates to hawk-skills and pull them if available. Use when
  the user wants to update their skills, or when asked to check for skill
  updates.
allowed-tools: Bash(git fetch:*), Bash(git log:*), Bash(git pull:*), Bash(git remote:*), Bash(git rev-parse:*), Bash(cat:*)
---

Update hawk-skills from GitHub.

## Steps

1. Read the repo path:
   ```bash
   cat ~/.hawk-skills-repo
   ```
   If the file doesn't exist, stop and tell the user to re-run `install.sh` from their hawk-skills clone.

2. Check the `origin` remote:
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

3. Fetch from origin without merging:
   ```bash
   git -C <repo_path> fetch origin --quiet
   ```

4. Check if there are incoming commits:
   ```bash
   git -C <repo_path> log HEAD..origin/main --oneline
   ```

5. If **no new commits**: report "Already up to date." and stop.

6. If **new commits exist**:
   - Show the incoming commit list (the output from step 4).
   - Pull:
     ```bash
     git -C <repo_path> pull --ff-only origin main
     ```
   - Report what was updated (skill names from changed paths) and tell the user to restart their CLI to pick up changes.

7. If fetch or pull fails:
   - If the error mentions authentication or SSH keys, confirm the repo uses the HTTPS remote above.
   - If the error mentions local modifications, tell the user to check `git status` in the repo.
