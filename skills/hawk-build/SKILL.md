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

## Build record

1. Locate the repository root and create `.build/` if it does not exist.
2. For a new task, create `.build/<build-id>-<slug>.md` from [the template](assets/build-record-template.md). Use a stable lowercase `build-id` such as `bld-20260709-auth-rate-limit`; include the current branch when available.
3. For a resumed task, find the matching active record by build ID, slug, or stated goal. If several records match, ask the user which one to resume.
4. The coordinator is the only agent that edits `.build/` records. Do not place secrets, credentials, raw tool output, or chain-of-thought in a record.
5. Maintain **Current checkpoint** as a concise handoff summary after every meaningful update. It must state the active stage, last verified result, next action, and blocker (or `none`) so a later session can resume without rereading the whole record.

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

Update **Research** with the goal, current behavior, evidence, constraints, candidate approaches, and explicit open questions. Ask only questions whose answers materially affect the outcome. Record decisions and rejected approaches as they are resolved.

Follow the architecture demonstrated by the closest relevant maintained code, whether it is feature-based, layered, domain-based, package-based, or another established pattern. If conventions conflict, prefer the closest related feature. Ask the user only when plausible placements create materially different ownership or dependency boundaries.

Draft a decision-complete plan in **Confirmed plan**: intended behavior, key interfaces or data changes, implementation approach, proposed new and modified paths with brief placement reasons, failure handling where relevant, and acceptance checks. Iterate with the user until they explicitly confirm it.

Do not edit application code, delegate implementation, run migrations, or make commits before confirmation. Save the confirmed plan verbatim with its confirmation date. If the host has a native plan artifact, use it as well, but the build record remains the durable repository artifact.

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

When implementation requires a material plan change, obtain user approval before proceeding. Append it under **Plan deviations** with date, change, reason, and effect; never rewrite the confirmed baseline plan.

## Git and finalization

For each user-authorized related commit, prepare a concise subject and include this trailer:

```text
Build: <build-id>
```

Never create commits automatically. At finalization, discover related commits from this trailer and list their short SHA and subject under **Related commits**. If a commit predates the trailer convention, list it only when the user identifies it as related.

Complete **Final outcome** with delivered behavior, verification results, remaining follow-ups, and a compact plan-versus-actual summary. Finalize the **Project memory** status and update `.codex/hawk-build.md` when verified outcomes changed durable project knowledge. Keep the confirmed plan unchanged; summarize deviations by linking to their existing entries. Mark the record `complete` only when the requested work and final record are both complete.

## Output

In the assistant response, state the active build record path and stage, then give only the next material result or question. At completion, report the record path, outcome, verification, project-memory path and status, and any follow-ups.
