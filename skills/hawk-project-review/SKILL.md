---
name: hawk-project-review
description: >-
  Evidence-backed review of an existing project feature, behavior, subsystem,
  file, symbol, or reported problem without requiring a commit diff. Traces how
  the requested area currently works, identifies concrete defects and
  improvement opportunities, and recommends proportionate fixes without editing
  files. Use only when the user explicitly invokes or names
  `hawk-project-review`, including `$hawk-project-review` and
  `/hawk-project-review`. Do not auto-use for reviewing local changes before a
  commit, implementing fixes, broad project onboarding, or open-ended
  exploration without an assessment goal.
---

# Hawk Project Review

Review the current implementation of a user-specified project area. Explain the
relevant behavior, assess it through appropriate engineering lenses, and
recommend concrete fixes or improvements grounded in repository evidence.

Remain read-only. This skill diagnoses and recommends; it does not edit files,
commit, push, or open a pull request. If the user wants implementation, leave a
precise handoff that can be passed to `hawk-build`.

## 1. Establish the review target

Use the text after the invocation and relevant recent chat context to identify:

- **Target:** a feature, behavior, subsystem, file, symbol, workflow, or observed
  problem.
- **Question:** what the user wants to understand or assess.
- **Desired outcome:** explanation, root-cause analysis, improvement options,
  fix guidance, or a combination of these.
- **Review lenses:** explicit concerns such as correctness, simplicity,
  maintainability, security, performance, data integrity, API behavior, or UI
  behavior.

Do not require or search for a commit diff. Review the repository's current
working state, including uncommitted content naturally encountered in the
target area.

If the user gives a target but not a precise question, perform the useful
default: explain how it works, identify material problems, and recommend
proportionate improvements. If no concrete target can be resolved from the
request or recent context, ask the user what feature, behavior, file, symbol, or
problem to review. Do not substitute the current diff as an implicit target.

Record a one-sentence scope statement before investigating. Keep the review
bounded to that scope unless following a directly related dependency is
necessary to explain or validate behavior.

## 2. Collect project evidence

Read applicable repository instructions before assessing the code:

- Root and directory-local `AGENTS.md`, `CLAUDE.md`, and `CODEX.md`.
- Directly applicable `.codex/*.md` and `.agents/*.md` files.
- Files explicitly referenced by those instructions.

Build the smallest useful map of the target:

1. Locate the primary definitions and entry points.
2. Trace relevant callers, state transitions, data flow, side effects, and error
   boundaries.
3. Inspect directly related interfaces, schemas, configuration, tests, and
   documentation needed to confirm behavior.
4. Stop expanding when the current behavior and material assessment claims are
   supported or ruled out.

Prefer project-local evidence over general assumptions. Use external research
only when the user requests it or when a current external contract or platform
behavior is necessary to verify a claim. Cite any external sources used.

Do not inventory the whole repository, review unrelated code, or turn a targeted
question into a general architecture audit.

## 3. Explain how the target works

Construct a concise behavior model before judging the implementation. Cover only
what matters to the user's question:

- Entry point and initiating event.
- Important control flow and state or data transformations.
- Boundaries with storage, APIs, platform services, or UI.
- Success result and meaningful failure behavior.

Support material statements with current file and line references. Distinguish
confirmed behavior from inference. If the implementation is incomplete or
contradictory, state the uncertainty rather than inventing the missing contract.
For cross-file or cross-platform comparisons, inspect and cite every side of
the comparison; do not infer parity or a difference from only one
implementation.

## 4. Select review lenses

Always assess correctness and maintainability. Add only relevant specialist
lenses:

- **Data integrity:** persistence, migrations, serialization, cache consistency,
  concurrency, and cross-process contracts.
- **API and integration:** request/response contracts, error boundaries,
  retries, idempotency, and external side effects.
- **Security:** authentication, authorization, secrets, trust boundaries, and
  attacker-reachable input.
- **UI behavior:** state presentation, interaction flow, accessibility, layout,
  and platform conventions.
- **Performance and reliability:** demonstrated hot paths, resource lifetime,
  contention, failure recovery, and operational behavior.
- **Simplification:** duplication, unclear ownership, unnecessary indirection,
  or missed reuse of nearby project abstractions.

