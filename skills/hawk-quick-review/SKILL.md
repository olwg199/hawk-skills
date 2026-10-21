---
name: hawk-quick-review
description: >-
  Adaptive code review that picks review perspectives based on what
  changed. Uses bounded Sonnet researchers in Claude and Luna researchers in
  Codex for substantive investigation, with the current main agent validating
  candidates and making final judgments. Reviews local uncommitted
  changes, considering the user's stated intent, and reports blocking findings,
  non-blocking simplification leads, high-value test suggestions, and a mandatory
  blocking knowledge and Codex/Claude compatibility check scoped to the reviewed
  work. Use only when the user explicitly asks to review local code, changes, or the worktree
  before commit, or invokes
  `$hawk-quick-review`. Do not auto-use for general questions about review
  practices, review skills, or whether a review approach is good.
allowed-tools: Bash(git diff:*), Bash(git status:*), Bash(git log:*)
---

Provide a code review in three phases: assign investigation, gather evidence,
then adjudicate in the current main agent. Researchers own discovery. The main
agent owns targeted source verification and every final decision: filtering,
severity, usefulness, compatibility status, and readiness. Never delegate those
decisions.

Remain read-only: do not edit code, tests, docs, memory, or instruction files.
By default, review local uncommitted changes: staged and unstaged tracked changes
relative to `HEAD`, plus eligible untracked files. If `HEAD` is unavailable,
combine staged and unstaged diffs. Do not assume every untracked file belongs
to the change. Always run the mandatory knowledge and Codex/Claude
compatibility pass below.

## Invocation focus

Invocation text: $ARGUMENTS

If the line above is empty or shows a literal placeholder (for example in
Codex), use any text after the skill name in the user's message. Add specific
concerns from recent chat context, such as "look closely at auth edge cases", as
focus notes only; chat context never sets scope. Sort the text into:

- **Scope:** `staged` reviews only staged changes. Paths, directories, or globs
  introduced by explicit limiting wording such as "only", "just", or "limit to"
  (for example `only src/api`) limit the eligible change set to matching
  changes. A path mentioned without such wording, as in "check error handling
  in src/api/client.ts", is a focus note. Without scope, review all local changes.
- **Directives:** single-agent or sub-agent requests, "no questions", explicit
  verification (builds, typechecks, tests), and untracked files to include.
- **Focus notes:** concerns to emphasize. For example,
  `/hawk-quick-review use subagents Make sure data consistency is not compromised`
  requests delegated review with a data-consistency focus. Without notes, use
  "general review"; do not ask solely to collect them.

Pass focus notes to every reviewer as emphasis. They never permit ignoring
serious issues outside the focus. Focus notes are not the change's intent; use
invocation text as intent only where it says what the change is meant to do.
Only scope narrows what is reviewed.

## Clarify ambiguous requests

Resolve material ambiguity before acting on a user message.

- Inspect the current message, relevant recent chat context, and available project evidence before asking.
- If one reasonable interpretation is low-risk and does not materially change scope, behavior, files, output, or external state, state the assumption and continue.
- If two or more plausible interpretations would lead to materially different work, ask a targeted question that names the likely meanings and their practical difference; prefer “Did you mean A or B?” over “Can you clarify?”
- Write the choice in the question shape of [report and question format](references/report-format.md), then use the host's structured question tool when available, with 2–3 mutually exclusive choices, the evidence-supported recommendation first, and a free-form answer when supported. Otherwise ask the same concise question in chat.
- Ask only the smallest set of blocking questions. Do not repeat questions answered by the request or context, and do not treat ambiguity as permission to broaden scope or make a consequential change.

## Host behavior

This skill is shared by Claude Code and Codex; use each host's available agent
mechanism within its permissions. For substantive investigation, delegate to one
researcher by default and split only when independent areas warrant it. Several
perspectives can share one researcher. Small mechanical changes, explicit
single-agent requests, and unavailable delegation can stay in the main agent.
Do not ask solely for delegation permission.

**In Claude Code:** Use Sonnet for routine researchers. Do not assign final
filtering or judgment to Haiku or another planning agent. The current main agent
keeps its selected model, including Opus when that is what the user is running.

**In Codex:** Use `gpt-6-luna` with `high` reasoning for routine researchers,
where supported. Select the model and effort explicitly through the host's
supported mechanism; do not assume explorer/default agents are cheaper or that
inherited settings select Luna. Do not change the main chat's model or effort.
When the host offers a fresh-context option, such as `fork_turns="none"`, use it
with the compact assignment so researchers do not inherit the full conversation.

