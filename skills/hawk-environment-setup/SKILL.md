---
name: hawk-environment-setup
description: >-
  Set up or update the owner's personal agent environment (global Claude and Codex rules, the no-AI-in-commits and PR
  hooks, Claude settings, git hooks) from the hawk-skills environment folder, on this computer. Use only when the user
  asks to set up, sync, update, check or repair their environment or global rules, or invokes `$hawk-environment-setup`
  or `/hawk-environment-setup`. Do not use for updating the skill set (that is hawk-skills-update) or for project-level
  rules (that is hawk-project-rules-review).
---

# Hawk Environment Setup

Invocation text: $ARGUMENTS

If that line is empty or shows a literal placeholder (for example in Codex), use any text after the skill name in the
user's message. It may say `check` (report only) or nothing (update and apply).

The hawk-skills repository keeps the owner's environment in `environment/`: `rules.md` (rules for both agents),
`claude/rules.md` and `codex/rules.md` (what one agent alone needs), `claude/hooks/` (the Claude Code PR hook),
`git-hooks/` (the commit message check and wrappers for repository hooks) and `tests/`. Besides copying files, it merges
`~/.claude/settings.json` and sets git `core.hooksPath` and `core.autocrlf input`. `environment/install.ps1`
(Windows) and `environment/install.sh` (macOS, Linux) call `environment/environment.py`, which does all the work. This
skill runs it and reports; it never edits home files by hand. The hawk-skills installer only links skills and never
applies the environment, so other users of these skills are not affected unless they run this skill.

## Steps

1. **Find the repository.** Read `~/.hawk-skills-repo` (saved by the hawk-skills installer). If it is missing, ask the user
   where hawk-skills is cloned.
2. **Update.** If `git status --short -- environment` is empty, run `git pull --ff-only` in the repository. If there are
   uncommitted changes there, or the pull cannot fast-forward, do not pull, merge or rebase: say so and continue with the
   files as they are. Do not run the hawk-skills installer here.
3. **Check.** Run the environment installer with `check` (`environment/install.ps1 -Mode check` or
   `environment/install.sh check`). Each home file is `ok`, `missing`, `outdated` (apply updates it) or `CHANGED` (edited at
   home, or not written by this skill); `CHANGED` can also name a hooks folder that is a link (nothing is written through
   it) or another git `core.hooksPath` or `core.autocrlf`. `SETTINGS` means `~/.claude/settings.json`
   cannot be read; `PRIVATE` names a line in `environment/` that identifies this computer.
4. **Decide on `CHANGED` items.** For each one, show the user what it holds that the repository version does not (for a
   rule file, the rules missing from the repository version; for a hook, what it does), then ask in the question shape of
   the report format, in its all / one by one / none layout:
   - **Replace all** (recommended), **one by one** (then one "Replace: <item>" option per item, multi-select), or
     **Keep all for now**. With one item: "Replace: <item>" or "Keep it for now".
   - A replaced item is moved to the backups, the repository version is installed, and step 8 offers back whatever is
     worth keeping.
   - A kept item is not replaced; plain apply still updates every other item, and `check` keeps reporting it.
   Never replace a home item without this confirmation.
5. **Local rules for this computer.** Each home rule file is the shared rules, then the agent's rules, then this computer's
   own rules from `~/.hawk-environment/local/claude.md` and `codex.md` (tool paths, installed apps, MCP servers). These
   never go into git. When `check` notes one as missing, or the user asks to refresh it:
   - **Research:** look at this computer for what the rules should say: MCP servers registered in `~/.claude.json` and
     `~/.codex/config.toml`, local AI tool folders and their README (ComfyUI, model folders), image editors (GIMP with its
     MCP server), and anything the other computer's rules mentioned that the user names.
   - **Propose and ask:** write the proposed local rules in the chat, then ask in the question shape of the report format
     (what was found, what each rule would say), in its all / one by one / none layout with one "Apply: …" option per
     proposed rule. Never guess a path you did not see.
   - **Write** the confirmed text to the local file.
