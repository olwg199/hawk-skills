---
id: bld-20260821-hawk-build-record-clarity
title: Make Hawk Build plans easier to understand and control
status: complete
started: 2026-08-21
updated: 2026-08-21
branch: main
---

# Make Hawk Build plans easier to understand and control

## Current checkpoint

- Stage: complete
- Last verified: unified work-item model passed the official skill validator and repository whitespace check
- Next action: none
- Blocked by: none

## Goal

Make the pre-implementation Hawk Build result show a detailed but compact account of what will change, why it is needed, what has already been decided, what remains open, and exactly what the user is approving.

## Research

### Evidence

- `skills/hawk-build/SKILL.md` requires a decision-complete confirmed plan, but defines its contents as a sentence rather than a scannable schema.
- `skills/hawk-build/assets/build-record-template.md` gives the confirmed plan only an empty placeholder, so record shape depends on each run.
- The completed `.build/bld-20260712-clarity-first-skills.md` contains strong detail, but requirements, rationale, affected areas, decisions, validation, and approval scope are spread across multiple long sections.
- The assistant output rule asks for only the next material result or question, but does not prescribe a compact plan preview when asking for confirmation.
- `.codex/hawk-build.md` confirms that detailed task history belongs in `.build/` while durable project facts remain separate.

### Requirements and constraints

- Preserve a detailed durable record without turning it into a transcript or private reasoning log.
- Before implementation, show a compact plan of all upcoming changes.
- Clearly separate what is needed, what is decided, what is still open, and what the user is being asked to approve.
- Keep the format easy to scan and control without losing affected paths, behavior, risks, or verification.
- Do not edit the Hawk Build skill until the revised design is confirmed.

### Candidate approach

- Add a **Plan at a glance** control section near the top of every active record: outcome, plan state, scope, risk, decisions needed, and approval target.
- Separate **Needed**, **Decided**, **Assumptions**, **Open questions**, and **Out of scope** so evidence, requirements, and choices cannot blur together.
- Give each planned workstream a short ID and require bullets for why it is needed, behavior to change, expected paths, interface or data effects, failure handling when relevant, and verification.
- Require exact paths when known and an explicitly marked path area or pattern when research cannot yet identify every file.
- Show the full compact plan in the assistant's confirmation request instead of reporting only the record path and next question.
- Let users approve the whole plan or request a change by workstream ID; require fresh approval only for material scope, behavior, interface, data, risk, or acceptance changes.
- Keep research evidence and implementation history as supporting detail below the control section; preserve the confirmed baseline and record later deviations separately.

### Open questions

_None._

### Resolved decisions

- Use a fixed compact schema, omitting irrelevant optional bullets.
- Approve the whole plan by default while allowing the user to exclude or revise a named change group.
- Keep research and implementation history in the same record below the plan.
- Keep each upcoming-change entry to four core bullets—why, change, paths, and verification—and add interface, data, failure-handling, or risk detail only when it materially affects the work.

### Rejected approaches

- Improving only the wording of the current instructions — the main ambiguity comes from the lack of a required output schema and approval summary.
- Making the whole build record short — this would weaken resumability and audit value; the better split is a compact control surface plus supporting detail.

## Project memory

- Path: `.codex/hawk-build.md`
- Status: unchanged
- Durable facts changed: none

## Confirmed plan

<!-- Preserve this section after the user confirms it. -->

Confirmed by the user on 2026-08-21, with an explicit request to keep upcoming-change entries compact while retaining enough detail to understand and control the work.

### Outcome

Make Hawk Build present a compact, decision-complete plan before implementation so the user can distinguish what is needed, what is decided, what will change, what will remain unchanged, and what approval authorizes.

### Changes

- **C1 — Planning and approval instructions**
  - Why: the current skill requires plan content but not a consistent presentation or approval schema.
  - Change: define plan states, separate needs from decisions, specify concise change groups, and clarify confirmation and deviation rules.
  - Paths: modify `skills/hawk-build/SKILL.md`.
  - Verification: inspect realistic draft, decision-needed, ready-for-approval, implementation-update, and material-deviation scenarios.
