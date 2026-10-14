---
id: bld-20261014-quick-review-invocation-focus
title: Use invocation text reliably and compact Hawk Quick Review
status: complete
status_evidence: "2026-10-14 — W1–W5 done; rule-presence check, frontmatter-unchanged check, and git diff --check passed; validators could not run (PyYAML missing)"
started: 2026-10-14
updated: 2026-10-14
---

# Use invocation text reliably and compact Hawk Quick Review

## Current checkpoint

- Status owner: [Plan](#plan)
- Settled contracts: none
- Last verified: 2026-10-14 — one `$ARGUMENTS` per skill; frontmatter byte-identical to HEAD; distinctive-rule presence check passed; `git diff --check` clean; skill-creator validators not run (PyYAML not installed)

## Plan

- Risk: medium — compacting a heavily tuned 38 KB review prompt can silently drop a rule; W3 needs a rule-by-rule preservation check.

### Outcome

Text typed after `/hawk-quick-review` (and other hawk slash commands) reliably reaches the workflow as focus or directives in Claude Code and Codex, and the Quick Review prompt is noticeably smaller and easier to follow with no lost review behavior.

### Needed

- N1 — Text after `/hawk-quick-review` is used as review focus/instructions every time, distinct from the change's intent.
- N2 — The same invocation pattern applies to the other hawk skills that accept text after the command.
- N3 — Quick Review becomes smarter, clearer, and more token-efficient without losing review behavior.
- N4 — Must work in both Claude Code and Codex; the official skill validators must still pass (project verification rule).

### Decided

- D1 — Put a `$ARGUMENTS` placeholder near the top of each SKILL.md body, with a fallback to the user's message text when it is empty or shown literally (Codex) — Claude Code substitutes it in place instead of appending `ARGUMENTS:` after ~460 lines.
- D2 — Focus steers emphasis; it never suppresses serious issues outside the focus (existing behavior preserved).
- D3 — Invocation text may narrow scope with `staged` or explicit paths; out-of-scope changes are listed as not reviewed and readiness names the requested scope — user chose W4 option A on 2026-10-14.
- D4 — Do not add `argument-hint`; both validators reject it and the body placeholder is the real fix — user chose W6 option A on 2026-10-14.

### Work items

- **W1 — Quick Review invocation focus** · `done` — 2026-10-14 — early Invocation focus section and README examples in place
  - Why: N1, D1, D2.
  - Work: Add an early `## Invocation focus` section with `$ARGUMENTS` and Codex fallback. Classify the text into focus notes and run directives already supported elsewhere in the skill (single agent / sub-agents, no questions, explicit verification, explicitly included untracked files). Replace Phase 1 step 3 with a pointer; state that invocation focus is not change intent. Add a Claude Code focus example to the README.
  - Paths: modify `skills/hawk-quick-review/SKILL.md`, `README.md`.
  - Verification: `$ARGUMENTS` appears once near the top; step 2/3 wording separates intent from focus; both validators pass.
- **W2 — Same pattern in other hawk skills** · `done` — 2026-10-14 — one `$ARGUMENTS` line with fallback in each of six skills
  - Why: N2, D1.
  - Work: Add one compact invocation-text line near the top of each skill, phrased for that skill's meaning (build task, review target, findings to fix, screenshots/instructions, docs request, `--local` mode). Replace Project Review's "text after the invocation" wording.
  - Paths: modify `skills/hawk-{build,project-review,fix-review-findings,mobile-ui-builder,knowledge-transfer,skills-update}/SKILL.md`.
  - Verification: grep each file for one `$ARGUMENTS`; both validators pass; `--local` detection in skills-update still reads correctly.
- **W3 — Compact and clarify Quick Review** · `done` — 2026-10-14 — 38,060 → ~32,500 bytes; rule-presence check passed
  - Why: N3.
  - Work: State each rule once and reference it elsewhere. Merge the repeated main-agent-ownership statements; the test-suggestion rules (≥75, max 3, never findings) and simplification-lead rules (max 3, non-blocking) split between Phase 2 and Phase 3; the duplicated failing-test rule; the repeated readiness conditions; and the two output templates into one with conditional lines. Shrink the mandatory knowledge-pass section to a pointer plus the main-agent ownership, since `references/knowledge-compatibility.md` already owns the detail. Replace the project-specific false-positive examples (IIS workers, WinRM, environment state files, deployment monitoring) with the general rules they illustrate. Target roughly 24–28 KB, down from 38 KB.
  - Paths: modify `skills/hawk-quick-review/SKILL.md`; inspect `skills/hawk-quick-review/references/knowledge-compatibility.md` (no change expected).
  - Verification: rule-by-rule preservation checklist from the old file against the new file; byte count; validators; `git diff --check`.
- **W4 — Review scope directives** · `done` — 2026-10-14 — `staged`/path scope, excluded-path output line, and scoped readiness line added
  - Why: N3 ("smarter").
  - Work: Optionally let invocation text narrow what gets reviewed, e.g. `/hawk-quick-review staged` (index only) or `/hawk-quick-review only src/api`.
  - Paths: modify `skills/hawk-quick-review/SKILL.md`, `README.md`.
  - Verification: inventory commands and readiness wording cover the scoped case.
  - Why (decision): D3.
- **W5 — Record the invocation convention** · `done` — 2026-10-14 — authoring rule and project-map entry added
  - Why: N2, N4; reusable authoring fact.
  - Work: Add the `$ARGUMENTS` + fallback convention (and the frontmatter-key limitation) to the authoring rules and the project map.
  - Paths: modify `docs/project-rules.md`, `docs/generated/hawk-build/project.md`.
  - Verification: inspection.
- **W6 — `argument-hint` frontmatter** · `excluded` — 2026-10-14 — user chose option A (D4)
  - Why: N4.
  - Work: Decide whether to add Claude Code's `argument-hint` key, which only shows a hint while typing the command.
  - Paths: SKILL.md frontmatter of affected skills.
  - Verification: validator result.
  - Why (decision): D4.

### Boundaries

- Out of scope: Quick Review's review criteria, thresholds, model routing, and output contract (IDs, readiness line, commit message), except where W4 is approved; `references/` content; installers; test artifacts.
- Preserved: focus never suppresses serious issues; read-only review; mandatory knowledge/compatibility pass; Codex `$skill` invocation behavior.

### Acceptance checks

- [ ] `/hawk-quick-review <text>` puts the text in an early, labeled focus slot; Codex `$hawk-quick-review <text>` still works.
- [ ] Every rule in the old Quick Review is still present in the new one (checklist).
- [ ] Quick Review SKILL.md is materially smaller.
- [ ] Both skill-creator validators pass for every changed skill; `git diff --check` is clean.

## Research

### Current behavior and evidence

- `skills/hawk-quick-review/SKILL.md:100` defines invocation text as review focus, but no skill uses `$ARGUMENTS`; Claude Code appends `ARGUMENTS: <text>` after the final "Notes" section, ~370 lines below that rule.
- `skills/hawk-project-review/SKILL.md:37` has the same "text after the invocation" wording; `skills/hawk-skills-update/SKILL.md:26` depends on `--local`.
- Both validators (`~/.claude/.../skill-creator/scripts/quick_validate.py:42`, `~/.codex/skills/.system/skill-creator/scripts/quick_validate.py:40`) allow only `name`, `description`, `license`, `allowed-tools`, `metadata` (+ `compatibility` in Claude's), so `argument-hint` fails.
- Quick Review duplication: test-suggestion rules at lines 281–289 and 357–360; simplification leads at 252–272 and 351–359; failing-test rule at 289 and 346; main-agent ownership at 18–20, 51–53, 72, 189, 293, 326; two near-identical output templates at 382–438; knowledge-pass section 183–198 restates `references/knowledge-compatibility.md`.
- False-positive list lines 456–460 names specific infrastructure (IIS, WinRM, environment state files) from another project.

## Project memory

- Path: `docs/generated/hawk-build/project.md`
- Status: updated — 2026-10-14 — placement entry added
- Durable facts changed: skills read slash-command text through an early `$ARGUMENTS` line with Codex fallback (`docs/project-rules.md`)

## Plan deviations

- 2026-10-14 — W3 size target: planned 24–28 KB; delivered ~32.5 KB including ~2 KB of new focus/scope text. The remaining sections hold rules that appear only once, so cutting further would remove behavior. No approval change needed.
- 2026-10-14 — Verification: both skill-creator validators need PyYAML, which no local Python has. Substituted a byte-identical frontmatter check against HEAD (the validators only inspect frontmatter).

## Delegated work

_None._ Coordinator works locally; edits are tightly coupled prompt text.

## Implementation iterations

- W1/W3/W4 — Rewrote `skills/hawk-quick-review/SKILL.md`: early Invocation focus (scope, directives, focus notes); merged duplicate ownership, test-suggestion, simplification, failing-test, and readiness rules; one conditional output template; knowledge-pass section reduced to a pointer; project-specific false positives generalized. Original saved outside the repo for comparison; presence check of 50 distinctive rule terms found none missing.
- W2 — Added the invocation line to build, project-review, fix-review-findings, mobile-ui-builder, knowledge-transfer, and skills-update.
- W5 — Updated `docs/project-rules.md`, `docs/generated/hawk-build/project.md`, and README examples.
- 2026-10-14 review fix (F1) — Path scope now requires explicit limiting wording ("only", "just", "limit to"); a path mentioned without it is focus, and chat context never sets scope. Updated the matching README sentence.

## Final outcome

Text after any hawk slash command now lands in an early, labeled `$ARGUMENTS` slot instead of being appended after the whole skill, with a fallback for Codex. Quick Review sorts that text into scope (`staged`, paths), run directives, and focus notes; only scope narrows the review. Quick Review is ~15% smaller with the same rules. Plan vs actual: all approved items delivered; size target and validator run deviated as recorded above. Not yet exercised end to end: a live `/hawk-quick-review <text>` run.