If the requested researcher model or effort cannot be selected, use supported
settings and report the actual fallback. If delegation is unavailable or
disabled, perform the same scoped review in the main agent and explain the
fallback once. Do not imply that the preferred model ran without evidence.

Use a stronger researcher only for a named, consequential question the routine
researcher cannot resolve, or an assigned area beyond its capability. Give it
only the relevant evidence and missing question; do not repeat the full review
with a stronger model. Narrow context and reduce redundant researchers before
escalating. Report stronger investigations and why they were needed.

---

## Phase 1 — Inventory changes and assign investigation

The main agent coordinates this phase without researching every hunk:

1. Fetch a compact change inventory:
   - Use `git diff HEAD --name-status` and `git diff HEAD --stat`. For `staged`
     scope, use `git diff --cached` with the same options. For path scope,
     append `-- <paths>`.
   - If `HEAD` is unavailable, inventory both `git diff --cached` and `git diff`.
   - Use `git status --short --untracked-files=all` to detect untracked files.
     `staged` scope excludes untracked files unless explicitly included.
   - When scope excludes changes, list the excluded paths for the output. For
     `staged` scope, also note partially staged files whose unstaged hunks were
     not reviewed.
   - Read selected hunks only when needed to assign ownership or clarify intent.
     Let a researcher map ambiguous areas when that requires substantive
     investigation. Fetch the full diff only in single-agent mode. Researchers
     use the scope's diff command limited to their assigned paths (both staged
     and unstaged without `HEAD`) and read eligible untracked files directly.

2. Capture a short intent snapshot:
   - Summarize the user's stated goal for the change from the request and recent chat context.
   - If intent is unclear and could materially affect whether changed behavior is a bug or expected, ask the user to confirm it before Phase 2 when the host supports interactive input. Offer 2–3 concise intent options drawn from the request, chat, and diff, plus a free-form option when supported.
   - If the host is non-interactive or the user asked for no questions, proceed and clearly separate stated intent from diff-based inference.
   - Use the snapshot to avoid flagging intentional behavior changes, never to suppress bugs, regressions, security issues, data loss, or broken contracts.

3. Identify all changed file paths within scope:
   - Include tracked paths from the inventory.
   - Treat untracked files as candidates, not automatically part of the change.
     Review those eligible for commit: plausible project source, configuration,
     test, migration, or documentation files in normal project paths, including
     relevant skill-maintained Markdown under `docs/generated/` for the
     knowledge pass. Skip other generated, binary, cache, log, scratch,
     vendored, and secret-looking files unless explicitly requested.
   - List skipped or partially reviewed untracked files in the output with a
     short reason. If important-looking untracked files are ambiguous, ask the
     user to stage them or rerun with explicit instructions to include them.

4. Collect relevant repo instruction files and return the paths used:
   - Root and directory-local `CLAUDE.md`, `AGENTS.md`, and `AGENTS.override.md`.
   - `CODEX.md` only if present; its absence never blocks review.
   - `.codex/*.md` and `.agents/*.md` only when directly applicable to the changed paths.
   - Documentation and matching `docs/generated/` knowledge entries that describe
     affected behavior or whose read conditions apply to this work, verified
     against current source. Follow only relevant links. Notes do not override
     instructions.

5. Group eligible changes by affected behavior, shared source context, and
   contracts. File and line counts guide batching, not agent count. Check every
   eligible change rather than sampling, batching repetitive changes when
   needed. Report deferred or partially reviewed paths instead of skipping them.

6. Select the relevant perspectives and execution mode using the routing rules
   below. Related perspectives can share one pass; do not add perspectives or
   agents to fill slots. Always apply **simplification-reviewer** to a non-empty
   code review; every reviewer checks its area for simpler approaches alongside
   correctness, without a separate agent or quota. With no eligible changes,
   select no code reviewers and run only the mandatory pass. Record the areas,
   perspectives, execution mode, and concrete reason.

### Area and risk routing

- Keep related changes with one researcher: repeated styling or layout changes,
  mechanical renames or moves, or a coherent feature with UI and state logic.
  Use the main agent directly for small mechanical changes when delegation would
  add overhead. Apply relevant perspectives together, without repeated diff reads.
- Before treating moves and renames as mechanical, confirm they preserve
  behavior, imports, references, registration, discovery, packaging, and module
  initialization where applicable. Repetition alone does not establish low risk.
