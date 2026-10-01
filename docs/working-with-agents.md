# Working with Codex and Claude Code

Use the same repository rules and documentation with either tool. The thin
[CLAUDE.md](../CLAUDE.md) points to
[AGENTS.md](../AGENTS.md), which tells agents when to read
[project rules](project-rules.md) and other relevant docs. The shared
[instruction layout](agent-instruction-layout.md) defines this chain. Detailed
rules live in docs rather than being copied into the entrypoints.

## Knowledge and Codex/Claude compatibility

Verified against source and official docs on 2026-10-01; instruction and file
checks are static, not proof that both CLIs executed this checkout.

- **Instructions:** Codex discovers `AGENTS.md` and gives scoped override files
  precedence. Claude supports imports relative to their containing file. Keep
  its import outside code formatting. Check applicable scoped rules before
  work or delegation; do not assume overrides work identically in both tools.
  `CODEX.md` is optional, not Codex's default automatic loader file. Do not
  create or require it; a missing `CODEX.md` never blocks review.
  `AGENTS.md` must explicitly require reading named docs; bare links do not load them.
- **Knowledge:** human explanations live under `docs/`. Existing skill memory,
  design notes, and task records live under `docs/generated/<skill>/` with their
  original formats. The generated-folder README explains ownership. Read only
  relevant notes and verify their claims against source.
- **Skills:** source lives under `skills/hawk-*/`. This repository's installers
  create personal links for Claude Code and Codex. Install on each machine;
  these local links do not make a fresh clone or cloud environment self-contained.
  Current project skill discovery uses `.agents/skills/` in Codex and
  `.claude/skills/` in Claude. That distinction is documented here; it does not
  change this repository's existing installer destinations.
- **Handoff:** use existing build records for task status, verified results,
  unresolved issues, and next actions. Do not depend on private chat history or
  Claude's machine-local automatic memory as the only project knowledge.
- **Concurrent work:** separate Codex and Claude writers with worktrees or
  exclusive paths. One coordinator integrates changes and owns shared docs,
  records, and instruction edits. Pass relevant scoped rules to every delegate.
- **Review:** Quick Review always reports this compatibility status. Concrete
  missing instructions, stale current knowledge, broken imports, or unsupported
  documented setup are blocking findings. An incomplete check also prevents
  readiness. Review does not repair files or install a Git hook.

Sources: [OpenAI instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
[OpenAI skills](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills),
[Claude instructions and imports](https://code.claude.com/docs/en/memory#share-one-file-with-other-coding-tools),
[Claude skills](https://code.claude.com/docs/en/skills#choose-where-skills-load),
[Claude parallel worktrees](https://code.claude.com/docs/en/common-workflows#run-parallel-sessions-with-worktrees).

## Maintain documentation

Run `hawk-knowledge-transfer` for a named area or the whole project when wanted.
It updates human explanations, links, shared instructions, and the compatibility
section from verified evidence, preserving manual content and existing working
records. Writing skills maintain affected reusable rules in docs; reviews report
gaps without editing files. No timestamp-only update or new memory format is required.

Knowledge Transfer and Quick Review package the same instruction-layout source.
Edit `docs/agent-instruction-layout.md` and run
`python3 scripts/sync-agent-instructions.py --write` to update their copies;
`--check` detects drift. Each installed skill carries its own copy so neither
depends on the other being installed or on a path outside its skill folder.

## Verification and installation

Validate changed skills with the active Skill Creator's
`scripts/quick_validate.py <skill-folder>` and run `git diff --check`.
When changing shared layout or packaged references, also run
`python3 scripts/sync-agent-instructions.py --check`.
Check documentation links and the Claude import target. These checks do not
prove either host loaded the latest instructions. When checking runtime loading,
start a fresh Codex session and inspect instruction sources; in Claude use
`/context` to inspect memory files.

For local skill installation or newly added skills, use the platform commands in
the [installation guide](../README.md#install), or `/hawk-skills-update --local`
through an already installed update skill. The installers discover skill folders;
new skill source does not require changing their implementation.
