---
name: hawk-build
description: >-
  Build a feature, fix, refactor, or technical investigation with a lightweight
  path for clear localized changes and a full research, approved-plan,
  implementation, and verification lifecycle for complex work. Preserve a
  durable outcome proportional to the task. Use only when the user explicitly invokes or names
  `hawk-build`, including `$hawk-build` and `/hawk-build`. Do not auto-trigger
  from an ordinary request to research, plan, implement, fix, refactor,
  investigate, document, or delegate engineering work when that skill name is
  absent.
---

# Hawk Build

Maintain a durable outcome for each task, proportional to its uncertainty and consequences. The coordinator alone edits records and project memory. Never store secrets, raw tool output, transcripts, or private reasoning there. User instructions and existing authorization take precedence. Never commit automatically.

## Choose the path

Use the lightweight path when the requested outcome is clear, the change is localized to understood behavior, an established pattern applies, and there is no material interface, persistence, security, or architectural change. Decide from the request and a focused look at the owning code, not a separate discovery exercise. File count alone does not determine the path. Use the full lifecycle for other tasks, an explicit request for a plan/full build record, or an existing full build being resumed.

### Lightweight path

Inspect applicable instructions and the owning code, make the authorized change, and run focused verification plus required repository checks. Apply the research and context-budget practices below, but load project knowledge only when needed. Work locally; skip the full template, plan approval, work-item statuses, milestone logs, and lifecycle references. Do not request approval again for a clear change the user already authorized.

At completion, upsert one short entry in `.build/index.md` with a stable lowercase build ID, date/title, status, request/outcome, changed paths, verification result, and unresolved issue or `none`. Include useful keywords in the title or outcome. This entry is the lightweight build record and history summary; no separate build file or self-link is needed. If pausing before completion, save the same entry with an incomplete status and the next action. On resume, read that entry and verify relevant current state. Report outcome, verification, unresolved issues, and the index path without full-lifecycle status fields.

Escalate when a concrete uncertainty or risk invalidates the lightweight criteria, or durable design knowledge needs to change or be corrected. Preserve completed changes and verification in a full build record under the same ID, replace the index entry with a pointer, and plan the remaining work before proceeding with it. Do not redo settled research or treat completed work as awaiting retroactive approval. A routine fixable verification failure alone does not require escalation; an unexplained failure that changes the approach may.

The remaining lifecycle requirements apply to full builds; lightweight builds share only the research/context practices and repository, authorization, and commit constraints described above.

## Start and resume

Locate the repository root. Create `.build/<build-id>-<slug>.md` from [the template](assets/build-record-template.md) for a new task, with a stable lowercase ID and current branch. Resume by ID, slug, or goal; ask which record only if several match.

On resume, read **Current checkpoint**, shared plan requirements and contracts, and active work items first. Read other work items only when their dependencies matter. Read historical research, deviations, or iterations only to resolve a specific uncertainty. Verify relevant current repository state before relying on the checkpoint. Do not reread unchanged skill references or files already available in context.

Inspect the request, recent context, and repository evidence before asking questions. State a low-risk assumption and proceed when one interpretation is reasonable. Ask the smallest targeted question when plausible interpretations materially change the work; do not repeat answered questions.

## Research and context budget

Default to narrow research. Read applicable repository instructions and search relevant entries in `.codex/hawk-build.md`, the project-knowledge index. Load a linked design note only when it helps resolve this task, then inspect the current owning code and nearest relevant verification. Notes explain architecture; current source establishes the behavior being changed. Missing knowledge is not a reason to scan the repository or initialize every category.

Stop once change location, approach, and verification are supported. After roughly 3–5 targeted reads, reassess whether those questions are answered; this is a checkpoint, not a hard cap. Before expanding research, name the unresolved question that could change the plan and the next focused lookup. Inspect contracts, configuration, callers, or a comparable implementation only when needed to answer it. Research external documentation when it materially reduces uncertainty; retain URLs and short findings. Do not collect evidence merely to fill record fields.

Consult build history only for a specific question about a prior decision or regression that current code and design notes do not answer. Search `.build/index.md` by concepts, keywords, symbols, and paths; open a matching full build only when its summary is insufficient. These are optional retrieval steps, not a checklist to exhaust.

Use targeted searches and bounded source sections instead of whole-file dumps. Narrow excessive search results before loading them; broaden reads when surrounding control flow or contracts matter. Summarize checks with command, outcome, and relevant failure excerpts. Keep needed large logs in temporary artifacts outside the record, without secrets; link them and retain enough summary to resume if they expire. Start with focused verification, broaden for evidenced risk or repository requirements, and do not rerun successful checks without changed code or evidence that justifies it.

