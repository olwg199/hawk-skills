<!-- Packaged from docs/code-clarity.md in hawk-skills. Edit that source and run scripts/sync-agent-instructions.py --write. -->

# Clear code

How Hawk skills and agents write, simplify and review code so a human or agent can find it, explain it and change it
safely: when to make a method, when to split, where errors are handled and what comments are for. It applies the same
way in Claude Code and Codex.

## Core rules

- **Clear, not short:** easy to find, explain and change safely. A simplification names what gets easier (fewer jumps,
  no duplication, fewer branches), never only "shorter".
- **Structure:** follow the project's architecture, naming and placement; reuse a nearby helper; share code only when
  two or more callers use it. Split by responsibility (presentation, state, interaction, data access), never by line
  count (about 500 lines: check cohesion).
- **New helper methods:** only for code used in two or more places with one meaning, or for a responsibility with logic
  of its own (a validator, a mapping), never a single condition. A check used once stays inline, with a named local
  variable (`isExpired = …`) if unclear. No near-identical methods.
- **Errors:** at the project's existing boundary; a guard, retry or fallback only where a reachable case needs another
  outcome; never swallowed silently.
- **Comments:** none unless the user or the project's rules ask; write code that needs none (names that say why, a test
  that guards odd behavior, the reason in the docs). Allowed: documentation comments (XML, docstrings, JSDoc) on request
  (what it does, inputs with units, what it returns, when it fails); comments a tool reads (lint, type, pragma,
  license), which are code; a one-line `TODO:` where a skill or the user asks for it. Existing comments stay unless
  your change makes them wrong.
