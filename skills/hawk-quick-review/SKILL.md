---
name: hawk-quick-review
description: >-
  Adaptive code review that picks review perspectives based on what
  changed. Defaults to single-agent review and delegates bounded specialist
  work when distinct risks or context justify it. Reviews local uncommitted
  changes, considering the user's stated intent, and reports blocking findings,
  non-blocking simplification leads, high-value test suggestions, and a mandatory
  blocking knowledge and Codex/Claude compatibility check scoped to the reviewed
  work. Use only when the user explicitly asks to review local code, changes, or the worktree
  before commit, or invokes
  `$hawk-quick-review`. Do not auto-use for general questions about review
  practices, review skills, or whether a review approach is good.
allowed-tools: Bash(git diff:*), Bash(git status:*), Bash(git log:*)
---

Provide a code review using an adaptive 3-phase pipeline that selects review perspectives and execution based on affected areas and concrete risks.

Remain read-only: do not edit code, docs, memory, or instruction files. Review
local uncommitted code changes plus the mandatory scoped knowledge and
Codex/Claude compatibility pass described below. Fetch the diff with `git diff HEAD`, including staged and unstaged tracked changes. If `HEAD` is unavailable, combine `git diff --cached` and `git diff`. Also check `git status --short --untracked-files=all` for untracked files, but do not assume every untracked file belongs to the change.

---

## Clarify ambiguous requests

Resolve material ambiguity before acting on a user message.

- Inspect the current message, relevant recent chat context, and available project evidence before asking.
- If one reasonable interpretation is low-risk and does not materially change scope, behavior, files, output, or external state, state the assumption and continue.
- If two or more plausible interpretations would lead to materially different work, pause and ask a targeted clarification. Name the likely meanings and their practical difference; prefer “Did you mean A or B?” over “Can you clarify?”
- Use the host's questions or structured user-input tool when available. Offer 2–3 mutually exclusive choices, put the recommended interpretation first when evidence supports one, and allow a free-form answer when the host supports it. Otherwise ask the same concise question in normal chat.
- Ask only the smallest set of blocking questions. Do not repeat questions answered by the request or context, and do not treat ambiguity as permission to broaden scope or make a consequential change.

## Host behavior

This skill is shared by Claude Code and Codex, so do not assume a specific agent API or model name.

Use Phase 1's area and risk assessment to choose execution before discovering
sub-agent tools. Single-agent review is the default on both hosts. Multiple
review perspectives do not require multiple agents. Honor explicit single-agent
or multi-agent requests within host permissions; permission to use sub-agents
alone does not require spawning them. Do not ask solely for delegation permission.

**In Codex:** Discover sub-agent tooling only when justified delegation is
selected. Use available read-only explorer/default agents for bounded tasks.
If tooling is unavailable or the user disables it, cover the same areas in the
main agent. Mention unavailable tooling once in the final output only when it
prevented planned delegation. Model selection follows the host's policy; do not
add cost-based model restrictions or overrides without an applicable reason.

**In Claude Code:** Apply the same routing with the available task/sub-agent
mechanism. Use Haiku for planning/filtering and Sonnet for routine review,
including a single reviewer covering several related perspectives. Single-agent
routing means one code reviewer, not permission to bypass the model policy below.

**Claude Code model and cost policy:**

- Never use Opus or Anthropic's highest-tier/most expensive model for Phase 1 planning or Phase 3 filtering.
- Never use Opus or Anthropic's highest-tier/most expensive model for routine specialist reviewers.
- Use an expensive Anthropic model only when the user explicitly asks for it, or for one targeted follow-up reviewer when the diff is unusually complex and a Sonnet pass found a high-impact but unresolved correctness, security, data-loss, or concurrency concern.
- If an expensive Anthropic model is used, state which reviewer used it and why in the final output.
- If Claude Code cannot force Haiku or Sonnet for routine review, run the reviewers sequentially in the main agent only when the current main model is not Opus or another expensive/highest-tier Anthropic model; otherwise ask before continuing.
- Prefer reducing reviewer count, narrowing context, or running sequentially over escalating models for ordinary diffs.

---

## Phase 1 — Read diff, map areas, and choose execution

Use the main agent or the host's lightweight planning agent to:

1. Fetch the full diff:
   - Use `git diff HEAD`.
   - If `HEAD` is unavailable, combine `git diff --cached` and `git diff`.
   - Use `git status --short --untracked-files=all` to detect untracked files.

2. Capture a short intent snapshot:
   - Summarize the user's stated goal for the change from the current request and available recent chat context.
   - If intent is clear, proceed with that snapshot.
   - If intent is unclear and intent could materially affect whether changed behavior is a bug or expected, ask the user to confirm it before Phase 2 when the host supports interactive input.
   - Offer 2–3 concise suggested intent options based on the request, chat context, and diff. Include a free-form/custom option when the host supports it so the user can type over the suggestions.
   - If the host does not support interactive input, the user asked for no questions, or review is running non-interactively, proceed and clearly separate stated intent from diff-based inference.
   - Use this snapshot to avoid flagging intentional behavior changes, but do not let it suppress bugs, regressions, security issues, data loss, or broken contracts.

3. Capture review focus notes:
   - Treat any text after the skill invocation as review focus and instructions for the reviewers. For example, `/hawk-quick-review use subagents Make sure data consistency is not compromised` requests sub-agent review and adds a data-consistency focus.
   - Also extract any specific concerns the user wants reviewers to check from recent chat context, such as "look closely at auth edge cases", "focus on UI regressions", or "check for simplification opportunities".
   - If no focus is provided, use "general review" and do not ask solely to collect focus notes.
   - Pass these notes to every reviewer. Treat them as emphasis, not as permission to ignore serious issues outside the focus.

4. Identify all changed file paths.
   - Include tracked paths from the diff.
   - Classify untracked files from `git status --short --untracked-files=all` as candidates, not automatically part of the change.
   - Automatically review untracked files eligible for commit: plausible project source, configuration, test, migration, or documentation files in normal project paths. Include relevant skill-maintained Markdown under `docs/generated/` for the
     mandatory knowledge pass. Skip other generated, binary, cache, log, scratch,
     vendored, and secret-looking files unless explicitly requested.
   - If untracked files are skipped or only partially reviewed, list them in the final output under "Untracked files not fully reviewed" with a short reason.
   - If important-looking untracked files are ambiguous, ask the user to stage them or rerun with explicit instructions to include them.

5. Collect relevant repo instruction files:
   - Root and directory-local `CLAUDE.md`, `AGENTS.md`, and `AGENTS.override.md`.
   - `CODEX.md` only if present; its absence never blocks review.
   - `.codex/*.md` and `.agents/*.md` only when directly applicable to the changed paths.
   - Documentation and matching `docs/generated/` knowledge entries that describe
     affected behavior or whose instruction read conditions apply to this work,
     verified against current source. Follow only relevant links; do not collect
     all docs referenced by an instruction file or index. Notes do not override
     instructions.
   Return the paths that were used.

6. Group eligible changes by affected behavior, shared source context, and contracts.
   File count and line count guide batching, not agent count. Review repetitive
   changes in batches when needed, checking every eligible change rather than
   sampling. Do not silently skip files; report deferred or partially reviewed paths.

7. Select the relevant perspectives below and choose execution using the routing
   rules that follow. Related perspectives can share one coherent review pass.
   Do not add perspectives or agents to fill slots. With no eligible changes,
   select zero code reviewers and run only the mandatory coordinator pass.
   Record the areas, relevant perspectives, execution mode, and concrete reason.

8. Add **simplification-reviewer** only when at least one of these is true:
   - The user explicitly asks for simplification, refactoring, cleanup, reuse, or maintainability review.
   - The diff adds or changes duplicated logic, repeated UI/component structure, repeated data transformations, or repeated control flow.
   - The diff is a large refactor or introduces a large new implementation where complexity is itself a review risk.
   - The changed code appears to reimplement a project-local helper, utility, component, abstraction, or pattern that is already imported, referenced, colocated, or visible in directly adjacent files.
   Do not run it by default for small, localized, or single-concern diffs.

### Area and risk routing

- Default to one agent when changes share behavior and context: repeated styling
  or layout changes, mechanical renames or moves, or a coherent feature with UI
  and straightforward state logic. Apply all relevant perspectives together;
  do not reread the full diff once per role.
- Confirm moves and renames preserve behavior, imports, references, registration,
  discovery, packaging, and module initialization where applicable before treating
  them as mechanical. Repetition does not establish low risk by itself.
