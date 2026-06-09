# hawk-skills Agent Notes

- Personal skills in this repo must use the `h-` prefix for folder names, `name:` frontmatter, and documented slash commands.
- When changing install or update behavior, update both `install.sh` and `install.ps1` in the same change unless the change is explicitly platform-specific.
- Keep the installers behaviorally equivalent where possible, but use native platform mechanisms: Bash for macOS/Linux and PowerShell for Windows. Do not make the Windows installer depend on Bash, Git Bash, or WSL.
- Installer cleanup must only remove links or tracked copies created by this repo, and must leave unrelated user skills alone.