- **C2 — Build-record template**
  - Why: the current plan section is an empty placeholder and the research structure omits some required categories.
  - Change: put the compact plan and approval surface before supporting research and execution history.
  - Paths: modify `skills/hawk-build/assets/build-record-template.md`.
  - Verification: create or inspect a representative record and ensure optional detail can be omitted without losing control information.
- **C3 — User documentation**
  - Why: the README should describe the planning and approval experience users will receive.
  - Change: document the compact plan, named change groups, and approval controls without duplicating the full schema.
  - Paths: modify `README.md`.
  - Verification: compare the README description with the final skill behavior.

### Boundaries

- Preserve project memory, delegation, model-routing, commit, and finalization behavior unless a small wording adjustment is required to align with the new plan states.
- Keep detailed evidence and implementation history in the same record below the plan.
- Do not add a separate reference file or script for this focused format change.

### Acceptance checks

- A user can scan the plan and identify needs, decisions, open questions, upcoming changes, exclusions, verification, and the exact approval request.
- Upcoming-change entries default to only why, change, paths, and verification; optional impact details appear only when material.
- The assistant shows the compact plan when requesting confirmation instead of only reporting a record path or isolated question.
- The confirmed baseline stays unchanged and later material deviations require renewed approval.
- The skill passes its structural validator and repository whitespace checks.

## Plan deviations

- 2026-08-21 — Replaced the global plan-state and separate approval/question model with one status-bearing **Work items** section.
  - Reason: avoid repeating the same scope from different angles while allowing individual items to need details, need a decision, wait for approval, proceed, finish, or be excluded.
  - Effect: work items retain their title and details in every status; unresolved input and approval live on the affected item; implementation waits for all items by default but can be explicitly staged for independent approved items.
  - Affected confirmed changes: C1, C2, and C3.
  - Approval: explicitly authorized by the user after reviewing the alternative model.

## Delegated work

_None. The three instruction and documentation edits were tightly coupled and completed in one pass._

## Implementation iterations

- 2026-08-21 — Updated `SKILL.md` with explicit plan states, a compact control schema, four-field upcoming-change groups, approval by change ID, and material-deviation rules; updated the record template and README to match.
- 2026-08-21 — Audited draft, decisions-needed, ready-for-approval, confirmed, implementation-update, and material-deviation scenarios. The first validator run could not import PyYAML; installed it only under `/private/tmp`, reran the official validator successfully, and confirmed `git diff --check` passes.
- 2026-08-21 — Addressed successive review findings, then replaced global approval state, confirmation, open-question, and approval-list concepts with a unified work-item lifecycle. Added inspect-only investigation support and single-source status, decision, exclusion, and deviation behavior.
- 2026-08-21 — Fixed successive F1 gate findings by defining the default gate in terms of unresolved statuses and applying it to every work-item type. Terminal `done` items remain valid; pre-approval research may scope an investigation but cannot perform its planned analysis or deliverable.

## Related commits

_None._

## Final outcome

- Delivered a compact control surface that separates outcome, durable needs and decisions, named work items, boundaries, and plan-level acceptance checks.
- Unified missing details, user decisions, approval, progress, completion, and exclusion under one status-bearing **Work items** section instead of duplicating them in global state or separate lists.
- Limited each work item to **Why**, **Work**, **Paths**, and **Verification** by default; added **Missing** or **Decision needed** only when the item's status requires it, and allowed only material optional impact detail.
- Preserved excluded work in place with status `excluded`, so its title and details remain understandable without a duplicate boundary entry.
- Added accurate path labels for inspect-only investigations and `none` for genuinely non-file decision work.
- Made unresolved-item clearance the default gate for every work-item type while allowing planning-record maintenance, bounded scoping research, and explicitly authorized staged execution; investigation deliverables remain approval-controlled and terminal `done` items continue to satisfy the gate.
- Kept work items as the current source of truth and preserved prior approved scope and outcomes under **Plan deviations** when material changes occur.
- Verification: official skill validator passed and `git diff --check` passed after the final review-finding fixes.
- Project memory: `.codex/hawk-build.md` unchanged because no architecture, placement, or verification convention changed.
- Plan versus actual: delivered C1–C3 with the user-approved work-item lifecycle deviation recorded above.
