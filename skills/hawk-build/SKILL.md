---
name: hawk-build
description: >-
  Build a feature, fix, refactor, or technical investigation with a lightweight
  path for clear localized changes and a full research, approved-plan,
  implementation, and verification lifecycle for complex work. Preserve a
  durable outcome proportional to the task. Use for requests to build or
  implement a feature, fix a bug, refactor code, investigate a technical issue,
  or continue an unfinished build, including natural-language requests without
  the skill name. Also supports `$hawk-build` and `/hawk-build`. Do not trigger
  for general explanations, read-only code reviews, or standalone documentation
  requests.
---

# Hawk Build

Invocation text: $ARGUMENTS

If that line is empty or shows a literal placeholder (for example in Codex), use any text after the skill name in the user's message. It describes the task to build, fix, investigate, or resume, together with recent chat context.

Maintain a durable outcome for each task, proportional to its uncertainty and consequences. The coordinator alone edits records and project memory. Never store secrets, raw tool output, transcripts, or private reasoning there. User instructions and existing authorization take precedence. Never commit automatically.

For fixes, use the existing outcome summary to capture the symptom, confirmed cause, change, and behavior to preserve where relevant; keep verification in its existing field. Resume unfinished work under its existing ID. A new change after completion gets a new ID linking to the prior record or index entry, carrying forward only still-relevant constraints.

## Shared storage and instructions

Start both paths by reading applicable root and directory-local `AGENTS.md`,
`AGENTS.override.md`, `CLAUDE.md`, and their referenced docs rules. Read `CODEX.md`
only if present; never create or require it. Before delegation,
pass the rules governing each owned path explicitly. The coordinator alone
maintains shared instruction files and records.

Locate the target project root and create `docs/generated/` if missing. Create
its README if missing, explaining that skills maintain these working records,
humans may read them, and current source and project instructions take precedence.
Create `hawk-build/`, `design/`, and `builds/` only when their existing artifacts
are needed. Preserve record content and formats; this is a location change.

New record files use `docs/generated/hawk-build/`. Existing legacy records are
not moved or copied automatically. Resolve the active project map and history
index once: use the canonical artifact when present, otherwise its existing
legacy counterpart. Keep using that resolved path for task updates and resume;
do not create a competing record or index merely because migration is pending.
Inspect conflicting counterparts rather than silently replacing either.

Before treating needed knowledge as missing, check legacy `.codex/hawk-build.md`
and its linked notes when the new project map is absent. For a specific history
question or resume, check `.build/index.md` and matching legacy records when the
new location lacks them. Retain working links between the active index and its
records, including a new canonical full record referenced by a legacy index.
Report affected legacy paths and recommend an explicit Knowledge Transfer
migration. Record migration is separate from normal build work; only perform it
when the user requested it, using native full-file copies, equality checks before
edits, and targeted structural edits that preserve recorded knowledge.

At completion, check applicable startup instructions and docs routes. Keep
essential project-wide rules directly in `AGENTS.md`, shared by `CLAUDE.md`'s
actual import. Update detailed area-specific docs only when this task establishes
reusable facts or procedures. Keep design/history in existing knowledge records.
`CODEX.md` remains optional. Preserve host conditions and directory scope; never
demote essential rules into on-demand docs or restructure unrelated instructions.
A routine task needs no instruction rewrite. Report unresolved compatibility gaps.

## Status ownership and resume

Keep one owner for working status: an existing project plan with build steps
(such as a **Build order** table), otherwise the full record's **Work items** or
lightweight index entry. Link to the owner instead of copying its statuses.
When a project plan takes over existing work, close the record as `history`,
preserve its decisions and evidence, and point its history index entry at the
plan. Closing as history does not mean unfinished work is complete.

Use fixed work-item words: `needs details`, `needs decision`, `waiting approval`,
`approved`, `in progress`, `done`, or `excluded`. Record lifecycle words are
`research`, `planning`, `in progress`, `blocked`, `complete`, or `history`;
lightweight entries use `in progress`, `blocked`, or `complete`. Memory outcomes
use `created`, `updated`, or `unchanged`. Every status includes the check date
(`YYYY-MM-DD`) and what the check showed, for example `done — 2026-10-13 — focused
verification passed`. For frontmatter, keep the status word and use `updated`
plus `status_evidence`; never leave a bare status as the only evidence. A date is
provenance, not proof of freshness: inspect the owner and relevant current code,
verification, and Git on resume and at milestones before updating status.

Do not record Git status, branch state, commit hashes, or “committed” / “not
committed yet” in records, checkpoints, index entries, or plans. Review establishes
readiness for commit; Git supplies commit history. Preserve existing historical
evidence and formats rather than rewriting unrelated records.

Handoff is the owning record or plan plus this fixed chat prompt:
“Continue the next item of <record or plan path> that is not done.” For a
lightweight entry, identify its stable build ID in the chat alongside the index
path. Never name a step number in a resume prompt or create separate handoff,
prompt, or next-chat files. Follow existing approval gates and dependencies when
selecting the next item. Shared read-first, scope, safety, question, and finish
rules live once in project docs or this skill; task artifacts link to them and
contain only task-specific requirements and constraints.

