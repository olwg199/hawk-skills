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

Provide a code review using a 3-phase pipeline: assign investigation, gather
evidence, then adjudicate candidates in the current main agent. Researchers own
discovery; the main agent owns final judgment and targeted source verification.

Remain read-only: do not edit code, docs, memory, or instruction files. Review
local uncommitted changes plus the mandatory scoped knowledge and Codex/Claude
compatibility pass below. Include staged and unstaged tracked changes relative
to `HEAD`, plus eligible untracked files. In delegated mode, researchers fetch
their assigned diffs; the main agent need not load the full diff. If `HEAD` is
unavailable, combine staged and unstaged diffs. Do not assume every untracked
file belongs to the change.

---

## Clarify ambiguous requests

Resolve material ambiguity before acting on a user message.

- Inspect the current message, relevant recent chat context, and available project evidence before asking.
- If one reasonable interpretation is low-risk and does not materially change scope, behavior, files, output, or external state, state the assumption and continue.
- If two or more plausible interpretations would lead to materially different work, pause and ask a targeted clarification. Name the likely meanings and their practical difference; prefer “Did you mean A or B?” over “Can you clarify?”
- Use the host's questions or structured user-input tool when available. Offer 2–3 mutually exclusive choices, put the recommended interpretation first when evidence supports one, and allow a free-form answer when the host supports it. Otherwise ask the same concise question in normal chat.
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

Use a stronger researcher for a named, consequential question that the routine
researcher cannot resolve or an assigned area whose difficulty exceeds that
researcher's capability. Give it only the relevant evidence and missing question;
do not repeat the full review with a stronger model. Narrow context and reduce
redundant researchers before escalating. Report stronger investigations and why
they were needed. The main agent still makes every final decision.

---

## Phase 1 — Inventory changes and assign investigation

The current main agent coordinates this phase without researching every hunk:

1. Fetch a compact change inventory:
   - Use `git diff HEAD --name-status` and `git diff HEAD --stat`.
   - If `HEAD` is unavailable, inventory both `git diff --cached` and `git diff`.
   - Use `git status --short --untracked-files=all` to detect untracked files.
   - Read selected hunks only when needed to assign ownership or clarify intent.
     Let a researcher map ambiguous areas and return a short summary when that
     requires substantive investigation. Fetch the full diff only in single-agent
     mode; researchers use `git diff HEAD -- <assigned paths>`, or both staged
     and unstaged path-scoped diffs without `HEAD`, and read eligible untracked
     files directly.

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
   - Include tracked paths from the inventory.
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

8. Include **simplification-reviewer** as a perspective in every non-empty code
   review. Every researcher checks its area for simpler approaches alongside
   correctness. This does not require a separate agent or a suggestion quota.

### Area and risk routing

- Keep related changes with one researcher: repeated styling or layout changes,
  mechanical renames or moves, or a coherent feature with UI and state logic.
  Use the main agent directly for small mechanical changes when delegation would
  add overhead. Apply relevant perspectives together, without repeated diff reads.
- Confirm moves and renames preserve behavior, imports, references, registration,
  discovery, packaging, and module initialization where applicable before treating
  them as mechanical. Repetition does not establish low risk by itself.
- Add a separate researcher when a bounded area needs substantial separate
  context, presents
  an independent consequential risk, or needs a targeted second assessment of a
  concrete unresolved concern. For example, UI plus a database migration may
  warrant a data delegate; auth plus independent API or persistence changes may
  warrant distinct specialists. A tiny concurrency, authorization, or migration
  diff can justify one targeted specialist despite its size.
- Several specialty labels, many files, or many lines alone do not justify
  additional researchers. Keep one complex area with one researcher when others
  would repeat the same investigation.
- Use only the justified delegates, normally no more than three. Give each a
  distinct question, owned paths/behavior, required evidence, and connecting
  contracts. Keep related areas together; avoid overlapping full-diff reviews.
  Explicit multi-agent requests can justify an independent assessment, but still
  bound each assignment and avoid redundant role splits.