When the target naturally splits into two or three independent concerns and the
host supports sub-agents, run up to three read-only specialist passes in
parallel. Otherwise review sequentially in the main agent. Give each specialist
the same scope statement, user question, applicable repository instructions,
and relevant source paths. Do not delegate final validation or synthesis.

Specialists must stay inside their assigned lens, inspect only directly relevant
context, and return evidence-backed candidates rather than broad recommendations.

## 5. Separate defects from improvements

Report a **finding** only when the current implementation supports all of:

- A concrete initiating event or state reachable through supported project use.
- The current code path from that trigger to the result.
- An incorrect, unsafe, or contract-violating observable outcome.
- A precise source location where the repair should begin.

Do not require the issue to have been introduced by recent changes. Existing
defects are in scope.

Reject hypothetical failures supported only by API fallibility, arbitrary
tampering, manual corruption, simultaneous independent failures, or undocumented
assumptions. Account for existing validation, types, constraints, retries, and
error boundaries before reporting a problem. Do not report style preferences or
issues a normal formatter, compiler, or linter would already identify.

Report an **improvement opportunity** when there is no proven incorrect outcome
but a concrete project-local change would materially improve clarity,
maintainability, performance, reliability, testability, or reuse. Anchor it to
specific code and explain the expected benefit and tradeoff. Do not recommend a
rewrite merely because another design is possible.

Use stable IDs:

- `F1`, `F2`, ... for current defects.
- `I1`, `I2`, ... for non-blocking improvement opportunities.

Classify findings by practical priority:

- **P1:** high-impact correctness, security, data-loss, or availability problem
  that should be addressed urgently.
- **P2:** material behavior problem that should be fixed in normal development.
- **P3:** limited but real defect with a supported trigger and localized impact.

## 6. Recommend proportionate changes

For every finding and improvement:

- Describe the required outcome, not just the suspected mechanism.
- Identify the best starting file and line.
- Prefer the project's existing patterns and abstractions.
- Recommend the smallest change that fully addresses the demonstrated problem.
- Name relevant tests or verification that should prove the result.
- Mention meaningful tradeoffs or unresolved product decisions.

Before recommending a structural improvement or nontrivial repair, locate the
nearest maintained project-local implementation with similar responsibilities.
Confirm that its constraints are comparable, then prefer alignment with that
precedent when appropriate. Cite the precedent by file and line. If no suitable
precedent exists, say so before proposing a new pattern and explain why the new
pattern is warranted. Do not require this search for an obvious localized fix.

When several findings share one cause, recommend one coherent repair rather than
independent defensive patches. Responsibility-based helpers, validators,
repositories, services, and UI components are desirable when they match the
project architecture; fewer files or fewer lines is not automatically simpler.

If the user asks how to fix the target, provide an implementation-ready approach
but remain read-only. End with a compact `hawk-build` handoff containing the
goal, affected paths, required behavior, constraints, and verification.

## 7. Validate and report

Before returning, independently verify every finding against the current files
and remove duplicates. Recheck each material statement in the behavior
explanation as well as each finding, especially claims comparing multiple
implementations. Ensure the explanation, assessment, and recommendations answer
the user's actual question.

Use short sections and omit empty sections:

---

### Project review

Scope: Review how order synchronization applies remote updates and determine
whether it can lose local changes.

#### How it works

- Concise flow with file and line references.

#### Findings

- **F1 · P1 `path/to/file.ts:42`** — Incorrect observable outcome, realistic
  trigger, supporting evidence, and required repair.

#### Improvement opportunities

- **I1 `path/to/helper.ts:18`** — Concrete improvement, expected benefit, and
  tradeoff. Project precedent: `path/to/comparable-helper.ts:42`.

#### Recommended approach

- Prioritized repair or improvement sequence with verification.

#### Review limits

- Material uncertainty or scope not fully verified.

Generated with hawk-project-review

---

If no material defects are found, say `No material defects found in the reviewed
scope.` Continue to report supported improvement opportunities when present. If
neither defects nor worthwhile improvements are found, say so directly while
still explaining how the target works.

When the host supports inline or file comments, attach each finding to the
tightest current source range. Do not attach comments for improvement
opportunities. In Codex Desktop, emit one `::code-comment{...}` directive per
finding after the human-readable review.