6. **Compare local rules with the global ones.** On every run except `check`, read the shared rules
   (`environment/rules.md`) and the agent's rules (`environment/<agent>/rules.md`), then judge every rule in
   `~/.hawk-environment/local/claude.md` and `codex.md` as [rules comparison](references/rules-comparison.md) describes.
   Local rules hold only what is specific to this computer, so Belongs elsewhere here means a general working rule that
   could go into the shared rules (a suggestion, never written there by this step).
   - When every rule is Keep, say so in one line and go on.
   - Otherwise write the findings and ask about the planned removals and moves in the all / one by one / none layout,
     one option per change ("Apply: remove <rule>", "Apply: move <rule> to <file>"). Each Contradiction gets its own
     single-choice question: "Apply: remove the local rule" or "Apply: mark it as a deliberate override because
     <reason>".
   - For what the user picked: replace `~/.hawk-environment/local.bak/` with a copy of `~/.hawk-environment/local/`
     (remove the old copy if it exists: `Remove-Item -Recurse -Force` or `rm -rf`; then `Copy-Item -Recurse` or
     `cp -R`), then edit the local files.
   - Check every removed rule against the shared and agent rules read above, name the rule that covers it, and put back
     any that nothing covers.
7. **Apply.** Run the environment installer with no argument (`apply`). For the items the user chose to replace, add
   `-Replace` followed by exactly those items as `check` printed them (`install.ps1 -Replace ~/.claude/CLAUDE.md
   core.hooksPath`, or `install.sh apply --replace ...`); never `-Replace` alone unless the user chose to replace every
   `CHANGED` item. Note every `backed up` line and the `old file backed up` path of `settings.json`. Then run `check`
   again: no `missing`, `outdated`, `SETTINGS`, `UNKNOWN` or `PRIVATE` line may remain, and `CHANGED` only for items the
   user chose to keep.
8. **Add back what is worth keeping.** Go through every backup from step 7:
   - **Rule files:** list the rules the installed version does not already cover (skip duplicates and rules the
     repository rules contradict; name any contradiction). For each one propose where it goes: shared
     (`environment/rules.md`, or `environment/<agent>/rules.md` when only one agent needs it) or this computer only
     (`~/.hawk-environment/local/<agent>.md`; always for paths, tool folders, installed apps and anything personal).
   - **Hooks:** a replaced git hook, or a hooks folder link (its target folder is left as it was): say what it did and
     offer it back (into `environment/git-hooks/` if shared).
   - **Settings:** compare the `settings.json` backup with the new file and list every value that changed or disappeared;
     offer each back except `includeCoAuthoredBy` and `attribution`, which the commit rule requires.
   - **Git settings:** a replaced `core.hooksPath` or `core.autocrlf` is saved in `~/.hawk-environment-state.json`; name
     it.
   Ask in the question shape of the report format, in its all / one by one / none layout with one "Apply: …" option per
   item to add back (naming where it goes), write only what the user picks, then apply and `check` again.
9. **Before proposing a commit** of changes under `environment/`, run `python -m unittest discover -s environment/tests`
   in the repository and read the `environment/` diff for private details (see Rules). Never commit or push without the
   user's approval of that commit.
10. **Report** as [report and question format](references/report-format.md) describes, in the user's language: what was
   installed, removed or backed up, which local rules were removed and which global rule covers each, what was added
   back and where, what the final check and the tests showed,
   what waits for the user (a commit of shared changes, a push), and that new sessions pick the rules up on their next
   start.

For `check` alone, run steps 1 and 3 and report.

## Rules

- Every home file is a copy, never a link: rule files, `~/.claude/hooks/hawk/` and `~/.githooks/`. Edit shared files in
  `environment/` and this computer's rules in `~/.hawk-environment/local/`, then apply; an edit made in a home copy shows
  as `CHANGED`. Other files in `~/.claude/hooks/` and the rest of the user's settings are never touched.
- **Nothing private in git.** `environment/` is published with hawk-skills: no user names, home folder paths, drive paths,
  hostnames, emails or tokens. `check` finds only this computer's user name, its home folder path and drive paths, reports
  them as `PRIVATE` and exits with an error. Before proposing a commit, also read the `environment/` diff yourself for
  hostnames, emails, tokens and other personal details. Move anything private to the local rules, and never commit or
  push while a `PRIVATE` line or such a detail remains.
- Commit messages are checked by `~/.githooks/commit-msg`, which sees the exact message. PR, issue and release text is
  checked by the Claude Code hook `~/.claude/hooks/hawk/no_ai_in_pr.py`; its settings entry runs it only when the file
  exists, so a missing script never blocks other commands.
- Before step 6 changes the local rules, the whole `~/.hawk-environment/local/` folder is copied to
  `~/.hawk-environment/local.bak/`: one copy, replaced each time step 6 changes the local rules, kept only to compare
  against; name it in the report.
- Replaced files go to `~/.hawk-environment-backups/<time>/`; mention them in the report. Never copy credentials or session
  files.
