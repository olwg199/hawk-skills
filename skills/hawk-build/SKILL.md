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

Maintain one durable build record for each work item. The record is a concise, reviewable account of the task—not a transcript or private reasoning log.

## Clarify ambiguous requests

Resolve material ambiguity before acting on a user message.

- Inspect the current message, relevant recent chat context, and available project evidence before asking.
- If one reasonable interpretation is low-risk and does not materially change scope, behavior, files, output, or external state, state the assumption and continue.
- If two or more plausible interpretations would lead to materially different work, pause and ask a targeted clarification. Name the likely meanings and their practical difference; prefer “Did you mean A or B?” over “Can you clarify?”
- Use the host's questions or structured user-input tool when available. Offer 2–3 mutually exclusive choices, put the recommended interpretation first when evidence supports one, and allow a free-form answer when the host supports it. Otherwise ask the same concise question in normal chat.
- Ask only the smallest set of blocking questions. Do not repeat questions answered by the request or context, and do not treat ambiguity as permission to broaden scope or make a consequential change.

## Build record

1. Locate the repository root and create `.build/` if it does not exist.
2. For a new task, create `.build/<build-id>-<slug>.md` from [the template](assets/build-record-template.md). Use a stable lowercase `build-id` such as `bld-20260709-auth-rate-limit`; include the current branch when available.
3. For a resumed task, find the matching active record by build ID, slug, or stated goal. If several records match, ask the user which one to resume.
4. The coordinator is the only agent that edits `.build/` records. Do not place secrets, credentials, raw tool output, or chain-of-thought in a record.
5. Maintain **Current checkpoint** as a concise handoff summary after every meaningful update. It must state the active stage, last verified result, ordered next steps, and blocker (or `none`) so a later session can resume without rereading the whole record. Keep **Next steps** as the single stored handoff list; one item is enough when only one action remains.

## Project memory

Use `.codex/hawk-build.md` as concise, project-local memory for durable research that future Hawk Build calls can reuse.

1. Read it at the start of every build when present. Treat its entries as research leads, not unquestionable truth: verify facts relevant to the current task against the repository and correct entries proven stale.
2. Create or update it after the user confirms placement and architecture decisions. Update it again at finalization when implemented paths, boundaries, or verified commands differ from the plan.
3. Store only durable, verified facts:
   - architecture style and major ownership boundaries;
   - feature, shared-code, UI-component, service, validator, repository, helper, and test locations;
   - dependency direction and placement rules;
   - representative maintained features that demonstrate current conventions;
   - naming and file-organization conventions;
   - preferred targeted verification commands; and
   - project-specific file-size or decomposition conventions.
4. Keep task requirements, temporary findings, rejected approaches, implementation attempts, and other work-item history in `.build/<build-id>.md`. Never store secrets, raw tool output, copied source code, speculation, or a convention inferred from one ambiguous example in project memory.
5. Merge facts into the relevant section instead of appending a chronology. Keep the file brief, remove or replace entries proven stale, and let current repository evidence override saved memory.
6. The coordinator is the only agent that edits project memory. Record its path, status (`created`, `updated`, or `unchanged`), and a short list of durable facts changed under **Project memory** in the build record; do not duplicate the memory contents there.

Use this structure and omit empty optional bullets:

```markdown
# Hawk Build Project Map

## Architecture and boundaries
- <verified architecture or dependency rule with representative path>

## Placement
- Features:
- Shared code:
- UI components:
- Services, validators, repositories, and helpers:
- Tests:

## Reference features
- `<path>` — <convention it demonstrates>

## Verification
- `<targeted command>` — <scope>

## File organization
- <naming, size, or decomposition convention>
```

## Research and planning

Before asking the user questions, inspect relevant repository code, instructions, configuration, and tests. Read project memory when present, then inspect the nearest comparable maintained feature or subsystem. Identify the demonstrated architecture, feature and ownership boundaries, dependency direction, naming, imports, file-size conventions, test placement, and verification commands. Research external documentation only when it materially reduces uncertainty; cite URLs and short findings in the record.

