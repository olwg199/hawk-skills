# Candidates, simplification leads, tests and the finding gate

The main agent reads all of it before Phase 3. Researchers read only Candidate reporting, Simpler approaches and
High-value test suggestions; the final gate is the main agent's alone.

## Candidate reporting

Forward a candidate when a specific changed-code signal supports a plausible
consequential defect or useful simplification, even if the trigger, caller, or
outcome is not fully verified. Name the missing link and how to check it. Do not
require final confidence, proven trigger likelihood, or a blocking remedy. Do not
invent evidence to complete a packet. Separate observed facts from assumptions,
and mention counterevidence, such as an existing guard or error boundary whose
adequacy remains uncertain.

Discard disproven concerns, unrelated or pre-existing code defects, pure style
preferences, and generic speculation without a concrete code signal. The final
gate does not suppress an evidence-backed candidate solely because verification
is incomplete. Candidates are not findings or review limitations. Do not impose
a top-N quota that hides material concerns; keep packets concise and deduplicated.

Stop investigating a concern once it is supported enough for adjudication, ruled
out, or has a clearly stated missing verification. Return consequential
interaction questions to the coordinator with source references instead of
expanding into adjacent systems. Then continue the remaining assigned changes
before returning the coverage summary.

In each packet, give the current repo-relative path and line range, plus a brief
fix-location note if behavior spans files. Cite source locations for evidence
and counterevidence so the main agent can verify them directly. Attach
removed-code or missing-block concerns to the nearest surviving owner line. Rate
claim confidence from 0–100 as a rough judgment, not a calibrated probability,
and describe trigger reachability/frequency and impact or improvement value
separately. Mark unknown links as unknown; neither serious impact nor a high
score substitutes for evidence. No numeric floor applies to candidates.

## Simpler approaches

Check for unnecessary abstractions, indirection, configuration, branching,
duplication, and reimplemented nearby helpers or components. Propose a concrete
simpler alternative, explain which complexity it removes, and show how required
behavior and contracts are preserved. State any remaining equivalence question.

Judge clarity, methods, splitting and comments by the [clear-code rules](code-clarity.md); a lead
that only makes code shorter is not a simplification. Inspect only the affected area, directly referenced utilities, colocated
components, or adjacent files; do not search the whole repository for reuse.
Avoid rare-condition hardening that adds disproportionate complexity.

Keep simplification candidates separate from defects. A confident, worthwhile
simplification can remain optional when behavior is correct; optional
improvements have no confidence band or cap. They become at most 3
**nice-to-have simplification leads** that never block readiness, never count as
issues, and never receive inline/file comments.

## High-value test suggestions

Researchers may forward concrete test ideas with unverified value or coverage,
naming the missing check; no score cutoff applies to forwarded ideas. A final
suggestion must cover changed behavior where a focused test would materially
protect a critical or error-prone invariant. Prioritize mappings and conversions,
parsing or serialization, state transitions, authorization boundaries, monetary
calculations, persistence or migrations, idempotency, and cross-process or API
contracts. Complex branching qualifies when a specific consequential outcome can
be exercised.

The main agent independently scores **test-value confidence** from 0–100 based on project
evidence that the behavior is consequential, realistically regression-prone, not
already protected, and expressible as a focused invariant: 25 for trivial,
duplicate, or coverage-for-coverage's-sake ideas; 50 for plausible but minor or
weakly evidenced value; 75 for a specific material regression risk with a clear
invariant; 100 for a critical contract or high-impact mapping with direct
evidence. It measures the value of adding the test, not whether the code is
currently correct. Keep at most 3 suggestions scoring 75 or more, preferring the
most critical, specific, and non-duplicative.

Each suggestion is one line: the production location, test kind, and exact
scenario or invariant. Do not
suggest broad coverage, tests for trivial accessors or presentation copy,
duplicates of nearby tests, or a test merely because coverage is absent. Inspect
the nearest existing tests only when needed to avoid duplication or choose the
level. A missing test is never a finding or review limitation, even when
repository instructions call for one. Suggestions are advice only: they do not
count as issues, do not affect readiness, receive no inline/file comments, and
never authorize test work.

## Final finding gate and proportional remedies

Only the main agent applies this gate. Before a candidate becomes a final
finding, prove the changed code path, the incorrect outcome, **and** that the
initiating trigger is realistically likely in this project's current
environment. Logical possibility, API fallibility, or the fact that an operation
can throw is not trigger evidence.

Require at least one of these forms of trigger evidence:

- A deterministic path from normal supported use.
- A failing or missing behavior exercised by an existing test.
- Production evidence, logs, or a reported incident.
- A documented, reasonably common platform behavior applicable to this project's configuration.
- A current caller or workflow that produces the state.
- A user action supported by the application or documented operating procedure.

Apply the gate as follows:

- Discard triggers based only on manual corruption, unsupported file editing or
  operator behavior, arbitrary tampering, generic transient infrastructure
  errors, or simultaneous independent failures, unless project-specific evidence
  shows they realistically occur.
- For a multi-failure chain, verify every material link and establish that each
  additional failure is realistically likely during the preceding one. For
  example, do not report "primary operation fails → optional follow-up query
  also fails → cleanup is skipped" merely because both operations can throw.
- Report filesystem, persistence, network, remote-management, or monitoring
  exceptions only when project-specific evidence establishes the concrete
  failure mode and existing handling produces an unacceptable observable result.
  Assess existing error boundaries first; do not assume automatic retry,
  compensation, or recovery is required.
- Do not infer unrelated persistence, network, device, or platform failures from
  input validation or another proven failure. Do not report states excluded by
  enforced types, validation, schema constraints, locks, or documented invariants.
- Preserve deterministic bugs in ordinary execution, common edge cases supported
  by current callers, security boundaries reachable by an actual lower-privileged
  actor, data loss reachable through normal workflows, and contract violations
  demonstrated by code, tests, or documented behavior.
- Require claim confidence ≥ 75 with evidence for the trigger, changed path, and
  incorrect outcome. Assess trigger realism and impact separately when deciding
  whether a maintainer would block the commit. Confidence is not frequency, and
  impact never compensates for missing evidence; an uncertain material link
  prevents acceptance.
- Treat unsupported defensive improvement as non-finding hardening. Do not use
  simplification leads to smuggle speculative failure prevention into the review.
- Describe what breaks and the required outcome. When remedy context helps,
  prefer an existing shared error boundary, and recommend guards, retries,
  recovery, or fallbacks only for a demonstrated case. Never recommend silently
  swallowing errors or disproportionate defensive architecture.
- A failing test is not a test suggestion. Keep it as a finding only when evidence
  proves the eligible change set introduced the failure or materially changed
  the failing behavior. If an unproven failure blocks validation of changed
  behavior, report a concise review limitation; otherwise omit pre-existing or
  unrelated failures. Do not call a test stale or broken without evidence, and
  never recommend rewriting or deleting a test merely to make review pass.

Never report as a finding, beyond the gate above:

- Pre-existing issues not introduced by these changes, except those the scoped mandatory knowledge/setup pass covers.
- Real issues unrelated to modified, added, deleted, or untracked code in scope.
- Things that look like bugs but aren't, and pedantic nitpicks a senior engineer wouldn't flag.
- Issues a linter, compiler, typechecker, or formatter would catch.
- Documentation style preferences and unrelated documentation gaps.
- Repo instruction issues explicitly silenced in code (for example lint-ignore comments).
- Intentional behavioral changes that are clearly the purpose of this change.
- Structural preferences based only on minimizing file, abstraction, or line count.
