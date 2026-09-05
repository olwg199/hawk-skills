# Full-build planning and execution

Read when starting or resuming a full build, or materially revising its plan. These procedures do not apply to the lightweight path. Use the host's native plan when available; the task record remains authoritative.

## Start and resume

Locate the repository root. Create `.build/<build-id>-<slug>.md` from [the template](../assets/build-record-template.md) for a new task, with a stable lowercase ID and current branch. Resume by ID, slug, or goal; ask which record only if several match.

On resume, read **Current checkpoint**, shared plan requirements and contracts, and active work items first. Read other work items only when their dependencies matter. Read historical research, deviations, or iterations only to resolve a specific uncertainty. Verify relevant current repository state before relying on the checkpoint.

Inspect the request, recent context, and repository evidence before asking questions. State a low-risk assumption and proceed when one interpretation is reasonable. Ask the smallest targeted question when plausible interpretations materially change the work; do not repeat answered questions.

## Plan structure

Scale content to the task: a small change can use one work item and brief fields. Do not create research work merely to fill the structure. When durable architecture, contracts, or reusable patterns change, or affected design knowledge needs correction, add a knowledge-maintenance item using [project knowledge and history](knowledge.md); otherwise leave project knowledge unchanged. The routine final history-index entry does not need its own work item.

Maintain **Plan** directly after **Current checkpoint** using this compact structure:

- **Outcome:** the intended observable result in one or two sentences.
- **Risk:** only a material plan-wide risk not already owned by one work item; omit when empty.
- **Needed:** confirmed user outcomes and constraints, separate from implementation choices.
- **Decided:** material choices already resolved, each with a brief rationale.
- **Work items:** implementation, investigation, decision, or documentation work grouped into stable IDs such as `W1`, `W2`, and `W3`.
- **Boundaries:** important out-of-scope work and behavior that must remain unchanged.
- **Acceptance checks:** end-to-end or user-observable outcomes for the complete plan.

Each work item has exactly one status: `needs details`, `needs decision`, `waiting approval`, `approved`, `in progress`, `done`, or `excluded`. The status in the work-item heading is the source of truth; do not create separate open-question, missing-detail, or approval lists in the record.

Keep every entry under **Work items** compact. Use only four core bullets: **Why**, **Work**, **Paths**, and **Verification**. **Why** references the relevant **Needed** or **Decided** IDs and adds only context not already stated there. **Work** describes the implementation, investigation, decision, or output. **Paths** lists affected or inspected paths with `inspect`, `add`, `modify`, or `remove` labels; use an expected area or pattern when exact paths are not yet known, and `none` only for genuinely non-file work. **Verification** names the focused command, inspection, or evidence for that item; keep plan-level user outcomes in **Acceptance checks**. Add **Missing** only to `needs details` items and **Decision needed** only to `needs decision` items. Add interface, data, migration, failure-handling, or item-specific risk only when it materially affects the user's decision. Group related work instead of creating an item for every mechanical edit, and do not restate research evidence, requirements, decisions, scope, or acceptance checks from another angle.

Store current behavior and evidence in **Research** once; keep requirements, constraints, and decisions in **Plan** and reference them rather than restating them. Small changes may need only a few evidence bullets and one work item. Omit empty optional research sections.

## Approval and changes

Missing evidence means `needs details`; a material user choice means `needs decision`; decision-complete items await approval. Users can approve, revise, or exclude named IDs. Keep excluded items. A decision answer or revision returns an item to `waiting approval` unless the same message approves the result.

While any item is unresolved, do not execute items, edit target paths, delegate implementation, run migrations, or commit. Limit read-only research to defining scope, approach, and verification; do not perform a planned investigation or deliver its output under that exception. Permitted record and memory updates remain allowed. Only explicit staged authorization allows independent approved items to proceed while others remain unresolved.

Move approved implementation through `in progress` to `done`; approved investigation or decision items may move directly to `done` when their accepted output is complete. Material changes to approved behavior, scope, interfaces, data, risk, boundaries, or acceptance checks require renewed approval: set affected items to `needs decision` or `waiting approval`. Preserve prior scope, proposed change, reason, effect, item IDs, and approval outcome under **Plan deviations**. Routine file discovery within approved scope needs no renewed approval.

## Implementation

Follow the closest maintained architecture, ownership, dependency direction, and placement conventions. Separate substantial responsibilities and UI presentation, state, and interactions; share code only across actual consumers. Around 500 handwritten lines signals a cohesion check, especially for UI, not a mandatory split or unrelated refactor. Handle evidenced edge cases and plausible security, privacy, corruption, or data-loss risks. Prefer established error boundaries; add specialized recovery only for distinct required outcomes. Preserve logging, cleanup, and user-facing failures. Verify representative observable outcomes.

Invocation permits adaptive subagents unless the user requests single-agent work. Delegate only when independent ownership improves speed or safety; read [delegation and model routing](delegation.md) only then or when routing models. Otherwise implement locally and note the reason briefly under **Delegated work**. The coordinator integrates and verifies the combined result.

## Checkpoints and memory

Update the record at milestones: plan approval, work-item start or completion, material deviation, blocker, final verification, or handoff before pausing. Batch routine edits and checks; do not append an entry per tool call or minor iteration. Keep **Current checkpoint** concise: stage, approved scope and active item IDs by reference to **Plan**, settled contract links, last verified result, ordered **Next steps**, and blocker or `none`. Reference unresolved work-item questions instead of copying them. Store pending actions only in **Next steps**.

For implementation milestones, append a short **Implementation iterations** entry with item ID, change, result, and verification, referencing evidence already recorded. Retain failed attempts only when they change the approach or prevent repetition. Do not repeat delegation reports or the pending-action list.

Summaries do not remove earlier reads from the active conversation. Prevent unnecessary loading first; use the checkpoint after host compaction or an authorized fresh-context handoff. Do not claim to clear context, force compaction, or create a new task without user authorization.

## Progress responses

Give record path and stage, group item IDs by status, and expand only unresolved items. Show targeted questions for missing details/decisions and compact fields plus an exact approval request for items awaiting approval. During implementation report material changes, deviations, blockers, or decisions.