Update **Research** with current behavior and evidence, constraints, candidate approaches, and rejected approaches. Keep the user-facing control surface in **Plan** so the user does not need to reconstruct the proposal from research notes. Ask only questions whose answers materially affect the outcome.

Follow the architecture demonstrated by the closest relevant maintained code, whether it is feature-based, layered, domain-based, package-based, or another established pattern. If conventions conflict, prefer the closest related feature. Ask the user only when plausible placements create materially different ownership or dependency boundaries.

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

Use `needs details` while repository evidence or requirements are missing. Move an item to `needs decision` when a material user choice remains, then to `waiting approval` when it is decision-complete. The user may approve, revise, or exclude named work-item IDs. Approval moves the item to `approved`; exclusion moves it to `excluded` without removing its title or details. A decision answer or revision returns the item to `waiting approval` unless the same user message explicitly approves the resulting wording.

By default, while any work item is unresolved (`needs details`, `needs decision`, or `waiting approval`), do not execute work items, modify their target paths, delegate implementation, run migrations, or make commits. Before that gate clears, limit read-only research to evidence needed to define scope, approach, and verification; do not perform a planned investigation or produce its deliverable under this exception. Updates to the build record and project memory permitted above remain allowed. The user may explicitly authorize staged execution of independent `approved` items while other items remain unresolved. Move implementation items through `in progress` to `done`; decision-only or investigation items may move directly from `approved` to `done` when their accepted output is complete. Once an item is approved, its content is the approved scope; later material changes follow **Plan deviations**. If the host has a native plan artifact, use it as well, but the build record remains the durable repository artifact.

## Clarity and proportionality

Prefer code that a new human or agent can locate, explain, and safely modify without hidden context. Clarity does not mean minimizing files, abstractions, or lines.

- Separate materially different responsibilities according to repository conventions. Put validation, persistence, business workflows, integrations, and focused transformations in validators, repositories, services, and helpers when those boundaries make the system easier to understand.
- Keep feature-specific modules and UI components with their feature. Put code in shared locations only when its responsibility and consumers are genuinely cross-feature. Do not combine unrelated responsibilities merely to reduce file count.
- Split UI into focused presentation components, state/hooks or view models, and interaction helpers when those concerns are substantial. Keep feature-specific subcomponents local; place genuinely generic reusable components in the established shared component or design-system location.
- Treat approximately 500 lines in a hand-written source file as a strong signal to inspect cohesion, not a hard limit. Normally decompose a UI component approaching that size. A cohesive service, repository, parser, or workflow may be larger when splitting it would obscure one understandable flow.
- For a planned large file, identify natural responsibility boundaries or briefly explain why it remains cohesive. Do not split mechanically by line count, create arbitrary fragments, or turn an unrelated large existing file into a mandatory refactor.
- Handle edge cases supported by a current caller, reachable path, contract, untrusted-input boundary, relevant platform or dependency behavior, regression, production evidence, or plausible security, privacy, corruption, or data-loss risk. Do not design behavior for a merely imaginable failure.
- When several real failures require the same outcome, prefer one clear existing error boundary such as `try/catch`, a result mapper, middleware, or a shared handler. Add guards, retries, recovery, fallbacks, or other specialized behavior only when a concrete case requires a distinct outcome. Preserve established logging, cleanup, state-restoration, and user-facing error behavior; never silently swallow failures.
- Verify representative observable outcomes rather than enumerating every theoretical cause.

## Model routing

Choose the model at the most granular level the host supports. Reserve a high-capability model for repository research, plan development and approval, architecture and interface decisions, migrations, security-sensitive work, conflict resolution, and final integration and verification.

Use a lower-cost model only for implementation that is all of the following: isolated to an owned path or subsystem, mechanically specified by the approved plan, low risk to interfaces and persisted data, and independently verifiable with focused checks. Good candidates include small presentation changes, narrowly scoped test additions, repetitive mechanical edits, and straightforward fixes with clear acceptance checks.

