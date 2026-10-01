# Delegation

Read only when independent workstreams justify delegation or a model-routing decision is needed. Keep small or tightly coupled builds single-agent. Never change architecture just to partition work.

## Task packet

Use fresh agent context when the host supports it; avoid inheriting the conversation or loading the complete build record. Supply only:

- build ID and assigned approved work-item ID, objective, and acceptance requirements;
- non-overlapping owned paths or subsystem, with relevant repository instructions;
- required interfaces, dependencies, and constraints, including related decisions needed for this work;
- focused verification commands or evidence;
- prohibitions on editing shared instruction files, `docs/generated/`, project memory, other owned areas, creating commits, or mutating test artifacts unless the user directly and explicitly asked for that test change in this task. A failing test never authorizes mutation.

The packet must be self-contained enough to execute safely. Include a necessary cross-item contract rather than the entire approved plan. If fresh context is unavailable, still keep the assignment focused. Agents may inspect relevant source and ask for missing contracts; they must escalate material ambiguity or scope changes to the coordinator.

Launch independent agents in parallel when supported. The coordinator owns integration, conflict resolution, combined verification, and record updates. Agents return a concise summary of changes and paths, verification results, and unresolved issues. Include a failed attempt only when it changes the next approach or prevents repetition; omit transcripts and routine progress narration.

Under **Delegated work**, record role, work-item ID, owned scope, result, verification, and integration status once. Reference this entry from **Implementation iterations** instead of repeating its contents. Retain changed paths or handoff details only when not already captured by the work item or needed to resume.

## Model routing

Choose the model at the most granular level the host supports. Reserve a high-capability model for repository research, plan development and approval, architecture and interface decisions, migrations, security-sensitive work, conflict resolution, and final integration and verification.

Use a lower-cost model only for implementation that is all of the following: isolated to an owned path or subsystem, mechanically specified by the approved plan, low risk to interfaces and persisted data, and independently verifiable with focused checks. Good candidates include small presentation changes, repetitive mechanical edits, and straightforward fixes with clear acceptance checks. Delegate test-artifact work only when the user's request explicitly included it and the task packet states the exact requested change. Escalate failing tests to the coordinator; do not let an implementer rewrite or delete a test artifact to make verification pass.

Do not route migrations, authentication or authorization, security controls, concurrency, persistence or data-contract changes, public API changes, cross-cutting refactors, or unresolved failures to a lower-cost model by default. Escalate a task to the higher-capability model when its scope expands, verification fails, or the implementer identifies an ambiguity that needs judgment.

In Codex hosts whose spawned-subagent interface has no model selector, this policy is guidance only: the skill cannot force different models for individual subagents. Select the model for the coordinator task through the host's model controls, and use separate, deliberately model-selected tasks only when the host supports them and the work can be safely handed off. Never claim that a model was selected for a subagent unless the host confirms it.
