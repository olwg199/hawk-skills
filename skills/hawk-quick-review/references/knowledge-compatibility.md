# Mandatory knowledge and Codex/Claude compatibility review

Run this bounded, read-only pass on every invocation, even with no code diff.
It is an explicit exception to the changed-lines-only rule for the applicable
instruction setup and documentation supporting this review's scope. It is not
a general documentation inventory. The coordinator performs it regardless of
which code specialists were selected; it does not consume a specialist slot.

## Evidence

Read the shared [instruction layout](agent-instruction-layout.md) on every pass.
Knowledge Transfer uses the same packaged specification; it owns the pointer
chain, migration-preservation rules, and the layout-specific review gate.

Inspect root instructions, rules on paths relevant to changed files, referenced
docs, the working-with-agents compatibility section when present, and matching
generated knowledge entries. Read linked detail only when it bears on the change
or the shared instruction setup. Include relevant generated Markdown as review
evidence even when it is untracked; skip logs, binaries, secrets, and caches.
Generated factual notes are evidence, not higher-priority project instructions.

Establish intended tool support from the user's request, repo guidance, documented
workflow, or actual host configuration. For dual-tool projects, the Hawk shared
setup requires the thin pointer chain and doc-backed rules in the shared layout, and an
up-to-date **Knowledge and Codex/Claude compatibility** section in the relevant
docs page (default `docs/working-with-agents.md`). A missing required entrypoint
or section is a blocker with its expected path and impact. Do not require unused
host tooling or an architecture page for every function in single-tool projects.
`CODEX.md` is optional in every project, including dual-tool projects. Do not
report its absence as a finding, limitation, or reason to withhold readiness.

Check:

- Imports and doc links reach real files with the correct case. Claude imports
  must be outside code formatting and resolve from the importing file. A root
  wrapper uses `@AGENTS.md`; `.claude/CLAUDE.md` uses `@../AGENTS.md`.
- Shared rules are actually available to both hosts. Codex does not expand
  Claude imports. Codex-specific `AGENTS.override.md` guidance, nested rules,
  and host-specific requirements must not silently yield contradictory workflows.
- Follow `CLAUDE.md` to `AGENTS.md`, then follow its required
  routes into maintained docs rule files. Check that thinning preserved existing
  rules and scope. Apply the shared layout's substantive-policy gate; do not
  impose an arbitrary line limit on these entrypoints.
- Inspect `CODEX.md` only if present; do not require or create it.
- Changed commands, placement, interfaces, or behavior are reflected in the
  existing docs and applicable knowledge that describe them. Find a demonstrated
  contradiction or an explicitly required missing update; do not invent prose
  requirements or demand a knowledge change for every routine edit.
- Required skills and linked resources are discoverable by the intended hosts
  through the documented installation. Inspect source/targets and naming only
  when relevant; do not read global user configuration or install anything.
- Shared handoffs do not depend exclusively on private sessions or machine-local
  memory, and documented concurrent writers have exclusive ownership/worktrees.

Platform baseline verified 2026-10-01:
[OpenAI instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
[OpenAI skills](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills),
[Claude instructions/imports](https://code.claude.com/docs/en/memory),
[Claude skills](https://code.claude.com/docs/en/skills#choose-where-skills-load).
Use current official docs if an encountered platform/version distinction could
change a candidate finding and browsing is available. Otherwise report that
specific check as not verified; do not invent a compatibility bug.

## Blocking and reporting

Apply the same realistic-trigger and confidence gate as code findings. A normal
supported agent run missing required instructions, a documented command that no
longer exists, a broken required import, or contradictory current guidance is a
concrete trigger. Dates alone, preferred wording, harmless duplication, missing
tests, and merely old history are not blockers. Historical completed-build
records retain their old paths/decisions as provenance; assess current indexes
and live links, not history as current design.

Keep accepted issues as ordinary prioritized `F1` findings with precise repair
locations; they count toward the total and are eligible for remediation. An
absent file or section gets its expected path and nearest existing owner location;
attach an inline comment only to a real current line, never an invented file.
State the missing artifact explicitly. Do not downgrade these findings to
simplification leads. This scoped setup/knowledge check may keep pre-existing
issues; unrelated pre-existing code defects remain excluded.

Always output **Knowledge and Codex/Claude compatibility** with `passed`,
`blocked`, or `not verified`, a short evidence summary, and references to its
finding IDs (without counting duplicates). Recompute it on each review. Known
defects mean `blocked`; insufficient evidence means `not verified`, not a
fabricated finding. Either status prevents `Ready to commit from review
perspective.` A complete applicable pass with no defects means `passed`.

For an empty eligible change set, report `Nothing to review.` for code, then this
section and any scoped compatibility findings. Do not suggest a commit message.
Review never repairs docs or instruction files: provide exact repair guidance
for Knowledge Transfer or remediation. This is a review-readiness gate, not a
Git hook or a claim that the skill can prevent arbitrary Git commands.