- Assign every eligible path and relevant connecting contract an owner. Researchers
  return coverage summaries, interaction concerns, and gaps. The coordinator checks
  those summaries against the inventory and routes missing coverage or interaction
  questions explicitly, rather than independently rereading the whole diff.
  Stop spawning once the required questions are covered.

**Available review perspectives:**

- **ui-reviewer**: For changes to views, layouts, components, styles, animations, or any visual layer code. Focuses on layout correctness, visual regressions, accessibility, and platform UI conventions.
- **logic-reviewer**: For changes to business logic, algorithms, state machines, control flow, or data transformations. Focuses on correctness, realistic reachable edge cases, and subtle bugs.
- **data-reviewer**: For changes to models, persistence, migrations, serialization, caching, database code, or changed data contracts. Focuses on data integrity, schema correctness, and consistency introduced by the diff. Do not select it for ordinary UI display data, sample data, labels, or simple in-memory arrays unless those changes alter persistence, schema, serialization, or cross-process contracts.
- **security-reviewer**: For changes touching auth, permissions, encryption, token handling, input validation, or any security boundary. Focuses on vulnerabilities and exposure risks.
- **api-reviewer**: For changes to network calls, API contracts, error handling, request/response parsing, or backend integration. Focuses on reachable contract-relevant failures, existing error-boundary behavior, and contract mismatches.
- **simplification-reviewer**: Always applied to changed code. Looks for clearer
  equivalent approaches, unnecessary abstractions or indirection, duplicated
  logic, overly complicated control flow, and useful reuse within the affected area.

---

## Mandatory knowledge and Codex/Claude compatibility pass

Read [knowledge and compatibility review](references/knowledge-compatibility.md)
and perform its bounded pass on every invocation, including empty code diffs.
The coordinator owns this pass independently of the code specialist selection.
It may delegate bounded evidence gathering, but validates candidates and owns
the final compatibility status. Researchers use the candidate reporting rules
below; final compatibility findings use the same acceptance gate as code findings.
Select evidence from the reviewed work using that reference's relevance rules.
Check only applicable shared instructions, affected current knowledge/docs, and
host compatibility required for the work against the packaged shared specification.
The pass does not authorize a repository-wide documentation or setup audit.
Accepted issues are ordinary blocking findings. Keep the output section current
on every run, without modifying project files. Existing setup/documentation
problems qualify only when they govern or document the reviewed work; all other
review rules remain limited to the eligible change set.

## Phase 2 — Research and candidate reporting

In single-agent mode, perform one coherent review applying the selected
perspectives and simplification, then apply Phase 3's final acceptance rules.
In delegated mode, researchers cover every assigned hunk and included untracked
file, including relevant connecting contracts. The main agent coordinates coverage
and targeted follow-ups rather than reviewing assigned areas again. Independent
assignments can run in parallel when permitted. Pass intent, focus, applicable
instructions, owned paths, and relevant contracts, without copying the full chat
or full diff to every researcher. Keep the assignment compact:

```text
Read-only investigation of <bounded area> using <perspectives> plus simplification. Do not edit files; run builds/tests only if the user explicitly requested verification.
Question: <owned behavior, risk, or unresolved interaction>.
Inputs: intent, focus, assigned paths/untracked files, applicable instructions, connecting contracts.
Read your assigned diff and necessary source context. Cover every assigned change; inspect directly referenced definitions, callers, schemas, or nearby tests as needed. Avoid broad repo sweeps, external research, and unrelated architecture review.
Return a compact coverage summary (paths/behavior inspected, contracts checked, gaps) and candidate packets. For each candidate: category, current path/lines, claim, concrete code signal, trigger and suspected outcome or simpler alternative, supporting evidence, counterevidence, unknowns, and the exact missing verification. Include claim confidence and impact/value separately. Do not apply the final finding threshold or discard a concrete concern merely because one evidence link remains unverified. Separately return relevant test ideas with scenario, regression value, and known coverage or coverage uncertainty. The main agent decides what reaches the final review.
```