- Delegate a bounded area when it needs substantial separate context, presents
  an independent consequential risk, or needs a targeted second assessment of a
  concrete unresolved concern. For example, UI plus a database migration may
  warrant a data delegate; auth plus independent API or persistence changes may
  warrant distinct specialists. A tiny concurrency, authorization, or migration
  diff can justify one targeted specialist despite its size.
- Several specialty labels, many files, or many lines alone do not justify
  delegation. One complex area may still be best reviewed by one agent when
  additional reviewers would repeat the same investigation.
- Use only the justified delegates, normally no more than three. Give each a
  distinct question, owned paths/behavior, required evidence, and connecting
  contracts. Keep related areas together; avoid overlapping full-diff reviews.
  Explicit multi-agent requests can justify an independent assessment, but still
  bound each assignment and avoid redundant role splits.
- Start with the coordinator's inspection and escalate only when new evidence
  warrants it. An added reviewer receives the specific unresolved concern and
  relevant context. Stop spawning once the required questions are covered.

**Available review perspectives:**

- **ui-reviewer**: For changes to views, layouts, components, styles, animations, or any visual layer code. Focuses on layout correctness, visual regressions, accessibility, and platform UI conventions.
- **logic-reviewer**: For changes to business logic, algorithms, state machines, control flow, or data transformations. Focuses on correctness, realistic reachable edge cases, and subtle bugs.
- **data-reviewer**: For changes to models, persistence, migrations, serialization, caching, database code, or changed data contracts. Focuses on data integrity, schema correctness, and consistency introduced by the diff. Do not select it for ordinary UI display data, sample data, labels, or simple in-memory arrays unless those changes alter persistence, schema, serialization, or cross-process contracts.
- **security-reviewer**: For changes touching auth, permissions, encryption, token handling, input validation, or any security boundary. Focuses on vulnerabilities and exposure risks.
- **api-reviewer**: For changes to network calls, API contracts, error handling, request/response parsing, or backend integration. Focuses on reachable contract-relevant failures, existing error-boundary behavior, and contract mismatches.

---

## Mandatory knowledge and Codex/Claude compatibility pass

Read [knowledge and compatibility review](references/knowledge-compatibility.md)
and perform its bounded pass on every invocation, including empty code diffs.
The coordinator owns this pass independently of the code specialist selection.
Select evidence from the reviewed work using that reference's relevance rules.
Check only applicable shared instructions, affected current knowledge/docs, and
host compatibility required for the work against the packaged shared specification.
The pass does not authorize a repository-wide documentation or setup audit.
Accepted issues are ordinary blocking findings. Keep the output section current
on every run, without modifying project files. Existing setup/documentation
problems qualify only when they govern or document the reviewed work; all other
review rules remain limited to the eligible change set.

## Phase 2 — Specialist review

In single-agent mode, perform one coherent code review applying all selected
perspectives, including simplification only when selected. The coordinator also
performs the mandatory knowledge/compatibility pass. Preserve the same scope,
coverage, evidence thresholds, and final candidate validation in either mode.

In delegated mode, the coordinator reviews retained areas and cross-area
interactions, and runs the mandatory knowledge/compatibility pass. Launch only
justified, independent assignments in parallel when the host permits it. Pass
each delegate the intent, focus, applicable instructions, relevant diff and
source context, and connecting contracts rather than the full diff by default.
Keep each prompt compact:

```text
Read-only review of <bounded area> using <relevant perspectives>. Do not edit files.
Question: <distinct risk or unresolved concern>.
Inputs: intent snapshot, review focus notes, assigned diff/paths, included untracked files, applicable instructions, needed source context, and connecting contracts.
Scope: review the assigned area; report only issues introduced by changed lines. Read changed files plus directly referenced definitions, call sites, schemas, or tests needed to verify a candidate issue. Do not do broad repo sweeps, external research, or unrelated architecture review.
Output: high-signal finding candidates. For each include file path, start_line/end_line, fix-location note, explanation, exact trigger, project-specific evidence that the trigger is realistic, changed code path, incorrect observable outcome, whether another independent failure is required, trigger-likelihood confidence, reachability confidence, incorrect-outcome confidence, and overall confidence. Overall confidence is the minimum of those three component scores. When acting as simplification-reviewer, also return any qualifying nice-to-have simplification leads under the rules below, clearly separated from findings. Separately, return up to 2 high-value test suggestions only when changed critical behavior warrants them. For each include the production path/line, suggested test kind, exact scenario or invariant, concrete regression value, evidence that nearby coverage does not already protect it, and test-value confidence from 0–100. Do not return test suggestions below 75. Do not include code snippets unless a deleted-code finding cannot be located any other way.
```

