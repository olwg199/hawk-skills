# Shared Codex and Claude Code setup

Verified against official documentation on 2026-10-01. Recheck the linked
sources when installed versions or settings could affect a claim. The recommended
layout below is a project convention; the loading rules are platform behavior.

## Instructions

Use the shared [instruction layout](agent-instruction-layout.md): both host
entrypoints point to `AGENTS.md`, which explicitly routes to required docs.
This reference adds platform behavior; the shared layout owns the convention.

Codex discovers one instruction file per directory from project root to the
working directory: `AGENTS.override.md`, otherwise `AGENTS.md`, otherwise a
configured fallback. More local guidance takes precedence. Do not assume it
automatically loads `CLAUDE.md`, arbitrary docs, or all child-directory rules.
Pass relevant scoped rules explicitly to delegated agents working elsewhere.

Current Claude Code can load `AGENTS.md` natively, but discovery depends on
version and settings and on whether a project `CLAUDE.md` or `CLAUDE.local.md`
exists. The wrapper keeps shared rules available in sessions that use
`CLAUDE.md`; do not assume it makes Codex-specific overrides portable. For
scoped common rules, use a local `AGENTS.md` with a local Claude import when
needed. Inspect overrides and local rules before consolidating them.

Keep essential rules small. Link detailed docs and say when to read them;
do not import the whole documentation tree at startup. Updating files does not
prove a running session reloaded them. Verify Codex's loaded instructions in a
fresh session and Claude's memory sources with `/context` when execution is
available and appropriate.

Sources: [OpenAI instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
[Claude memory and imports](https://code.claude.com/docs/en/memory).

## Knowledge and handoff

Recommendation: keep human explanations and navigation under `docs/`, and
existing skill working records under `docs/generated/<skill>/`. These paths
are conventions enforced by the skills, not automatic loader locations.
Use a compact index to find relevant knowledge and verify it against source.

Do not depend on Claude's automatic personal memory as the shared handoff:
it is machine-local and is not a substitute for repository documentation.
Keep handoff scope, changed paths, verified results, unresolved questions, and
the next action in the existing task record. One coordinator owns shared docs
and instruction updates. Separate worktrees isolate simultaneous Codex and
Claude edits; integrate code and shared records deliberately before verification.

Sources: [Claude auto memory](https://code.claude.com/docs/en/memory#auto-memory),
[Claude parallel worktrees](https://code.claude.com/docs/en/common-workflows#run-parallel-sessions-with-worktrees).

## Reusable skills

Both tools use skill folders with `SKILL.md`, but their discovery locations and
host metadata differ. Current Codex documents project `.agents/skills/`; Claude
documents project `.claude/skills/`. For a new shared project setup, keep one
maintained skill source and expose it to each host using the project's supported
installer or packaging. Avoid two editable copies, broken links, duplicate names,
or Claude-only command injection in supposedly portable instructions.

Preserve an existing supported installation. This hawk-skills repository uses
installers for personal skill links; this research does not authorize changing
those installers or global settings. Machine-local absolute links do not make
a fresh clone or cloud checkout self-contained. Document the installation step
and intended environments instead of assuming personal skills are everywhere.
Use neutral workflow instructions and keep host-specific options in host metadata.

Sources: [OpenAI skill discovery](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills),
[Claude skill locations](https://code.claude.com/docs/en/skills#choose-where-skills-load).
