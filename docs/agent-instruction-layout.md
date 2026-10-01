# Thin instruction entrypoints

This is the shared Hawk convention used by Knowledge Transfer and Quick Review.
It is maintained once in `docs/agent-instruction-layout.md` in hawk-skills, then
packaged inside each consuming skill so installation does not require another
skill or an external documentation path.

## Routing

- `CLAUDE.md` contains only the actual import of the applicable `AGENTS.md`.
  A sibling wrapper uses `@AGENTS.md`; a wrapper in `.claude/` targeting root
  uses `@../AGENTS.md`. Keep imports outside code formatting and preserve case.
- `CODEX.md` is optional. Do not create or require it, and never block review
  because it is absent. If it already exists, keep only a short instruction and an ordinary Markdown link
  directing readers to the applicable `AGENTS.md`. Do not use Claude's `@`
  syntax here or assume Codex loads this file automatically. Codex's normal
  entrypoint is `AGENTS.md`; do not change global fallback settings to enforce
  this project convention.
- `AGENTS.md` is a compact routing index: instruct agents to read the named
  rule files under `docs/` before relevant work. A bare collection of links is
  insufficient; say which file must be read and when. Avoid duplicating the
  detailed policies in the index. Minimal routing text and headings are fine.
- Use maintained rule files, defaulting to `docs/project-rules.md` for common
  rules. Follow existing document names where suitable. Separate substantial
  scoped or host-specific rules only when that improves discovery; label their
  applicability explicitly. Keep detailed rules and human explanations under
  `docs/`, and factual working records under `docs/generated/<skill>/`.

Example root index:

```markdown
# Project instruction index

Before editing, read [project rules](docs/project-rules.md).
For data changes, also read [data contracts](docs/data-contracts.md).
```

This layout does not make docs automatic loader locations. `AGENTS.md` supplies
the instruction to read them. Keep essential required routes direct and bounded;
do not import all docs at startup. Pass the applicable rule contents or explicit
read requirements to delegated agents.

## Migration and maintenance

Before thinning an entrypoint, read its existing rules and all applicable scoped
overrides. Move its substantive rules into the appropriate maintained docs file,
preserving their meaning, scope, conditions, and required commands. Establish the
new routes and verify their targets before replacing the old text. Resolve real
conflicts instead of silently discarding a rule. Do not turn host-specific rules
into unconditional rules for both tools or flatten legitimate directory scope.

For scoped entrypoints, use paths relative to their containing file; retain the
same governing scope when moving a rule to docs. Global instruction files and
user settings are outside a project documentation task. Factual notes and past
build records do not acquire policy authority just because they are in docs.

Update the relevant rule document when a verified reusable rule changes. Change
entrypoints only when a route or scope changes. Human design/history belongs in
docs or existing working records, not in the pointer files.

## Review gate

For projects supporting both tools, review the applicable `CLAUDE.md`,
`AGENTS.md`, required docs targets, and the Knowledge and Codex/Claude
compatibility section. Check actual imports, file case, relative paths, routing
read requirements, preserved rules, scope, and current command/contract accuracy.
Inspect `CODEX.md` only if present; its absence is not a missing instruction route.

Missing required routes or documents, broken imports, lost or contradictory
rules, and substantive policy copied into entrypoints contrary to this declared
layout are blocking findings. Report the concrete rule or route and its effect;
do not flag line counts, headings, incidental path mentions, or wording preferences.
Check that manual material survives migration and that no rule remains available
only to one host by accident. Do not demand unused host setup in single-tool projects.

Knowledge Transfer repairs this layout within its authorized scope; Quick Review
checks it read-only. The two workflows use the same packaged specification and
report `passed`, `blocked`, or `not verified`; unresolved blockers prevent a
ready-to-commit conclusion. This is a review gate, not a Git hook.

Platform sources verified 2026-10-01:
[OpenAI instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
[Claude imports](https://code.claude.com/docs/en/memory#share-one-file-with-other-coding-tools).
