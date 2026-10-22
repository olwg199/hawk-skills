---
name: hawk-project-rules-review
description: >-
  Review one project's agent rules and agent config against the user's global rules: AGENTS.md, CLAUDE.md, CODEX.md,
  CLAUDE.local.md, nested rule files, everything they import or reference, and the project's Claude, Codex and MCP
  settings. Finds rules that repeat or contradict the global ones, stale references, layout problems and settings that
  undo global protections, then fixes the project files only after the user picks Apply. Use only when the user
  explicitly invokes or names `hawk-project-rules-review`, including `$hawk-project-rules-review` and
  `/hawk-project-rules-review`. Do not use for the global or per-computer rules (that is hawk-environment-setup), for
  migrating project knowledge (that is hawk-knowledge-transfer) or for reviewing code.
---

# Hawk Project Rules Review

Invocation text: $ARGUMENTS

If that line is empty or shows a literal placeholder (for example in Codex), use any text after the skill name in the
user's message. It may name a project folder or a narrower focus; otherwise review the git repository of the current
folder.

Compare what a project tells the agents with what the user's global rules already say, as
[rules comparison](references/rules-comparison.md) describes. Read-only until the user picks Apply; then change only the
project files the plan lists, never the global files, and never commit.

## 1. Collect the global side

Read what applies to every project on this computer, whichever exist:

- Global rules: `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`, including any files they import.
- Global agent config: `~/.claude/settings.json` (permissions, hooks, `attribution`, `includeCoAuthoredBy`), the
  user-scope `mcpServers` in `~/.claude.json`, and `~/.codex/config.toml` (MCP servers, approval and sandbox settings).

Never print secrets from these files (tokens, keys, `env` values); refer to them by name.

## 2. Collect the project side

From the git root, list each file you read:

- **Rule files:** `AGENTS.md`, `CLAUDE.md`, `CODEX.md`, `CLAUDE.local.md`, and every nested `AGENTS.md` or `CLAUDE.md`
  that `git ls-files` lists (plus untracked ones that `git status --short` shows).
- **What they reference:** every `@` import, followed to the end; every linked file under `docs/` or elsewhere in the
  project; and every path, command, script, skill or tool the rules name. List them one by one (a line can name several)
  and check each: it exists and still matches the code (for example, a named `npm run <script>` is in `package.json`, a
  named script is in the `scripts/` folder, and a documented folder layout matches the tree).
- **Agent config:** `.claude/settings.json`, `.claude/settings.local.json`, `.codex/config.toml` and `.mcp.json`.

Do not review project skills, commands or agents (`.claude/skills`, `.claude/commands`, `.claude/agents`,
`.agents/skills`), git settings, or rule files of other tools (`.cursor/rules`, `.github/copilot-instructions.md`); name
them in the report as not reviewed when they exist.

## 3. Judge

Put every project rule and setting into one category of [rules comparison](references/rules-comparison.md). Also check:

- **Layout:** `CLAUDE.md` imports `@AGENTS.md` and holds only lines that Claude alone needs; no rule lives only in
  `CLAUDE.md` or `CODEX.md`; rules that always apply are in `AGENTS.md`, and `docs/` files are linked from it with when to
  read them. A layout gap is Belongs elsewhere or Stale. A correct rule that both agents need but that lives only in
  `CLAUDE.md` is Belongs elsewhere (move it to `AGENTS.md`), never Keep.
- **Agent config:**
  - `attribution` or `includeCoAuthoredBy` that adds an AI to commits or pull requests when the global rules forbid it
    (Contradiction).
  - Permissions that allow without a prompt what the global rules make wait for approval (commits, pushes, history
    changes, deletes), and hooks that disable or bypass a global hook (Contradiction).
  - A project setting identical to the global one (Duplicate).
  - An MCP server with the same name, or the same command and arguments, as a user-scope one (Duplicate), or with the
    same name and a different command (Contradiction: say which one each agent will use).
  - `.claude/settings.local.json` and `CLAUDE.local.md` are personal to this computer: report them, and propose changes
    to them only for Contradictions.

## 4. Report and questions

Write the report as [report and question format](references/report-format.md) describes, in the user's language:

- **Scope:** the global files and the project files read, and what exists but was not reviewed.
- **Findings:** every item that is not Keep, as a full finding block.
- **Plan:** one line per change that needs no answer (fixing a Stale reference, moving a rule that Belongs elsewhere):
  file, what changes, and why. Duplicates and Contradictions are questions, not plan lines.

If there are no findings, say so and stop. Otherwise ask everything in one round, in as few question calls as the tool
allows:

- **The plan**, when it has lines: "Apply: <the plan lines>" or "Change the plan first".
- **Duplicates**, when there are any: "Apply: remove the duplicates (only I read these rules)" or "Keep the duplicates
  (others read these rules)".
- **Each Contradiction:** "Apply: remove the project rule", "Apply: mark it as a deliberate override because <reason>",
  or "Leave it for now".

## 5. Apply

Change only what the user picked:

1. Before editing, save a copy of every file you will change in a temporary folder outside the project. This works
   whatever the Git state is, and also covers ignored files such as `CLAUDE.local.md`.
2. Make the changes, keeping rule text word for word when moving it, with the agent's edit tools so line endings stay as
   the project has them.
3. Run `git diff --no-index <saved copy> <file>` for each changed file and check: every removed rule is covered by the
   named global rule, every moved rule arrived unchanged, and nothing else changed. List separately any change the
   user's own project-setup rules made (line-ending files, the `@AGENTS.md` import).
4. Report what changed per file, what was checked, what is left (contradictions left open, suggestions for the global
   rules), and that nothing is committed.
