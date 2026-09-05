---
name: hawk-build
description: >-
  Run a durable build lifecycle for a feature, fix, refactor, or technical
  investigation: research the task, refine and save a confirmed plan, implement
  it with adaptive subagent delegation when useful, and finalize a repository
  Markdown build record. Use only when the user explicitly invokes or names
  `hawk-build`, including `$hawk-build` and `/hawk-build`. Do not auto-trigger
  from an ordinary request to research, plan, implement, fix, refactor,
  investigate, document, or delegate engineering work when that skill name is
  absent.
---

# Hawk Build

Maintain one durable build record per task: research, confirmed plan, implementation, verification, and handoff. The coordinator alone edits records and project memory. Never store secrets, raw tool output, transcripts, or private reasoning there. User instructions and existing authorization take precedence.

## Start and resume

Locate the repository root. Create `.build/<build-id>-<slug>.md` from [the template](assets/build-record-template.md) for a new task, with a stable lowercase ID and current branch. Resume by ID, slug, or goal; ask which record only if several match.

On resume, read **Current checkpoint**, **Plan**, and the relevant work items first; for large plans, read shared requirements and contracts plus active items. Read historical research, deviations, or iterations only to resolve a specific uncertainty. Verify relevant current repository state before relying on the checkpoint. Do not reread unchanged skill references or files already available in context.

Inspect the request, recent context, and repository evidence before asking questions. State a low-risk assumption and proceed when one interpretation is reasonable. Ask the smallest targeted question when plausible interpretations materially change the work; do not repeat answered questions.

## Research and context budget

Read the relevant sections of `.codex/hawk-build.md` when present; treat them as leads and verify task-relevant facts. Inspect enough code, instructions, configuration, and tests to identify affected behavior, owning code, relevant contracts, one nearest maintained comparable implementation when available, and verification commands. Stop when scope, approach, and verification are supported. Expand only for an unresolved dependency, conflicting evidence, or concrete risk; do not inventory unrelated architecture. Research external documentation when it materially reduces uncertainty; retain URLs and short findings.

Use targeted searches and bounded source sections instead of whole-file dumps. Broaden reads when surrounding control flow or contracts matter. Summarize checks with command, outcome, and relevant failure excerpts. Keep needed large logs in temporary artifacts outside the record, without secrets; link them and retain enough summary to resume if they expire. Do not rerun successful checks without changed code or evidence that justifies it.

Store current behavior, evidence, constraints, and material alternatives in **Research** once; keep requirements and decisions in **Plan**.

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

Keep `.codex/hawk-build.md` as a brief verified map of architecture, ownership and placement, reference features, naming/decomposition conventions, and targeted verification commands. Aim for at most 500 words; replace redundant or stale entries before growing it, and link existing project documentation for detail. Read headings and relevant sections if an existing map is longer; do not trim unrelated knowledge just to meet the target.

Create or update memory after confirmed placement/architecture decisions and at finalization only when durable facts changed. Merge facts by topic; no task history, copied code, speculation, or conventions inferred from one ambiguous example. Current repository evidence wins. Record memory path, `created`/`updated`/`unchanged`, and changed facts briefly under **Project memory**, without duplicating the map.

## Finalization and output

Never commit automatically. For user-authorized commits or finalization, read [git and finalization](references/finalization.md). Complete authorized work and verification before marking the record complete; preserve the final review handoff.

In responses, give record path and stage, group item IDs by status, and expand only unresolved items. Show targeted questions for missing details/decisions and compact fields plus an exact approval request for items awaiting approval. During implementation report material changes, deviations, blockers, or decisions. At completion give outcome, verification, memory path/status, and reproduce the ordered **Next steps** exactly.