### Lower internal reporting gate

Forward a candidate when a specific changed-code signal supports a plausible
consequential defect or useful simplification, even if the trigger, caller, or
outcome is not fully verified. Identify the missing link and how to check it.
Do not require final confidence, proven trigger likelihood, or a blocking remedy
before reporting. Do not invent evidence to complete the packet. Distinguish
observed facts from assumptions and explicitly mention counterevidence, such as
an existing guard or error boundary whose adequacy remains uncertain.

Discard disproven concerns, unrelated/pre-existing code defects, pure style
preferences, and generic speculation without a concrete code signal. The final
false-positive rules below do not suppress an evidence-backed internal candidate
solely because verification is incomplete. Internal candidates are not findings
or final review limitations. Do not impose a top-N candidate quota that silently
hides material concerns; keep packets concise and deduplicate within your area.

Stop investigating once a candidate is supported enough for targeted adjudication,
ruled out, or has a clearly stated missing verification requiring a follow-up.
Return consequential interaction questions to the coordinator with relevant source
references. Do not expand into adjacent systems to force a confident answer.
This stopping rule bounds each concern's investigation; continue reviewing the
remaining assigned changes before returning the coverage summary.

For each packet, include current repo-relative path and line range, plus a brief
fix-location note if behavior spans files. Cite source locations for supporting
evidence and counterevidence so the main agent can verify them directly. Attach removed-code or missing-block
concerns to the nearest surviving owner line. Rate confidence in the claim's
correctness from 0–100 as a rough judgment, not a calibrated probability. Describe
trigger frequency/reachability and impact or improvement value separately. An
unknown link is explicitly unknown; neither serious impact nor a high score
substitutes for evidence. No numeric floor applies to internal candidates.

### Simpler approaches

Every researcher and single-agent reviewer checks for unnecessary abstractions,
indirection, configuration, branching, duplication, and reimplemented nearby
helpers or components. Propose a concrete simpler alternative, explain which
complexity it removes, and show how required behavior and contracts are preserved.
State any remaining equivalence question for the main agent to resolve.

Clarity means code a human or agent can locate, explain, and safely modify; it
is not minimizing files or lines. Respect useful responsibility-based validators,
repositories, services, helpers, and UI components that fit the project. A roughly
500-line hand-written file is a cohesion signal, not a defect or a reason for
arbitrary splitting. Inspect only the affected area, directly referenced utilities,
colocated components, or adjacent files; do not search the entire repository for
possible reuse. Avoid rare-condition hardening that adds disproportionate complexity.

Keep simplification candidates separate from defects. A confident, worthwhile
simplification can remain optional when behavior is correct. Optional improvements
have no numeric confidence band or upper confidence cap. The main agent
selects up to 3 worthwhile **nice-to-have simplification leads** for final output;
they never block readiness or receive inline/file comments.

**data-reviewer** stays bounded to changed data behavior and directly relevant
models, migrations, schemas, serializers, caches, fixtures, or API contracts.
Do not inventory unrelated entities or upstream/downstream flows unless the
changed code directly modifies that contract.

### High-value test suggestions

Researchers may forward concrete test ideas with unverified value or nearby coverage, naming the missing check; no final score cutoff applies to internal test candidates. The main agent decides which, if any, become final suggestions. Surface them only for changed behavior where a focused test would materially protect a critical or error-prone invariant. Prioritize mappings and conversions, parsing or serialization, state transitions, authorization boundaries, monetary calculations, persistence or migrations, idempotency, and cross-process or API contracts. Complex branching may qualify when a specific consequential outcome can be exercised.

