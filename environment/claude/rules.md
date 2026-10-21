# Claude Code only

- **Choice tool:** ask with `AskUserQuestion`. The end-of-turn summary box after finished work gets the recap only (no `ask`, no
  `actions`).
- **Commit hooks:** besides the git hook for commit messages, `~/.claude/hooks/hawk/no_ai_in_pr.py` blocks a GitHub PR, issue
  or release command whose text names an AI, and `attribution` stays empty in `~/.claude/settings.json`.
