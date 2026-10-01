# Project rules

- Personal skills in this repo must use the `hawk-` prefix for folder names, `name:` frontmatter, and documented slash commands.
- In the README, order feature skills by development lifecycle: general build work, specialized build work, review, then review remediation. Add new feature skills at their matching workflow stage; document update management after installation, outside that lifecycle.
- When changing install or update behavior, update both `install.sh` and `install.ps1` in the same change unless the change is explicitly platform-specific.
- Keep the installers behaviorally equivalent where possible, but use native platform mechanisms: Bash for macOS/Linux and PowerShell for Windows. Do not make the Windows installer depend on Bash, Git Bash, or WSL.
- Installer cleanup must only remove links or tracked copies created by this repo, and must leave unrelated user skills alone.
- Keep existing skill working records under `docs/generated/<skill>/`; human documentation belongs under `docs/`. Preserve record formats, IDs, and historical facts when relocating them.
- Keep `CLAUDE.md` as a pointer to `AGENTS.md`. `CODEX.md` is optional; inspect it only if present, never create it as a requirement or block review because it is absent. Keep `AGENTS.md` as a short index directing agents to required rule files under `docs/`, rather than storing detailed rules in the entrypoints.
- When reviewing local changes, always include Knowledge and Codex/Claude compatibility; concrete scoped defects block readiness. Only the coordinator edits shared documentation and instructions.
- The canonical instruction layout is `docs/agent-instruction-layout.md`. Update it once, then run `python3 scripts/sync-agent-instructions.py --write` to refresh the packaged Knowledge Transfer and Quick Review references. When changing this layout or its packaged references, `python3 scripts/sync-agent-instructions.py --check` must pass before readiness.