If planned delegation is unavailable or disabled, cover its areas in the main
agent, combining related perspectives and avoiding repeated full-diff reads.
Mention unavailable tooling once only when it prevented planned delegation.

**simplification-reviewer** runs only when selected in Phase 1. It focuses on simplification opportunities visible from the changed code: duplicated changed code that could be extracted into a shared helper or component, repeated patterns across changed files, overly verbose changed implementations where a clearer equivalent exists nearby, and reuse opportunities for existing utilities or abstractions already imported, referenced, or colocated with the changed files. Clarity means code a new human or agent can locate, explain, and safely modify; it does not mean minimizing files, abstractions, or lines. Responsibility-based validators, repositories, services, helpers, and UI components are desirable when they match project architecture. Do not flag a change merely for adding well-placed focused files. Its project scope is the current repository and the changed project area only. It may inspect nearby helpers, directly referenced utilities, colocated components, or immediately adjacent files, but must not use external research, inspect files outside the repository, or perform repo-wide searches for every possible similar implementation.

When the simplification-reviewer sees a plausible improvement but cannot prove it is worth changing, it may return a **nice-to-have simplification lead**, not a finding, only when it is project-local, genuinely simple, proportionate, non-blocking, and confidence 40–74. Limit leads to 3 and discard rare-condition hardening that would add disproportionate defensive complexity. Do not attach inline/file comments for leads.

**data-reviewer** must stay bounded to changed data behavior. It may inspect directly referenced model, migration, schema, serializer, cache, fixture, or API contract files needed to validate the diff. It must not inventory the full data model, audit unrelated tables/entities, or research upstream/downstream data flows unless the changed code directly modifies that contract.

### High-value test suggestions

Specialists may propose tests, but Phase 3 decides which, if any, become review suggestions. Surface them only for changed behavior where a focused test would materially protect a critical or error-prone invariant. Prioritize mappings and conversions, parsing or serialization, state transitions, authorization boundaries, monetary calculations, persistence or migrations, idempotency, and cross-process or API contracts. Complex branching may qualify when a specific consequential outcome can be exercised.

Score each suggestion's **test-value confidence** from 0–100 based on project evidence that the changed behavior is consequential, realistically regression-prone, not already protected, and expressible as a focused invariant. Use 25 for trivial, duplicate, or coverage-for-coverage's-sake ideas; 50 for plausible but minor or weakly evidenced value; 75 for a specific material regression risk with a clear invariant; and 100 for a critical contract or high-impact mapping with direct evidence. Confidence measures the value of adding this test, not whether the production code is currently correct.

Keep each suggestion concise: name the relevant production location, test kind, exact scenario or invariant, regression value, nearby-coverage evidence, and confidence score.

Discard suggestions below 75. Do not suggest broad coverage, tests for trivial accessors or presentation copy, duplicates of nearby existing tests, or a test merely because coverage is absent. Inspect the nearest existing tests only when needed to avoid duplication or identify the appropriate level. Never write or modify tests during review. A missing test is never a finding or review limitation, even when repository instructions call for one; it may only appear as a suggestion when it meets the threshold. Test suggestions do not count toward `Found N issues`, do not affect `Ready to commit from review perspective.`, and do not receive inline/file comments. They are advice only, never authorization to implement test work.

A failing test is not a test suggestion. Report it as a finding only when evidence proves that the eligible change set introduced the failure or materially changed the behavior that now fails. If an unproven failure blocks validation of changed behavior, report a concise review limitation. Omit pre-existing or unrelated failures when they do not block that validation. Never recommend rewriting or deleting a test merely to make review pass.

### Realistic trigger gate and proportional remedies

Before a candidate can become a finding, prove both the changed code path and incorrect outcome **and** that the initiating trigger is realistically likely in this project's current environment. Logical possibility, API fallibility, or the fact that an operation can throw is not trigger evidence.

