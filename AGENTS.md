# Project instructions

- Personal skills in this repo must use the `hawk-` prefix for folder names, `name:` frontmatter, and documented slash commands.
- When changing install or update behavior, update both `install.sh` and `install.ps1` in the same change unless the change is explicitly platform-specific.
- Keep the installers behaviorally equivalent where possible, but use native platform mechanisms: Bash for macOS/Linux and PowerShell for Windows. Do not make the Windows installer depend on Bash, Git Bash, or WSL.
- Installer cleanup must only remove links or tracked copies created by this repo, and must leave unrelated user skills alone.
- Keep essential project-wide rules directly in `AGENTS.md`; `CLAUDE.md` imports them with `@AGENTS.md`. Put detailed area-specific guidance under `docs/` and say when to read it. Never demote an always-applicable rule to an on-demand docs link.
- `CODEX.md` is optional. Its absence never blocks work or review.
- New skill working records belong under `docs/generated/<skill>/`; human documentation belongs under `docs/`. Migrate existing records only when requested, using native file-copy commands and checking copy integrity before targeted structural edits. Preserve recorded knowledge with the same meaning and level of detail.
- Only invoke `hawk-knowledge-transfer` when the user explicitly requests that skill. Ordinary documentation requests do not authorize it or record migration.
- When reviewing local changes, always include Knowledge and Codex/Claude compatibility; concrete scoped defects block readiness. Only the coordinator edits shared documentation and instructions.

For skill authoring or README changes, read [authoring conventions](docs/project-rules.md).
For documentation or agent setup changes, read the [shared layout](docs/agent-instruction-layout.md)
and [working-with-agents guide](docs/working-with-agents.md).
