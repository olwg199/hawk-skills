---
id: <build-id>
title: <title>
status: research
status_evidence: "<What the dated check showed>"
started: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---

# <title>

## Current checkpoint

<!-- Only the owner link, settled contract links, and last dated verification summary. Status/resume rules live in SKILL.md; do not copy shared working rules here. -->
- Status owner: [Plan](#plan) <!-- Use the existing project plan path when it owns build steps. -->
- Settled contracts: <links or none>
- Last verified: <YYYY-MM-DD — check and result>

## Plan

<!-- If a project plan owns status, link to it here instead of duplicating its steps. -->
<!-- Omit Risk when there is no material plan-wide risk. -->
- Risk: <low, medium, or high> — <brief reason>

### Outcome

<The intended observable result in one or two sentences.>

### Needed

- N1 — <Confirmed user outcome or constraint, separate from implementation choices.>

### Decided

- D1 — <Material decision> — <brief rationale>.
<!-- A decision the user made goes into the decision log in the same turn (doc-writing rules say where); cite it instead: D1 — <question it answers> — <log row ID>. -->

### Work items

- **W1 — <short work-item name>** · `needs details` — <YYYY-MM-DD> — <what the check showed>
  - Why: <reference N1/D1; add only context not already stated there>
  - Work: <implementation, investigation, decision, or output>
  - Paths: <inspect, add, modify, or remove paths and brief placement reason; `none` only for non-file work>
  - Verification: <focused command, inspection, or evidence for this item>
  - Missing: <repository evidence or requirement needed before this item can advance>

<!-- Add `Missing` only for `needs details` or `Decision needed` only for `needs decision`. Add interface, data, migration, failure-handling, or item-specific risk only when material. -->
<!-- For `needs decision`, use this shape inside the affected work item instead of `Missing`; include only viable options and recommend one when supported:
  - Decision needed: <Concrete question the user can answer?>
    - A — <Approach>. Pros: <brief benefit>. Cons: <brief drawback>.
    - B — <Approach>. Pros: <brief benefit>. Cons: <brief drawback>.
    - Recommendation: <A or B, and one sentence explaining why; or the preference needed to choose>.
-->

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

- Path: `docs/generated/hawk-build/project.md`
<!-- List affected design-note paths when applicable. Knowledge changes belong to an explicit work item; routine history indexing happens at finalization. -->
- Status: unchanged — <YYYY-MM-DD> — <what the check showed>
- Durable facts changed: none

## Plan deviations

_None._

## Delegated work

_None._

## Implementation iterations

<!-- One compact entry per implementation milestone: item ID, change, result, verification. Reference delegated results; retain failed attempts only when useful to the next approach. Keep pending actions only in the owning work items. -->
_Not started._

## Findings

<!-- Written at completion, when every section above is deleted and only the frontmatter and this section remain (see finalization.md): Outcome, Lessons, Contracts to keep, Last verification. -->
_Not finalized._