The main agent scores each final suggestion's **test-value confidence** from 0–100 based on project evidence that the changed behavior is consequential, realistically regression-prone, not already protected, and expressible as a focused invariant. Use 25 for trivial, duplicate, or coverage-for-coverage's-sake ideas; 50 for plausible but minor or weakly evidenced value; 75 for a specific material regression risk with a clear invariant; and 100 for a critical contract or high-impact mapping with direct evidence. Confidence measures the value of adding this test, not whether the production code is currently correct.

Keep each suggestion concise: name the relevant production location, test kind, exact scenario or invariant, regression value, nearby-coverage evidence, and confidence score.

In final output, discard suggestions below 75. Do not suggest broad coverage, tests for trivial accessors or presentation copy, duplicates of nearby existing tests, or a test merely because coverage is absent. Inspect the nearest existing tests only when needed to avoid duplication or identify the appropriate level. Never write or modify tests during review. A missing test is never a finding or review limitation, even when repository instructions call for one; it may only appear as a suggestion when it meets the threshold. Test suggestions do not count toward `Found N issues`, do not affect `Ready to commit from review perspective.`, and do not receive inline/file comments. They are advice only, never authorization to implement test work.

A failing test is not a test suggestion. Report it as a finding only when evidence proves that the eligible change set introduced the failure or materially changed the behavior that now fails. If an unproven failure blocks validation of changed behavior, report a concise review limitation. Omit pre-existing or unrelated failures when they do not block that validation. Never recommend rewriting or deleting a test merely to make review pass.

### Final finding gate and proportional remedies

Only the main agent applies this acceptance gate. Before a candidate becomes a final finding, prove both the changed code path and incorrect outcome **and** that the initiating trigger is realistically likely in this project's current environment. Logical possibility, API fallibility, or the fact that an operation can throw is not trigger evidence.

Require at least one of these forms of trigger evidence:

- A deterministic path from normal supported use.
- A failing or missing behavior exercised by an existing test.
- Production evidence, logs, or a reported incident.
- A documented, reasonably common platform behavior applicable to this project's configuration.
- A current caller or workflow that produces the state.
- A user action supported by the application or documented operating procedure.

Apply the gate as follows:

- Discard triggers based only on manual corruption, unsupported file editing, arbitrary tampering, generic transient infrastructure errors, or simultaneous independent failures. Keep them as final findings only when project-specific evidence shows they realistically occur.
- For every multi-failure chain, verify every material link and establish that each additional failure is realistically likely during the preceding failure. For example, do not report “deployment health check fails → optional IIS worker query also fails → restoration is skipped” merely because both remote operations can throw.
- Report filesystem, persistence, network, WinRM, IIS, or monitoring exceptions only when project-specific evidence establishes the concrete failure mode and existing handling produces an unacceptable observable result. First assess existing error boundaries and ordinary error handling; do not assume automatic retry, compensation, or recovery is required.
- Do not infer unrelated persistence, network, device, or platform failures from input validation or another already-proven failure. Do not report states excluded by enforced types, validation, schema constraints, or documented invariants.
- Preserve deterministic bugs in ordinary execution, common edge cases supported by current callers, security boundaries reachable by an actual lower-privileged actor, data loss reachable through normal workflows, and contract violations demonstrated by code, tests, or documented behavior.
- Require claim-correctness confidence ≥ 75, with evidence supporting the trigger,
  changed path, and incorrect outcome. Assess trigger realism/frequency and impact
  separately when deciding whether a maintainer would block the commit. Do not
  treat confidence as occurrence frequency or let impact compensate for missing
  evidence; an uncertain material link prevents accepting the finding.
- Treat unsupported defensive improvement as non-finding hardening. Keep optional
  improvements only under the simpler-approach rules; do not use that section to
  smuggle speculative failure prevention into the final review.
- Describe what breaks and the required outcome. Prefer an existing shared error boundary when remedy context helps, and recommend guards, retries, recovery, or fallbacks only for a demonstrated case. Never recommend silently swallowing errors or disproportionate defensive architecture.
- Treat approximately 500 lines in a hand-written file as a cohesion-review signal, not a defect by itself. Recommend responsibility-based decomposition, never arbitrary splitting by line count.

