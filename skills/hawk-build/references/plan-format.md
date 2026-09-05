# Plan format

Read when creating or materially revising a plan. Keep the existing full plan structure for every build.

Scale content to the task: a small change can use one work item and brief fields. Do not create research work merely to fill the structure. When durable architecture, contracts, or reusable patterns change, add a knowledge-maintenance item using [project knowledge and history](knowledge.md); otherwise leave project knowledge unchanged. The routine final history-index entry does not need its own work item.

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