## Test boundary

A **test artifact** is a test file or case, test-owned fixture, snapshot, golden file, or checked-in coverage baseline or configuration. It excludes production fixtures and generated coverage reports. Do not plan, create, generate, modify, rewrite, or delete test artifacts unless the user directly and explicitly asked for that test change in this task. General approval of a build, plan, finding, or production-code change does not add test work that the user did not request. If the requested test change is unclear, ask before touching a test artifact and do not broaden it beyond what the user requested.

You may inspect and run existing tests. When one fails, first determine whether the production behavior is wrong and fix it when that correction is already in scope. Otherwise report the failing test, relevant evidence, and practical options without changing any test artifact. Never use snapshot-update, golden-file rewrite, or similar mutating modes unless the user directly requested that exact change.

## Choose the path

Use the lightweight path when the requested outcome is clear, the change is localized to understood behavior, an established pattern applies, and there is no material interface, persistence, security, or architectural change. Decide from the request and a focused look at the owning code, not a separate discovery exercise. File count alone does not determine the path. Use the full lifecycle for other tasks, an explicit request for a plan/full build record, or an existing full build being resumed.

### Lightweight path

Inspect applicable instructions and the owning code, make the authorized change, and run focused verification plus required repository checks. Apply the research and context-budget practices below, but load project knowledge only when needed. Work locally; skip the full template, plan approval, work-item statuses, milestone logs, and lifecycle references. Do not request approval again for a clear change the user already authorized.

At completion, upsert one short entry in the resolved active history index (default `docs/generated/hawk-build/builds/index.md`) with a stable lowercase build ID, date/title, status, request/outcome, changed paths, verification result, and unresolved issue or `none`. Include useful keywords in the title or outcome. This entry is the lightweight build record and history summary; no separate build file or self-link is needed. If a project plan already owns status, link to it and keep only the outcome and dated verification evidence here. Otherwise, if pausing before completion, update the same entry with a dated `in progress` or `blocked` status and check evidence. Resume with the fixed prompt above; read the owner and verify relevant current state. Report outcome, verification, unresolved issues, and the index path without full-lifecycle status fields.

Escalate when a concrete uncertainty or risk invalidates the lightweight criteria, or durable design knowledge needs to change or be corrected. Preserve completed changes and verification in a full build record under the same ID, replace the index entry with a pointer, and plan the remaining work before proceeding with it. Do not redo settled research or treat completed work as awaiting retroactive approval. A routine fixable verification failure alone does not require escalation; an unexplained failure that changes the approach may.

### Full lifecycle

For a full build, read [full-build planning and execution](references/plan-format.md) before starting or resuming work. It owns the record structure, approval rules, implementation guidance, and checkpoints. Keep one task record, linking an existing owning plan instead of duplicating its working status; load other references only at their stated triggers:

- [Delegation and model routing](references/delegation.md): when independent workstreams justify delegation or a model-routing decision is needed.
- [Project knowledge and history](references/knowledge.md): when planning or completing knowledge maintenance, maintaining the full-build history index, or resolving note freshness.
- [Git and finalization](references/finalization.md): when finalizing a full build or preparing a user-authorized related commit.

Do not reread unchanged references already in context. Lightweight builds use only the shared rules and research practices here, plus the commit guidance when a commit is authorized.

## Research and context budget

Default to narrow research. Read applicable repository instructions and search relevant entries in `docs/generated/hawk-build/project.md`, the project-knowledge index. Load a linked design note only when it helps resolve this task, then inspect the current owning code and nearest relevant verification. Notes explain architecture; current source establishes the behavior being changed. Missing knowledge is not a reason to scan the repository or initialize every category.

Stop once change location, approach, and verification are supported. After roughly 3–5 targeted reads, reassess whether those questions are answered; this is a checkpoint, not a hard cap. Before expanding research, name the unresolved question that could change the plan and the next focused lookup. Inspect contracts, configuration, callers, or a comparable implementation only when needed to answer it. Research external documentation when it materially reduces uncertainty; retain URLs and short findings. Do not collect evidence merely to fill record fields.

Consult build history only for a specific question about a prior decision or regression that current code and design notes do not answer. Search the resolved active history index (default `docs/generated/hawk-build/builds/index.md`) by concepts, keywords, symbols, and paths; open a matching full build only when its summary is insufficient. These are optional retrieval steps, not a checklist to exhaust.

Use targeted searches and bounded source sections instead of whole-file dumps. Narrow excessive search results before loading them; broaden reads when surrounding control flow or contracts matter. Summarize checks with command, outcome, and relevant failure excerpts. Keep needed large logs in temporary artifacts outside the record, without secrets; link them and retain enough summary to resume if they expire. Start with focused verification, broaden for evidenced risk or repository requirements, and do not rerun successful checks without changed code or evidence that justifies it.