---

## Phase 3 — Main-agent adjudication and output

The current main agent performs this phase; do not delegate final filtering,
severity, usefulness, compatibility status, or readiness judgment:

- Check researcher coverage against the inventory. Assign uncovered paths and
  consequential connecting-contract questions to bounded follow-ups. Coverage
  summaries establish what was inspected, not proof that the code is correct.
- Read the actual current source and relevant diff around each candidate, plus
  directly needed callers/contracts and counterevidence. Expand only far enough
  to settle that claim; do not repeat the full diff investigation. If a packet
  lacks necessary evidence, request that exact check rather than accept its score.
- Use a stronger targeted researcher when the unresolved question requires it.
  Independently assess the returned evidence before making the final decision.
- Classify candidates as accepted findings, worthwhile optional improvements,
  rejected concerns, or unresolved material questions. Weak suspicion alone is
  not a limitation; a concrete consequential question or important coverage gap
  that cannot be resolved is. Report it concisely and withhold readiness.
- Merge candidates from the code review and any delegates with the mandatory
  knowledge/compatibility pass and targeted interaction checks. Specialist
  coverage alone does not establish integration correctness.
- Independently validate each finding candidate against the diff or an included untracked file, plus local source context; mandatory knowledge/setup candidates use their explicitly scoped current instructions and docs. For each, answer internally: What exact event starts the failure? Does normal supported usage produce it? What current evidence makes it likely enough to matter? Does it require another independent failure? Is the remedy proportional to the demonstrated likelihood? Would an experienced maintainer reasonably block the commit over it? Do not accept a finding if any answer is not concrete; seek targeted evidence or classify it under the unresolved-question rules above.
- For any failing test, require evidence that the eligible change set introduced the failure or materially changed the failing behavior before keeping it as a finding. When an unproven failure blocks validation of changed behavior, report only a concise review limitation. Omit pre-existing or unrelated failures entirely unless they block that validation. Do not call a test stale or broken without evidence.
- Independently assess claim confidence, trigger realism, and impact under the
  final finding gate. Reject unsupported findings regardless of researcher score.
  Do not mention rejected candidates or their scores in the final review; report
  only material unresolved limitations under the rules above.
- Keep simplification leads separate from defects. Select concrete, proportionate
  improvements worth considering, including confident improvements to correct
  code; apply no confidence ceiling. Explain the simpler alternative and value,
  and label any remaining verification before implementation.
- Discard findings based on hypothetical concerns, style preferences, unsupported failure prevention, unverified assumptions, or exceptions already handled with an acceptable observable outcome.
- Deduplicate overlapping findings.
- Merge and deduplicate test suggestions separately. Independently recompute test-value confidence and discard every suggestion below 75. Keep at most 3, retaining only the highest-confidence, most critical, specific, and non-duplicative suggestions under the criteria above.
- After filtering and deduplicating, assign stable IDs in final-output order: `F1`, `F2`, … for findings and `S1`, `S2`, … for nice-to-have simplification leads. Reuse each finding ID in its inline/file comment when comments are supported.
- Optionally include up to 3 clearly labeled "Nice-to-have simplification leads" after the findings. These are exploratory follow-ups, not blocking review issues, and must not be counted in "Found N issues".
- When present, include a clearly labeled "Suggested tests" section after simplification leads. Show each suggestion's test-value confidence. These are optional, non-blocking ideas and must not be counted as findings or review limitations.
- Whenever the eligible change set is non-empty, include exactly one `Suggested commit message:` line, whether or not the review found issues, simplification leads, suggested tests, scope gaps, skipped files, or required unrun checks.
- If the eligible change set is empty, report `Nothing to review.` for code, still output the mandatory compatibility section and its findings, and do not suggest a commit message.
- Include `Ready to commit from review perspective.` only when the eligible change set is non-empty and fully reviewed, no findings remain, the mandatory knowledge/compatibility status is `passed`, no important untracked files were skipped or only partially reviewed, no material unresolved questions remain, and repository instructions do not require an unrun check. Suggested tests and simplification leads do not prevent this conclusion. Otherwise, state the findings or review limitation concisely while still including the suggested commit message.
- Derive the message from the reviewed change's actual outcome, not the review process. Return exactly one plain-language sentence that starts with an uppercase letter and ends with a period. Do not use a conventional-commit prefix, quotes, markdown code formatting, multiple alternatives, or vague wording such as "Update files".
- Always include **Knowledge and Codex/Claude compatibility** with `passed`,
  `blocked`, or `not verified`, the inspected paths and their relevance, and
  relevant finding IDs. Unrelated docs left outside scope do not make this pass
  incomplete. Count each finding once. `blocked` and `not verified` prevent readiness.