Store current behavior and evidence in **Research** once; keep requirements, constraints, and decisions in **Plan** and reference them rather than restating them. Small changes may need only a few evidence bullets and one work item. Omit empty optional research sections.

## Plan and approval

When creating or materially revising a plan, read [plan formatting](references/plan-format.md). Preserve **Outcome**, optional **Risk**, **Needed**, **Decided**, **Work items**, **Boundaries**, and **Acceptance checks** directly after the checkpoint. Use the host's native plan when available; the record remains authoritative.

Each work-item heading owns its status: `needs details`, `needs decision`, `waiting approval`, `approved`, `in progress`, `done`, or `excluded`. Missing evidence means `needs details`; a material user choice means `needs decision`; decision-complete items await approval. Users can approve, revise, or exclude named IDs. Keep excluded items. A decision answer or revision returns an item to `waiting approval` unless the same message approves the result.

While any item is unresolved, do not execute items, edit target paths, delegate implementation, run migrations, or commit. Limit read-only research to defining scope, approach, and verification; do not perform a planned investigation or deliver its output under that exception. Permitted record and memory updates remain allowed. Only explicit staged authorization allows independent approved items to proceed while others remain unresolved.

Move approved implementation through `in progress` to `done`; approved investigation or decision items may move directly to `done` when their accepted output is complete. Material changes to approved behavior, scope, interfaces, data, risk, boundaries, or acceptance checks require renewed approval: set affected items to `needs decision` or `waiting approval`. Preserve prior scope, proposed change, reason, effect, item IDs, and approval outcome under **Plan deviations**. Routine file discovery within approved scope needs no renewed approval.

## Implementation

Follow the closest maintained architecture, ownership, dependency direction, and placement conventions. Separate substantial responsibilities and UI presentation, state, and interactions; share code only across actual consumers. Around 500 handwritten lines signals a cohesion check, especially for UI, not a mandatory split or unrelated refactor. Handle evidenced edge cases and plausible security, privacy, corruption, or data-loss risks. Prefer established error boundaries; add specialized recovery only for distinct required outcomes. Preserve logging, cleanup, and user-facing failures. Verify representative observable outcomes.

Invocation permits adaptive subagents unless the user requests single-agent work. Delegate only when independent ownership improves speed or safety; read [delegation and model routing](references/delegation.md) only then or when routing models. Otherwise implement locally and note the reason briefly under **Delegated work**. The coordinator integrates and verifies the combined result.

## Checkpoints and memory

Update the record at milestones: plan approval, work-item start or completion, material deviation, blocker, final verification, or handoff before pausing. Batch routine edits and checks; do not append an entry per tool call or minor iteration. Keep **Current checkpoint** concise: stage, last verified result, ordered **Next steps**, and blocker or `none`. Store pending actions only in **Next steps**.

For implementation milestones, append a short **Implementation iterations** entry with item ID, change, result, and verification, referencing evidence already recorded. Retain failed attempts only when they change the approach or prevent repetition. Do not repeat delegation reports or the pending-action list.

Use `.codex/hawk-build.md` as a small index into focused design notes under `.codex/hawk-build/design/`. Read [project knowledge and history](references/knowledge.md) when planning a knowledge update, maintaining these records, or resolving their freshness. Create notes only for useful verified knowledge; preserve existing maps and adopt the index incrementally. Consult relevant entries, not every note or past build.

When durable architecture, contracts, or reusable patterns will change, include a knowledge-maintenance work item in the plan. Complete it after implementation and relevant verification, updating affected notes and index entries. Routine changes following an existing pattern need no new note. Record knowledge paths, `created`/`updated`/`unchanged`, and a brief description of changed facts under **Project memory**, without copying the notes.

A checkpoint must support continuation: approved scope and active item IDs, settled contracts or links, last verified result, references to unresolved work-item questions, and ordered next steps. Reference existing plan fields rather than duplicating them. Summaries do not remove earlier reads from the active conversation. Prevent unnecessary loading first; use the checkpoint after host compaction or an authorized fresh-context handoff. Do not claim to clear context, force compaction, or create a new task without user authorization.

## Finalization and output

Never commit automatically. For user-authorized commits or finalization, read [git and finalization](references/finalization.md). Complete authorized work and verification before marking the record complete; preserve the final review handoff.

In responses, give record path and stage, group item IDs by status, and expand only unresolved items. Show targeted questions for missing details/decisions and compact fields plus an exact approval request for items awaiting approval. During implementation report material changes, deviations, blockers, or decisions. At completion give outcome, verification, memory path/status, and reproduce the ordered **Next steps** exactly.
