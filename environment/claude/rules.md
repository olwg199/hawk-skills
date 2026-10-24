# Claude Code only

- **Choice tool:** ask with `AskUserQuestion`, `multiSelect: true` unless the options exclude each other; its "Other"
  field is the free-form answer. The end-of-turn summary box after finished work gets the recap only (no `ask`, no
  `actions`).
- **Commit hooks:** besides the git hook for commit messages, `~/.claude/hooks/hawk/no_ai_in_pr.py` blocks a GitHub PR, issue
  or release command whose text names an AI, and `attribution` stays empty in `~/.claude/settings.json`.
- **AGENTS.md:** in a repository whose `CLAUDE.md` is missing or does not import `AGENTS.md`, read `AGENTS.md` at the start
  anyway, then set the project up as rule 13 says.