Require at least one of these forms of trigger evidence:

- A deterministic path from normal supported use.
- A failing or missing behavior exercised by an existing test.
- Production evidence, logs, or a reported incident.
- A documented, reasonably common platform behavior applicable to this project's configuration.
- A current caller or workflow that produces the state.
- A user action supported by the application or documented operating procedure.

Apply the gate as follows:

- Discard triggers based only on manual corruption, unsupported file editing, arbitrary tampering, generic transient infrastructure errors, or simultaneous independent failures. These become candidates only when project-specific evidence shows they realistically occur.
- For every multi-failure chain, verify every material link and establish that each additional failure is realistically likely during the preceding failure. For example, do not report “deployment health check fails → optional IIS worker query also fails → restoration is skipped” merely because both remote operations can throw.
- Report filesystem, persistence, network, WinRM, IIS, or monitoring exceptions only when project-specific evidence establishes the concrete failure mode and existing handling produces an unacceptable observable result. First assess existing error boundaries and ordinary error handling; do not assume automatic retry, compensation, or recovery is required.
- Do not infer unrelated persistence, network, device, or platform failures from input validation or another already-proven failure. Do not report states excluded by enforced types, validation, schema constraints, or documented invariants.
- Preserve deterministic bugs in ordinary execution, common edge cases supported by current callers, security boundaries reachable by an actual lower-privileged actor, data loss reachable through normal workflows, and contract violations demonstrated by code, tests, or documented behavior.
- Score trigger likelihood, reachability, and incorrect-outcome confidence separately. Overall confidence must equal their minimum; impact must not raise it above the weakest material link. A finding requires trigger-likelihood confidence ≥ 75 and overall confidence ≥ 75.
- Treat defensive improvement for a rare or unsupported condition as non-finding hardening. Only the simplification-reviewer may return it as a nice-to-have lead under the lead rules above; otherwise discard it.
- Describe what breaks and the required outcome. Prefer an existing shared error boundary when remedy context helps, and recommend guards, retries, recovery, or fallbacks only for a demonstrated case. Never recommend silently swallowing errors or disproportionate defensive architecture.
- Treat approximately 500 lines in a hand-written file as a cohesion-review signal, not a defect by itself. Recommend responsibility-based decomposition, never arbitrary splitting by line count.

Each reviewer should:
- Read the assigned diff and relevant connecting contracts.
- Read the intent snapshot and treat clearly intentional behavior changes as non-issues, while still flagging changed code that appears to violate that intent or introduce high-impact bugs.
- Read the review focus notes and prioritize those concerns without ignoring serious issues in the assigned specialty.
- Read enough surrounding context in the actual source files to understand each change — typically 20–40 lines around each hunk, or the full function/class if small.
- Stop gathering context once the reviewer can either support a concrete finding or rule out the concern. Prefer "no issue found" over expanding into adjacent systems.
- Before reporting an issue, apply the realistic trigger gate and establish every link from the diff or an included untracked file, plus local source context.
- Apply all assigned perspectives within the owned area. Flag serious cross-area
  concerns to the coordinator with their concrete evidence; the coordinator owns
  interaction checks and any justified follow-up.
- Check compliance with provided repo instruction files where relevant to its specialty. Prefer files named `CLAUDE.md`, `CODEX.md`, `AGENTS.md`, directly applicable `.codex/*.md` / `.agents/*.md` files, or files explicitly referenced by those instructions.
- Return a list of issues. For each issue include:
  - Repo-relative file path
  - Exact start_line and end_line in the current file where the fix should be made
  - If the finding concerns removed code or a missing block, attach it to the nearest surviving line where the replacement, guard, call site, or restored behavior should be added
  - A short fix-location note when the relevant failing behavior spans multiple files or the best fix is not on the changed line
  - A short explanation
  - Exact trigger
  - Project-specific evidence that the trigger is realistic
  - Changed code path
  - Incorrect observable outcome
  - Whether another independent failure is required
  - Trigger-likelihood confidence, reachability confidence, incorrect-outcome confidence, and overall confidence (0–100), where overall is their minimum:
    - 0: False positive or pre-existing issue.
    - 25: Might be real but unverified, depends on a speculative or negligibly likely failure, or is a stylistic issue not in repo instructions. Do not surface it.
    - 50: Plausible but below the finding threshold. Only eligible as a nice-to-have simplification lead when all lead rules apply.
    - 75: Evidence-supported and realistically likely enough to block a commit.
    - 100: Confirmed deterministic or frequent behavior.