- Add a separate researcher when a bounded area needs substantial separate
  context, presents an independent consequential risk, or needs a targeted second
  assessment of a concrete unresolved concern. For example, UI plus a database
  migration may warrant a data delegate; auth plus independent API or persistence
  changes may warrant distinct specialists. A tiny concurrency, authorization, or
  migration diff can justify one targeted specialist despite its size.
- Specialty labels, file count, or line count alone do not justify more
  researchers. Keep one complex area with one researcher when others would
  repeat the same investigation.
- Use only justified delegates, normally no more than three, each with a distinct
  question, owned paths/behavior, required evidence, and connecting contracts.
  Avoid overlapping full-diff reviews. Explicit multi-agent requests can justify
  an independent assessment, but still bound each assignment.
- Give every eligible path and relevant connecting contract an owner. Check the
  returned coverage summaries against the inventory and route missing coverage or
  interaction questions explicitly rather than rereading the whole diff. Stop
  spawning once the required questions are covered.

**Available review perspectives:**

- **ui-reviewer**: Views, layouts, components, styles, animations, or other visual layer code. Focuses on layout correctness, visual regressions, accessibility, and platform UI conventions.
- **logic-reviewer**: Business logic, algorithms, state machines, control flow, or data transformations. Focuses on correctness, realistic reachable edge cases, and subtle bugs.
- **data-reviewer**: Models, persistence, migrations, serialization, caching, database code, or changed data contracts. Focuses on data integrity, schema correctness, and consistency introduced by the diff. Not for ordinary UI display data, sample data, labels, or simple in-memory arrays unless they alter persistence, schema, serialization, or cross-process contracts. Stay bounded to changed data behavior and directly relevant models, migrations, schemas, serializers, caches, fixtures, or API contracts; do not inventory unrelated entities or flows the change does not modify.
- **security-reviewer**: Auth, permissions, encryption, token handling, input validation, or any security boundary. Focuses on vulnerabilities and exposure risks.
- **api-reviewer**: Network calls, API contracts, error handling, request/response parsing, or backend integration. Focuses on reachable contract-relevant failures, existing error-boundary behavior, and contract mismatches.
- **simplification-reviewer**: Always applied to changed code. Looks for clearer
  equivalent approaches, unnecessary abstractions or indirection, duplicated
  logic, overly complicated control flow, and useful reuse within the affected area.

---

## Mandatory knowledge and Codex/Claude compatibility pass

Read [knowledge and compatibility review](references/knowledge-compatibility.md)
and perform its bounded pass on every invocation, including empty or scoped code
diffs. The reference owns evidence selection, checks, and status rules. The main
agent owns this pass independently of code specialist selection: it may delegate
bounded evidence gathering under the candidate rules below, then validates
candidates with the same acceptance gate as code findings and decides the
status. Existing setup or documentation problems qualify only when they govern
or document the reviewed work. The pass never authorizes a repository-wide
documentation or setup audit; all other review rules stay limited to the
eligible change set.

## Phase 2 — Research and candidate reporting

In single-agent mode, perform one coherent review applying the selected
perspectives, then apply Phase 3. In delegated mode, researchers cover every
assigned hunk and included untracked file, including relevant connecting
contracts; the main agent coordinates coverage and targeted follow-ups rather
than reviewing assigned areas again. Independent assignments can run in parallel
when permitted. Pass intent, focus notes, applicable instructions, owned paths,
and relevant contracts, without copying the full chat or full diff. Keep the
assignment compact:

```text
Read-only investigation of <bounded area> using <perspectives> plus simplification. Do not edit files; run builds/tests only if the user explicitly requested verification.
Question: <owned behavior, risk, or unresolved interaction>.
Inputs: intent, focus notes, scope and its diff command, assigned paths/untracked files, applicable instructions, connecting contracts.
Read your assigned diff and necessary source context. Cover every assigned change; inspect directly referenced definitions, callers, schemas, or nearby tests as needed. Avoid broad repo sweeps, external research, and unrelated architecture review.
Return a compact coverage summary (paths/behavior inspected, contracts checked, gaps) and candidate packets. For each candidate: category, current path/lines, claim, concrete code signal, trigger and suspected outcome or simpler alternative, supporting evidence, counterevidence, unknowns, and the exact missing verification. Include claim confidence and impact/value separately. Do not apply the final finding threshold or discard a concrete concern merely because one evidence link remains unverified. Separately return relevant test ideas with scenario, regression value, and known coverage or coverage uncertainty. The main agent decides what reaches the final review.
```

### Candidate reporting

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

### Simpler approaches

