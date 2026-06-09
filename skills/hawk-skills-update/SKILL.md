---
name: hawk-skills-update
description: >-
  Check GitHub for updates to hawk-skills and pull them if available. Use when
  the user wants to update their skills, or when asked to check for skill
  updates.
allowed-tools: Bash(git fetch:*), Bash(git log:*), Bash(git pull:*), Bash(git rev-parse:*), Bash(cat:*)
---

Update hawk-skills from GitHub.

## Steps

1. Read the repo path:
   ```bash
   cat ~/.hawk-skills-repo
   ```
   If the file doesn't exist, stop and tell the user to re-run `install.sh` from their hawk-skills clone.

2. Fetch from origin without merging:
   ```bash
   git -C <repo_path> fetch origin --quiet
   ```

3. Check if there are incoming commits:
   ```bash
   git -C <repo_path> log HEAD..origin/main --oneline
   ```

4. If **no new commits**: report "Already up to date." and stop.

5. If **new commits exist**:
   - Show the incoming commit list (the output from step 3).
   - Pull:
     ```bash
     git -C <repo_path> pull --ff-only origin main
     ```
   - Report what was updated (skill names from changed paths) and tell the user to restart their CLI to pick up changes.

6. If the pull fails (e.g. local modifications): report the error and tell the user to check `git status` in the repo.