---

## Phase 3 — Filter and output

Use the main agent or the host's lightweight planning agent to:
- Merge candidates from the code review and any delegates with the mandatory
  knowledge/compatibility pass. Check interactions between reviewed areas and
  connecting contracts; specialist coverage alone does not establish integration correctness.
- Independently validate each finding candidate against the diff or an included untracked file, plus local source context; mandatory knowledge/setup candidates use their explicitly scoped current instructions and docs. For each, answer internally: What exact event starts the failure? Does normal supported usage produce it? What current evidence makes it likely enough to matter? Does it require another independent failure? Is the remedy proportional to the demonstrated likelihood? Would an experienced maintainer reasonably block the commit over it? Discard the candidate if any answer is not concrete.
- For any failing test, require evidence that the eligible change set introduced the failure or materially changed the failing behavior before keeping it as a finding. When an unproven failure blocks validation of changed behavior, report only a concise review limitation. Omit pre-existing or unrelated failures entirely unless they block that validation. Do not call a test stale or broken without evidence.
- Recompute the three confidence components and their minimum. Reject every finding candidate with trigger-likelihood confidence below 75 or overall confidence below 75, regardless of impact. Do not mention discarded candidates, low confidence scores, or possible defensive improvements in the final review.
- Keep nice-to-have simplification leads separate from finding candidates; apply their 40–74 confidence and proportionality rules instead of the finding threshold.
- Discard findings based on hypothetical concerns, style preferences, unsupported failure prevention, unverified assumptions, or exceptions already handled with an acceptable observable outcome.
- Deduplicate overlapping findings.
- Merge and deduplicate test suggestions separately. Independently recompute test-value confidence and discard every suggestion below 75. Keep at most 3, retaining only the highest-confidence, most critical, specific, and non-duplicative suggestions under the criteria above.
- After filtering and deduplicating, assign stable IDs in final-output order: `F1`, `F2`, … for findings and `S1`, `S2`, … for nice-to-have simplification leads. Reuse each finding ID in its inline/file comment when comments are supported.
- If simplification-reviewer ran, optionally include up to 3 clearly labeled "Nice-to-have simplification leads" after the findings. These are exploratory follow-ups, not blocking review issues, and must not be counted in "Found N issues".
- When present, include a clearly labeled "Suggested tests" section after simplification leads. Show each suggestion's test-value confidence. These are optional, non-blocking ideas and must not be counted as findings or review limitations.
- Whenever the eligible change set is non-empty, include exactly one `Suggested commit message:` line, whether or not the review found issues, simplification leads, suggested tests, scope gaps, skipped files, or required unrun checks.
- If the eligible change set is empty, report `Nothing to review.` for code, still output the mandatory compatibility section and its findings, and do not suggest a commit message.
- Include `Ready to commit from review perspective.` only when the eligible change set is non-empty and fully reviewed, no findings remain, the mandatory knowledge/compatibility status is `passed`, no important untracked files were skipped or only partially reviewed, and repository instructions do not require an unrun check. Suggested tests and simplification leads do not prevent this conclusion. Otherwise, state the findings or review limitation concisely while still including the suggested commit message.
- Derive the message from the reviewed change's actual outcome, not the review process. Return exactly one plain-language sentence that starts with an uppercase letter and ends with a period. Do not use a conventional-commit prefix, quotes, markdown code formatting, multiple alternatives, or vague wording such as "Update files".
- Always include **Knowledge and Codex/Claude compatibility** with `passed`,
  `blocked`, or `not verified`, the inspected paths and their relevance, and
  relevant finding IDs. Unrelated docs left outside scope do not make this pass
  incomplete. Count each finding once. `blocked` and `not verified` prevent readiness.
- Report execution mode (single agent or delegated), a short concrete reason,
  and the perspectives actually applied. Distinguish planned delegation that
  fell back to one agent from intentional single-agent routing.
- Produce final output.
- Do not include code snippets by default. Snippets are often noisy in the final combined review. Use only file/line attachments and concise explanations. Include a snippet only when the host cannot attach file/line references and the finding would otherwise be ambiguous.

