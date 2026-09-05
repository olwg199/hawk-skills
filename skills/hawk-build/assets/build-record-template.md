---
id: <build-id>
title: <title>
status: research
started: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
branch: <branch-or-none>
---

# <title>

## Current checkpoint

<!-- Update at milestones or handoff. Identify approved scope and active items by reference to Plan, plus any settled contract links needed to resume. Consult history only for a specific uncertainty. -->
- Stage: research
- Last verified: record created
- Next steps:
  - locate owning code and relevant project-knowledge entries
- Blocked by: none

## Plan

<!-- Omit Risk when there is no material plan-wide risk. -->
- Risk: <low, medium, or high> — <brief reason>

### Outcome

<The intended observable result in one or two sentences.>

### Needed

- N1 — <Confirmed user outcome or constraint, separate from implementation choices.>

### Decided

- D1 — <Material decision> — <brief rationale>.

### Work items

- **W1 — <short work-item name>** · `needs details`
  - Why: <reference N1/D1; add only context not already stated there>
  - Work: <implementation, investigation, decision, or output>
  - Paths: <inspect, add, modify, or remove paths and brief placement reason; `none` only for non-file work>
  - Verification: <focused command, inspection, or evidence for this item>
  - Missing: <repository evidence or requirement needed before this item can advance>

<!-- Add `Missing` only for `needs details` or `Decision needed` only for `needs decision`. Add interface, data, migration, failure-handling, or item-specific risk only when material. -->

### Boundaries

- Out of scope: <important excluded work>
- Preserved: <important behavior that must remain unchanged>

### Acceptance checks

- [ ] <End-to-end or user-observable outcome for the complete plan.>

## Research

### Current behavior and evidence

- <Repository observation, source URL, or relevant test.>

<!-- Keep constraints in Plan; reference them here only when needed to explain evidence. A small change may need only a few evidence bullets. -->

<!-- Omit Candidate approaches when there was only one reasonable approach. -->
### Candidate approaches

- <Approach> — <important tradeoff>.

<!-- Omit Rejected approaches when empty. -->
### Rejected approaches

- <Approach> — <why it was rejected.>

## Project memory

- Path: `.codex/hawk-build.md`
<!-- List affected design-note paths when applicable. Knowledge changes belong to an explicit work item; routine history indexing happens at finalization. -->
- Status: unchanged
- Durable facts changed: none

## Plan deviations

_None._

## Delegated work

_None._

## Implementation iterations

<!-- One compact entry per implementation milestone: item ID, change, result, verification. Reference delegated results; retain failed attempts only when useful to the next approach. Keep pending actions in Current checkpoint. -->
_Not started._

## Related commits

_None._

## Final outcome

_Not finalized._