Check for unnecessary abstractions, indirection, configuration, branching,
duplication, and reimplemented nearby helpers or components. Propose a concrete
simpler alternative, explain which complexity it removes, and show how required
behavior and contracts are preserved. State any remaining equivalence question.

Clarity means code a human or agent can locate, explain, and safely modify; it
is not minimizing files or lines. Respect useful responsibility-based validators,
repositories, services, helpers, and UI components that fit the project. A
roughly 500-line hand-written file is a cohesion signal, not a defect or a reason
for arbitrary splitting; recommend only responsibility-based decomposition.
Inspect only the affected area, directly referenced utilities, colocated
components, or adjacent files; do not search the whole repository for reuse.
Avoid rare-condition hardening that adds disproportionate complexity.

Keep simplification candidates separate from defects. A confident, worthwhile
simplification can remain optional when behavior is correct; optional
improvements have no confidence band or cap. They become at most 3
**nice-to-have simplification leads** that never block readiness, never count as
issues, and never receive inline/file comments.

### High-value test suggestions

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

Each suggestion names the production location, test kind, exact scenario or
invariant, regression value, nearby-coverage evidence, and confidence. Do not
suggest broad coverage, tests for trivial accessors or presentation copy,
duplicates of nearby tests, or a test merely because coverage is absent. Inspect
the nearest existing tests only when needed to avoid duplication or choose the
level. A missing test is never a finding or review limitation, even when
repository instructions call for one. Suggestions are advice only: they do not
count as issues, do not affect readiness, receive no inline/file comments, and
never authorize test work.

### Final finding gate and proportional remedies

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

---

## Phase 3 — Main-agent adjudication and output

- Check researcher coverage against the inventory. Assign uncovered paths and
  consequential connecting-contract questions to bounded follow-ups. Coverage
  summaries show what was inspected, not that the code is correct.
- For each candidate, read the actual current source and relevant diff, plus
  directly needed callers/contracts and counterevidence, only far enough to
  settle the claim. Mandatory-pass candidates use their scoped instructions and
  docs. If a packet lacks necessary evidence, request that exact check rather
  than accept its score. Independently assess any stronger researcher's evidence.
- For each finding candidate, answer: What exact event starts the failure? Does
  normal supported usage produce it? What current evidence makes it likely enough
  to matter? Does it require another independent failure? Is the remedy
  proportional? Would an experienced maintainer reasonably block the commit? If
  any answer is not concrete, seek targeted evidence or treat it as unresolved.
- Classify candidates as accepted findings, worthwhile optional improvements,
  rejected concerns, or unresolved material questions. Weak suspicion is not a
  limitation; a concrete consequential question or important coverage gap that
  cannot be resolved is: report it concisely and withhold readiness.
- Merge code candidates with the mandatory pass and targeted interaction checks;
  specialist coverage alone does not establish integration correctness.
  Deduplicate overlapping findings. Reject unsupported findings regardless of
  researcher score, and never mention rejected candidates or their scores.
- Select simplification leads and test suggestions under their rules above,
  explaining each lead's simpler alternative, value, and any remaining
  verification before implementation.
- Assign stable IDs in output order: `F1`, `F2`, … for findings and `S1`, `S2`, …
  for simplification leads. Reuse each finding ID in its inline/file comment.
- Include `Ready to commit from review perspective.` only when the eligible change
  set is non-empty and fully reviewed, no findings remain, the compatibility status
  is `passed`, no important untracked files were skipped or only partially
  reviewed, no material unresolved questions remain, and repository instructions
  do not require an unrun check. When scope excluded changes, write
  `Ready to commit the requested scope from review perspective.` instead.
  Simplification leads and suggested tests never prevent readiness. Otherwise,
  state the findings or limitation concisely.
- Whenever the eligible change set is non-empty, include exactly one
  `Suggested commit message:` line derived from the reviewed change's actual
  outcome: one plain-language sentence starting with an uppercase letter and
  ending with a period, without a conventional-commit prefix, quotes, code
  formatting, alternatives, or vague wording such as "Update files".
- If the eligible change set is empty, report `Nothing to review.` for code, still
  output the compatibility section and its findings, and omit the commit message.
- Always report **Knowledge and Codex/Claude compatibility** as `passed`,
  `blocked`, or `not verified`, with the inspected paths, their relevance, and
  finding IDs counted once. Unrelated docs left outside scope do not make it
  incomplete. `blocked` and `not verified` prevent readiness.