- Report execution mode (single agent or delegated), a short concrete reason,
  and the perspectives actually applied. Distinguish planned delegation that
  fell back to one agent from intentional single-agent routing. In delegated mode,
  state the actual researcher models/efforts and any stronger targeted investigation.
- Produce final output.
- Do not include code snippets by default. Snippets are often noisy in the final combined review. Use only file/line attachments and concise explanations. Include a snippet only when the host cannot attach file/line references and the finding would otherwise be ambiguous.

Return the review in the final assistant response. In CLI-style hosts, terminal output is acceptable.

When the host supports inline/file comments, attach every finding directly to the relevant file and line range using the host's native mechanism. In Codex Desktop, emit one `::code-comment{...}` directive per finding after the human-readable summary. Use an absolute path, or a workspace-resolvable path that includes the workspace folder segment, and 1-based `start`/`end` line numbers. Keep each directive tightly scoped to the line(s) where the fix should happen, not the whole hunk or file.

Format — short sections, bullet list, no ordered lists, no tables, no JSON, no fenced code blocks unless absolutely necessary:

---

### Code review

Review mode: delegated — UI and persistence changes require distinct context.
Researchers: Sonnet; main agent adjudicated candidates.
Perspectives: ui-reviewer, data-reviewer, simplification-reviewer.  *(list those actually applied)*

Found N issues:

- **F1 · P1 `path/to/File.swift:42`** — brief description of what breaks and where to fix it.
- **F2 · P2 `path/to/Other.swift:87-89`** — brief description of what breaks and where to fix it.
- **F3 · P2 `CLAUDE.md:1`** — the required shared-instruction import points to a missing file; restore its target.

Knowledge and Codex/Claude compatibility: blocked — F3 identifies a broken required import.
*(Use passed or not verified with the inspected paths when appropriate.)*

Nice-to-have simplification leads:  *(only include when present)*

- **S1 `path/to/Helper.swift:14`** — reuse the nearby validator to remove duplicate rules while preserving supported input behavior; optional.

Suggested tests:  *(only include when present)*

- **90% confidence `path/to/Mapper.swift:31`** — Unit-test every supported external status and the fallback invariant; this protects the import mapping from silent regressions not covered nearby.

Suggested commit message: Add resilient status mapping for imported orders.

Inline comments attached: N  *(only include this line when inline/file comments were actually emitted)*

Generated with hawk-quick-review

---

Or if no issues:

---

### Code review

Review mode: single agent — small mechanical changes make delegation unnecessary.
Perspectives: logic-reviewer, simplification-reviewer.  *(list those actually applied)*

No issues found.

Knowledge and Codex/Claude compatibility: passed — AGENTS.md and CLAUDE.md govern these paths; docs/status-mapping.md matches the changed mapping.

Ready to commit from review perspective.

Suggested tests:  *(only include when present)*

- **90% confidence `path/to/Mapper.swift:31`** — Unit-test every supported external status and the fallback invariant; this protects the import mapping from silent regressions not covered nearby.

Suggested commit message: Add stable review IDs and a remediation workflow.

Generated with hawk-quick-review

---

## False positives to exclude from final findings

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