Return the review in the final assistant response. In CLI-style hosts, terminal output is acceptable.

When the host supports inline/file comments, attach every finding directly to the relevant file and line range using the host's native mechanism. In Codex Desktop, emit one `::code-comment{...}` directive per finding after the human-readable summary. Use an absolute path, or a workspace-resolvable path that includes the workspace folder segment, and 1-based `start`/`end` line numbers. Keep each directive tightly scoped to the line(s) where the fix should happen, not the whole hunk or file.

Format — short sections, bullet list, no ordered lists, no tables, no JSON, no fenced code blocks unless absolutely necessary:

---

### Code review

Review mode: delegated — UI and persistence changes require distinct context.
Perspectives: ui-reviewer, data-reviewer.  *(list those actually applied)*

Found N issues:

- **F1 · P1 `path/to/File.swift:42`** — brief description of what breaks and where to fix it.
- **F2 · P2 `path/to/Other.swift:87-89`** — brief description of what breaks and where to fix it.
- **F3 · P2 `CLAUDE.md:1`** — the required shared-instruction import points to a missing file; restore its target.

Knowledge and Codex/Claude compatibility: blocked — F3 identifies a broken required import.
*(Use passed or not verified with the inspected paths when appropriate.)*

Nice-to-have simplification leads:  *(only include when present)*

- **S1 `path/to/Helper.swift:14`** — brief non-blocking simplification opportunity.

Suggested tests:  *(only include when present)*

- **90% confidence `path/to/Mapper.swift:31`** — Unit-test every supported external status and the fallback invariant; this protects the import mapping from silent regressions not covered nearby.

Suggested commit message: Add resilient status mapping for imported orders.

Inline comments attached: N  *(only include this line when inline/file comments were actually emitted)*

Generated with hawk-quick-review

---

Or if no issues:

---

### Code review

Review mode: single agent — related logic changes share behavior and context.
Perspectives: logic-reviewer.  *(list those actually applied)*

No issues found.

Knowledge and Codex/Claude compatibility: passed — AGENTS.md and CLAUDE.md govern these paths; docs/status-mapping.md matches the changed mapping.

Ready to commit from review perspective.

Suggested tests:  *(only include when present)*

- **90% confidence `path/to/Mapper.swift:31`** — Unit-test every supported external status and the fallback invariant; this protects the import mapping from silent regressions not covered nearby.

Suggested commit message: Add stable review IDs and a remediation workflow.

Generated with hawk-quick-review

---

## False positives to ignore

- Pre-existing code issues not introduced by these changes; the mandatory scoped knowledge/setup pass is the explicit exception
- Things that look like bugs but aren't
- Pedantic nitpicks a senior engineer wouldn't flag
- Issues a linter/compiler/typechecker/formatter would catch
- Missing or inadequate test coverage; it may only appear as a non-blocking test suggestion when it meets the high-value criteria
- Documentation style preferences and unrelated gaps; concrete mandatory knowledge/compatibility defects remain blocking findings
- Repo instruction issues explicitly silenced in code (eg. lint-ignore comments)
- Intentional behavioral changes clearly part of the purpose of this change
- Real code issues unrelated to modified, added, deleted, or untracked code; applicable mandatory knowledge/setup issues remain in scope
- Imaginary edge cases without an evidence-supported reachable trigger
- Multi-step failure chains whose local failure, retry behavior, or non-idempotent remote effect is only assumed
- Local persistence failures whose likelihood is only assumed from the fact that the storage API can throw
- Network-failure remedies that assume automatic retry or recovery without proving ordinary error handling is inadequate
- Possible exceptions already handled with the required observable outcome
- IIS worker enumeration failing after a separate deployment health failure, without evidence that the second failure is realistically likely during the first
- A valid environment state file being manually replaced with another environment's state file
- A post-success monitoring query throwing despite succeeding during current deployment testing, without evidence of realistic occurrence
- A timestamp collision already protected by an environment deployment lock
- Any concern whose only trigger is manual corruption or unsupported operator behavior
- Structural preferences based only on minimizing file, abstraction, or line count

## Notes

- Do not write or modify tests
- Do not run builds, typechecks, or test suites unless the user explicitly asks for verification
- Do not post GitHub comments or review remote PRs; this skill is local-only