- Report the execution mode (single agent or delegated) with a short concrete
  reason and the perspectives actually applied. Distinguish fallback from
  intentional single-agent routing. In delegated mode, state the actual
  researcher models/efforts and any stronger targeted investigation.
- Do not include code snippets unless the host cannot attach file/line references
  and a finding would otherwise be ambiguous.

Return the review in the final assistant response; terminal output is acceptable
in CLI-style hosts. When the host supports inline/file comments, attach every
finding to the relevant file and line range with the host's native mechanism. In
Codex Desktop, emit one `::code-comment{...}` directive per finding after the
human-readable summary, with an absolute or workspace-resolvable path (including
the workspace folder segment) and 1-based `start`/`end` lines scoped tightly to
the line(s) where the fix belongs.

Format: short sections and bullet lists; no ordered lists, tables, JSON, or
fenced code blocks unless absolutely necessary. Omit lines marked as conditional
when they do not apply. Write the review as [report and question format](references/report-format.md)
describes: in the user's language, every finding as a full block (what breaks,
why it matters, fix), and no closing question; next steps appear only as
statements. The template below shows the sections and their order.

---

### Code review

Review mode: delegated — UI and persistence changes require distinct context.
Researchers: Sonnet; main agent adjudicated candidates.  *(delegated mode only)*
Scope: staged changes only.  *(only when invocation scope applied)*
Perspectives: ui-reviewer, data-reviewer, simplification-reviewer.  *(list those actually applied)*

Found N issues:  *(or "No issues found.")*

- **F1 · P1 · `path/to/File.swift:42` — imported orders lose their status**
  - **What breaks:** an order imported with an unknown remote status is saved as `draft`, so the user sees it reopened.
  - **Why it matters:** every sync with the partner API produces such orders; confirmed by reading the mapper and its caller.
  - **Fix:** map unknown statuses to the existing fallback in `StatusMapper`; one function, no data change.
- **F2 · P2 · `CLAUDE.md:1` — shared instructions are not loaded**
  - **What breaks:** the import points to a missing file, so Claude starts without the project rules in `AGENTS.md`.
  - **Why it matters:** every Claude session in this repo misses the essential rules; checked by resolving the path.
  - **Fix:** restore the import target `@AGENTS.md`; one line.

Knowledge and Codex/Claude compatibility: blocked — F2 identifies a broken required import.  *(or passed / not verified, with inspected paths)*

Ready to commit from review perspective.  *(only when every readiness condition holds)*

Not reviewed (outside requested scope): `path/to/Other.swift`; unstaged hunks in `path/to/File.swift`.  *(only when scoped)*

Untracked files not fully reviewed: `notes/tmp.md` — scratch file.  *(only when present)*

Nice-to-have simplification leads:  *(only when present)*

- **S1 `path/to/Helper.swift:14`** — reuse the nearby validator to remove duplicate rules while preserving supported input behavior; optional.

Suggested tests:  *(only when present)*

- **90% confidence `path/to/Mapper.swift:31`** — Unit-test every supported external status and the fallback invariant; this protects the import mapping from silent regressions not covered nearby.

Suggested commit message: Add resilient status mapping for imported orders.

Inline comments attached: N  *(only when inline/file comments were emitted)*

Generated with hawk-quick-review

---

## False positives to exclude from final findings

- Pre-existing issues not introduced by these changes, except those the scoped mandatory knowledge/setup pass covers
- Real issues unrelated to modified, added, deleted, or untracked code in scope
- Things that look like bugs but aren't, and pedantic nitpicks a senior engineer wouldn't flag
- Issues a linter, compiler, typechecker, or formatter would catch
- Missing or inadequate test coverage (only a qualifying test suggestion)
- Documentation style preferences and unrelated documentation gaps
- Repo instruction issues explicitly silenced in code (for example lint-ignore comments)
- Intentional behavioral changes that are clearly the purpose of this change
- Imaginary edge cases, or failure chains whose local failure, retry behavior, or non-idempotent remote effect is only assumed
- Failures assumed only because a storage, network, or remote API can throw (including a follow-up query that succeeds in current testing), or remedies that assume retry/recovery is required
- Exceptions already handled with the required observable outcome
- States already prevented by locks, validation, types, or documented invariants
- Concerns whose only trigger is manual corruption, hand-replaced state, or unsupported operator behavior
- Structural preferences based only on minimizing file, abstraction, or line count

## Notes

- Never write or modify tests
- Do not run builds, typechecks, or test suites unless the user explicitly asks for verification
- Do not post GitHub comments or review remote PRs; this skill is local-only
