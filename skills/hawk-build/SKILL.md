---
name: hawk-build
description: >-
  Run a durable build lifecycle for a feature, fix, refactor, or technical
  investigation: research the task, refine and save a confirmed plan, implement
  it with adaptive subagent delegation when useful, and finalize a repository
  Markdown build record. Use when asked to start a build, research before
  building, plan and implement a task, record failed approaches, resume a build,
  delegate UI/API/data work, or finalize documented engineering work.
---

# Hawk Build

Maintain one durable build record for each work item. The record is a concise, reviewable account of the task—not a transcript or private reasoning log.

## Build record

1. Locate the repository root and create `.build/` if it does not exist.
2. For a new task, create `.build/<build-id>-<slug>.md` from [the template](assets/build-record-template.md). Use a stable lowercase `build-id` such as `bld-20260709-auth-rate-limit`; include the current branch when available.
3. For a resumed task, find the matching active record by build ID, slug, or stated goal. If several records match, ask the user which one to resume.
4. The coordinator is the only agent that edits `.build/` records. Do not place secrets, credentials, raw tool output, or chain-of-thought in a record.
5. Maintain **Current checkpoint** as a concise handoff summary after every meaningful update. It must state the active stage, last verified result, next action, and blocker (or `none`) so a later session can resume without rereading the whole record.

## Research and planning

Before asking the user questions, inspect relevant repository code, instructions, configuration, and tests. Research external documentation only when it materially reduces uncertainty; cite URLs and short findings in the record.

Update **Research** with the goal, current behavior, evidence, constraints, candidate approaches, and explicit open questions. Ask only questions whose answers materially affect the outcome. Record decisions and rejected approaches as they are resolved.

Draft a decision-complete plan in **Confirmed plan**: intended behavior, key interfaces or data changes, implementation approach, failure handling where relevant, and acceptance checks. Iterate with the user until they explicitly confirm it.

Do not edit application code, delegate implementation, run migrations, or make commits before confirmation. Save the confirmed plan verbatim with its confirmation date. If the host has a native plan artifact, use it as well, but the build record remains the durable repository artifact.

## Model routing

Choose the model at the most granular level the host supports. Reserve a high-capability model for repository research, plan development and approval, architecture and interface decisions, migrations, security-sensitive work, conflict resolution, and final integration and verification.

Use a lower-cost model only for implementation that is all of the following: isolated to an owned path or subsystem, mechanically specified by the approved plan, low risk to interfaces and persisted data, and independently verifiable with focused checks. Good candidates include small presentation changes, narrowly scoped test additions, repetitive mechanical edits, and straightforward fixes with clear acceptance checks.

Do not route migrations, authentication or authorization, security controls, concurrency, persistence or data-contract changes, public API changes, cross-cutting refactors, or unresolved failures to a lower-cost model by default. Escalate a task to the higher-capability model when its scope expands, verification fails, or the implementer identifies an ambiguity that needs judgment.

In Codex hosts whose spawned-subagent interface has no model selector, this policy is guidance only: the skill cannot force different models for individual subagents. Select the model for the coordinator task through the host's model controls, and use separate, deliberately model-selected tasks only when the host supports them and the work can be safely handed off. Never claim that a model was selected for a subagent unless the host confirms it.

## Implementation and delegation

After confirmation, inspect the work for independent workstreams. Delegate only when separate ownership makes the work faster or safer; keep small or tightly coupled changes single-agent.

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

Complete **Final outcome** with delivered behavior, verification results, remaining follow-ups, and a compact plan-versus-actual summary. Keep the confirmed plan unchanged; summarize deviations by linking to their existing entries. Mark the record `complete` only when the requested work and final record are both complete.

## Output

In the assistant response, state the active build record path and stage, then give only the next material result or question. At completion, report the record path, outcome, verification, and any follow-ups.