Do not route migrations, authentication or authorization, security controls, concurrency, persistence or data-contract changes, public API changes, cross-cutting refactors, or unresolved failures to a lower-cost model by default. Escalate a task to the higher-capability model when its scope expands, verification fails, or the implementer identifies an ambiguity that needs judgment.

In Codex hosts whose spawned-subagent interface has no model selector, this policy is guidance only: the skill cannot force different models for individual subagents. Select the model for the coordinator task through the host's model controls, and use separate, deliberately model-selected tasks only when the host supports them and the work can be safely handed off. Never claim that a model was selected for a subagent unless the host confirms it.

## Implementation and delegation

After confirmation, inspect the work for independent workstreams. Delegate only when separate ownership makes the work faster or safer; keep small or tightly coupled changes single-agent. Delegation boundaries must follow the chosen project architecture—never create extra layers, files, or ownership boundaries merely to make work delegable.

Possible workstreams include UI, API/integration, data/model or migration, tests, and focused research. Assign each implementation agent:

- the build ID and approved plan;
- a non-overlapping owned path or subsystem;
- interfaces it consumes or must preserve;
- verification it must run; and
- the instruction not to edit `.build/`, create commits, or modify files outside its scope.

Treat invocation of `hawk-build` as permission to use adaptive subagent delegation unless the user asks for a single-agent build. When the host supports subagents, launch independent agents in parallel. If delegation is unavailable, conflicts with task constraints, or the work cannot be safely partitioned, perform the work sequentially and explain that choice in **Delegated work**.

Implementation agents may edit only their owned source areas. The coordinator integrates changes, resolves cross-area conflicts, validates the combined result, and updates the build record. After every meaningful iteration, update **Current checkpoint**, then append a short entry to **Implementation iterations** with the change, outcome, verification, unsuccessful approach when applicable, and next action.

For every delegated agent, add one compact **Delegated work** entry: role, scope, outcome, changed files, verification, failed attempts, handoff notes, and whether the coordinator integrated it. Never copy agent transcripts or private reasoning.

When implementation requires a material change to approved behavior, scope, interfaces, data, risk, boundaries, or acceptance checks, set the affected work item to `needs decision` or `waiting approval` and obtain user approval before proceeding. Append the prior approved scope, proposed change, reason, effect, affected work-item IDs, and approval outcome under **Plan deviations** so history is preserved while **Work items** remains the current source of truth. Ordinary file discovery within an approved item does not require renewed approval, but record it in the implementation entry when it helps the handoff.

## Git and finalization

For each user-authorized related commit, prepare a concise subject and include this trailer:

```text
Build: <build-id>
```

Never create commits automatically. At finalization, discover related commits from this trailer and list their short SHA and subject under **Related commits**. If a commit predates the trailer convention, list it only when the user identifies it as related.

Complete **Final outcome** with delivered behavior, verification results, and a compact plan-versus-actual summary. Finalize the **Project memory** status and update `.codex/hawk-build.md` when verified outcomes changed durable project knowledge. Keep **Work items** at their final statuses and summarize material changes by linking to **Plan deviations**. Mark the record `complete` only when all authorized work the coordinator can perform and the final record are complete. Keep any outstanding local code-readiness actions only in **Current checkpoint** under **Next steps**.

At finalization, use **Next steps** only for actions required before the final review of the current local changes. Include a manual readiness prerequisite only when the coordinator cannot safely complete it within the authorized scope; state when it is needed and the observable completion result. Never list commit, push, deployment, release, or post-deployment actions. When `hawk-quick-review` is available, append exactly one review action as the final **Next steps** item. The review owns the code-readiness conclusion.

## Output

In the assistant response, state the active build record path and stage. Group work-item IDs by status, then expand only items that need details, a decision, or approval; do not copy complete items into a second stored list. For `needs details` or `needs decision`, show the targeted missing information or question. For `waiting approval`, show the item's compact fields and exact approval request. During implementation, report only material status changes, deviations, blockers, or decisions. At completion, report the record path, outcome, verification, project-memory path and status, then reproduce the ordered **Next steps** without rephrasing or creating another stored list.
