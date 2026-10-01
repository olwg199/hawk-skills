---
id: bld-20260712-clarity-first-skills
title: Clarity-first build, review, and fix skills
status: complete
started: 2026-07-12
updated: 2026-07-12
branch: main
---

# Clarity-first build, review, and fix skills

## Current checkpoint

- Stage: complete
- Last verified: all three skills passed quick validation; scenario and whitespace checks passed
- Next action: none
- Blocked by: none

## Goal

Make Hawk Build, Quick Review, and Fix Review Findings prefer clear responsibility-based organization while rejecting behavioral complexity for unsupported or imaginary edge cases. Add durable Hawk Build project research at `.codex/hawk-build.md`.

## Research

### Evidence

- `skills/hawk-build/SKILL.md` already stores task-specific research in per-build records but has no reusable project-memory artifact.
- `skills/hawk-mobile-ui-builder/SKILL.md` establishes `.codex/<skill>.md` as the repository convention for concise, skill-specific project memory.
- `skills/hawk-quick-review/SKILL.md` requires an evidence chain, but its reviewer descriptions still use broad terms such as edge cases and failure modes without a reachability gate.
- `skills/hawk-fix-review-findings/SKILL.md` asks for the smallest root-cause patch but does not prefer shared boundary handling when several failures need the same outcome.

### Requirements and constraints

- Clear separation into helpers, validators, repositories, services, and UI components is desirable when it matches real responsibilities and project architecture.
- Roughly 500 lines is a strong cohesion-review signal for hand-written files, especially UI components, but not a universal hard maximum.
- Overengineering means adding behavioral complexity for unsupported or imaginary edge cases, not splitting code into clear files.
- Keep simplification-reviewer selection, nice-to-have reporting, and default remediation behavior unchanged.

### Open questions

_None._

### Rejected approaches

- Treating minimal file count or minimal abstraction count as simplicity — conflicts with the desired clarity and responsibility separation.
- Saving reusable research only in task build records — future builds would need to search unrelated historical records.
- Storing Hawk Build memory in general agent instructions — would apply task-specific build guidance outside the skill.

## Project memory

- Path: `.codex/hawk-build.md`
- Status: created
- Durable facts changed: recorded skill layout, documentation and build-record boundaries, reference skills, and validation commands

## Confirmed plan

Confirmed by the user on 2026-07-12:

### Summary

Update the skills to encourage clear responsibility-based organization while preventing speculative edge-case handling. Add `.codex/hawk-build.md` as durable project memory so future build calls can reuse verified architecture and placement research.

### Build changes

- Research the nearest comparable feature and follow the repository's demonstrated architecture, boundaries, naming, imports, tests, and verification commands.
- Record proposed file paths and placement reasons in the confirmed plan.
- Encourage responsibility-based helpers, validators, repositories, services, integrations, transformations, and UI components in the correct feature-local or genuinely shared locations.
- Treat approximately 500 lines as a cohesion-review signal, normally decomposing large UI components while allowing cohesive services and similar workflows to remain larger.
- Define clarity as code a new human or agent can locate, explain, and safely modify, without equating clarity with minimal files, abstractions, or lines.

### Durable project research

- Use `.codex/hawk-build.md`, read and verify it at the start of every build, and correct stale entries from repository evidence.
- Store only durable architecture, placement, dependency, representative-feature, naming, verification, and decomposition conventions.
- Keep transient task research in `.build/<build-id>.md`; never store secrets, raw output, copied code, speculation, or ambiguous inferences in project memory.
- Update memory after confirmed placement decisions and again at finalization when verified outcomes differ.
- Merge concise facts, remove stale facts, and report memory status in the build record and final response.

### Review and fix changes

- Require findings to establish a reachable trigger, changed path, and incorrect observable outcome.
- Accept edge cases supported by current callers, contracts, untrusted inputs, relevant dependency behavior, regressions, production evidence, or plausible security/data-loss risk.
- Do not report already acceptably handled exceptions or prescribe exhaustive prevention.
- Prefer one existing error boundary when several failures share an outcome; add specialized recovery only for concrete cases requiring different behavior.
- Allow responsibility-based extraction during fixes, preserve proper error logging and cleanup, and keep simplification behavior unchanged.

### Validation

- Run skill-creator validation for all three modified skills.
- Confirm the build template records memory status without duplicating the memory contents.
- Inspect the final diff and check the representative architecture, file-size, memory reuse, realistic edge-case, shared error-boundary, and simplification scenarios.

## Plan deviations

_None._

## Delegated work

_None. The changes are tightly coupled instruction edits and are being implemented in one pass._

## Implementation iterations

- 2026-07-12 — Added reusable Hawk Build project memory, architecture-aware placement and file-cohesion guidance, reachable-edge-case review gates, proportionate remediation rules, build-record memory status, and matching README documentation.
- 2026-07-12 — Validated all three skill folders with `quick_validate.py`; checked required scenario language and confirmed `git diff --check` passes.

## Related commits

_None._

## Final outcome

- Delivered clarity-first architecture and placement guidance without treating file count as overengineering.
- Added the 500-line cohesion signal with UI-specific decomposition and cohesive-service exceptions.
- Restricted actual review findings and fixes to evidence-supported reachable failures and proportionate outcomes.
- Added `.codex/hawk-build.md` durable project memory plus compact build-record status tracking.
- Preserved simplification-reviewer selection, nice-to-have reporting, and default remediation behavior.
- Verification: all three skills passed the official quick validator; scenario and whitespace checks passed.
- Plan versus actual: implemented as confirmed with no deviations.
