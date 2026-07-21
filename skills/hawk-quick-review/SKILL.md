---
name: hawk-quick-review
description: >-
  Adaptive code review that picks specialist reviewer roles based on what
  changed. Uses parallel sub-agents by default when the host supports them,
  otherwise runs the same review roles sequentially. Reviews local uncommitted
  changes, considering the user's stated intent from the current request and
  available chat context. Use only when the user explicitly asks to review
  local code, changes, or the worktree before commit, or invokes
  `$hawk-quick-review`. Do not auto-use for general questions about review
  practices, review skills, or whether a review approach is good.
allowed-tools: Bash(git diff:*), Bash(git status:*), Bash(git log:*)
---

Provide a code review using an adaptive 3-phase pipeline that picks reviewers based on what actually changed.

Reviews local uncommitted changes only. Fetch the diff with `git diff HEAD`, including staged and unstaged tracked changes. If `HEAD` is unavailable, combine `git diff --cached` and `git diff`. Also check `git status --short --untracked-files=all` for untracked files, but do not assume every untracked file belongs to the change.

---

## Host behavior

This skill is shared by Claude Code and Codex, so do not assume a specific agent API or model name.

**In Codex:**

1. Unless the user explicitly asks for a single-agent review or says not to use sub-agents, discover whether sub-agent tooling is available using the host's tool-discovery or native subagent mechanism when one is exposed.
2. If a sub-agent tool is available, use it for Phase 2 by default.
3. If sub-agents are unavailable, undiscoverable, not visible in the current UI, or explicitly disabled by the user, run the selected reviewer roles sequentially in the main agent. Mention the fallback once in the final output only when it was caused by unavailable tooling, not when the user opted out.
4. Do not add cost-based model restrictions for Codex. Let Codex choose or inherit the model according to the host's policy, unless the user explicitly requests a model or the task clearly needs a specific override.
5. Do not ask solely for permission to use sub-agents. Treat parallel specialist review as the default.

**In Claude Code:**

Unless the user explicitly asks for a single-agent review or says not to use sub-agents, use Claude Code's available task/sub-agent mechanism for Phase 2. Use Haiku for planning/filtering and Sonnet for routine specialist review.

**Claude Code model and cost policy:**

- Never use Opus or Anthropic's highest-tier/most expensive model for Phase 1 planning or Phase 3 filtering.
- Never use Opus or Anthropic's highest-tier/most expensive model for routine specialist reviewers.
- Use an expensive Anthropic model only when the user explicitly asks for it, or for one targeted follow-up reviewer when the diff is unusually complex and a Sonnet pass found a high-impact but unresolved correctness, security, data-loss, or concurrency concern.
- If an expensive Anthropic model is used, state which reviewer used it and why in the final output.
- If Claude Code cannot force Haiku or Sonnet for routine review, run the reviewers sequentially in the main agent only when the current main model is not Opus or another expensive/highest-tier Anthropic model; otherwise ask before continuing.
- Prefer reducing reviewer count, narrowing context, or running sequentially over escalating models for ordinary diffs.

---

## Phase 1 — Read diff and pick specialists

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
   - Treat any text after the skill invocation as review focus and instructions for the reviewers. For example, `/hawk-quick-review use subagents Make sure data consistency is not compromised` both permits sub-agents and adds a data-consistency focus.
   - Also extract any specific concerns the user wants reviewers to check from recent chat context, such as "look closely at auth edge cases", "focus on UI regressions", or "check for simplification opportunities".
   - If no focus is provided, use "general review" and do not ask solely to collect focus notes.
   - Pass these notes to every reviewer. Treat them as emphasis, not as permission to ignore serious issues outside the focus.

4. Identify all changed file paths.
   - Include tracked paths from the diff.
   - Classify untracked files from `git status --short --untracked-files=all` as candidates, not automatically part of the change.
   - Automatically review untracked files eligible for commit: plausible project source, configuration, test, migration, or documentation files in normal project paths. Skip generated, binary, cache, log, scratch, vendored, and secret-looking files unless explicitly requested.
   - If untracked files are skipped or only partially reviewed, list them in the final output under "Untracked files not fully reviewed" with a short reason.
   - If important-looking untracked files are ambiguous, ask the user to stage them or rerun with explicit instructions to include them.

5. Collect relevant repo instruction files:
   - Root and directory-local `CLAUDE.md`, `CODEX.md`, and `AGENTS.md`.
   - `.codex/*.md` and `.agents/*.md` only when directly applicable to the changed paths.
   - Other files only when explicitly referenced by one of the instruction files above.
   Return the paths that were used.

6. If the diff is large or touches many files, group changed paths by risk area and review in batches. Do not silently skip files because of context size; summarize any files that were deferred or only partially reviewed.

7. Analyze what kind of changes are present and select **1 to 3 specialist reviewer roles** from the list below. Pick only the ones that are genuinely relevant — do not pick a specialist just to fill slots. Return the selected specialist names and a short reason for each.

8. Add **simplification-reviewer** only when at least one of these is true:
   - The user explicitly asks for simplification, refactoring, cleanup, reuse, or maintainability review.
   - The diff adds or changes duplicated logic, repeated UI/component structure, repeated data transformations, or repeated control flow.
   - The diff is a large refactor or introduces a large new implementation where complexity is itself a review risk.
   - The changed code appears to reimplement a project-local helper, utility, component, abstraction, or pattern that is already imported, referenced, colocated, or visible in directly adjacent files.
   Do not run it by default for small, localized, or single-concern diffs.

**Available specialists (pick 1–3 based on the diff):**

- **ui-reviewer**: For changes to views, layouts, components, styles, animations, or any visual layer code. Focuses on layout correctness, visual regressions, accessibility, and platform UI conventions.
- **logic-reviewer**: For changes to business logic, algorithms, state machines, control flow, or data transformations. Focuses on correctness, realistic reachable edge cases, and subtle bugs.
- **data-reviewer**: For changes to models, persistence, migrations, serialization, caching, database code, or changed data contracts. Focuses on data integrity, schema correctness, and consistency introduced by the diff. Do not select it for ordinary UI display data, sample data, labels, or simple in-memory arrays unless those changes alter persistence, schema, serialization, or cross-process contracts.
- **security-reviewer**: For changes touching auth, permissions, encryption, token handling, input validation, or any security boundary. Focuses on vulnerabilities and exposure risks.
- **api-reviewer**: For changes to network calls, API contracts, error handling, request/response parsing, or backend integration. Focuses on reachable contract-relevant failures, existing error-boundary behavior, and contract mismatches.

---

## Phase 2 — Specialist review

Run one review pass per selected specialist. Include **simplification-reviewer** only if Phase 1 selected it.

When sub-agents are available and the user has not opted out, launch these review passes in parallel. In Codex, use the discovered sub-agent tool and prefer read-only explorer/default agents for these bounded review tasks. Keep each spawned reviewer prompt compact:

```text
Read-only <specialist> review. Do not edit files.
Inputs: intent snapshot, review focus notes, full diff, included untracked files, changed files, repo instructions, and needed source context.
Scope: review only through your specialty; report only issues introduced by changed lines. Read changed files plus directly referenced definitions, call sites, schemas, or tests needed to verify a candidate issue. Do not do broad repo sweeps, external research, or unrelated architecture review.
Output: high-signal candidates only. For each include file path, start_line/end_line, fix-location note, explanation, exact trigger, project-specific evidence that the trigger is realistic, changed code path, incorrect observable outcome, whether another independent failure is required, trigger-likelihood confidence, reachability confidence, incorrect-outcome confidence, and overall confidence. Overall confidence is the minimum of those three component scores. Do not include code snippets unless a deleted-code finding cannot be located any other way.
```

When sub-agents are unavailable or the user opted out, perform the same reviewer passes sequentially in the main agent and keep their findings separated by reviewer role until Phase 3. Mention unavailable tooling once in the final output only when it caused the fallback.

**simplification-reviewer** runs only when selected in Phase 1. It focuses on simplification opportunities visible from the changed code: duplicated changed code that could be extracted into a shared helper or component, repeated patterns across changed files, overly verbose changed implementations where a clearer equivalent exists nearby, and reuse opportunities for existing utilities or abstractions already imported, referenced, or colocated with the changed files. Clarity means code a new human or agent can locate, explain, and safely modify; it does not mean minimizing files, abstractions, or lines. Responsibility-based validators, repositories, services, helpers, and UI components are desirable when they match project architecture. Do not flag a change merely for adding well-placed focused files. Its project scope is the current repository and the changed project area only. It may inspect nearby helpers, directly referenced utilities, colocated components, or immediately adjacent files, but must not use external research, inspect files outside the repository, or perform repo-wide searches for every possible similar implementation.

When the simplification-reviewer sees a plausible improvement but cannot prove it is worth changing, it may return a **nice-to-have simplification lead**, not a finding, only when it is project-local, genuinely simple, proportionate, non-blocking, and confidence 40–74. Limit leads to 3 and discard rare-condition hardening that would add disproportionate defensive complexity. Do not attach inline/file comments for leads.

**data-reviewer** must stay bounded to changed data behavior. It may inspect directly referenced model, migration, schema, serializer, cache, fixture, or API contract files needed to validate the diff. It must not inventory the full data model, audit unrelated tables/entities, or research upstream/downstream data flows unless the changed code directly modifies that contract.

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
- Read the diff.
- Read the intent snapshot and treat clearly intentional behavior changes as non-issues, while still flagging changed code that appears to violate that intent or introduce high-impact bugs.
- Read the review focus notes and prioritize those concerns without ignoring serious issues in the assigned specialty.
- Read enough surrounding context in the actual source files to understand each change — typically 20–40 lines around each hunk, or the full function/class if small.
- Stop gathering context once the reviewer can either support a concrete finding or rule out the concern. Prefer "no issue found" over expanding into adjacent systems.
- Before reporting an issue, apply the realistic trigger gate and establish every link from the diff or an included untracked file, plus local source context.
- Review only through the lens of its specialty (a ui-reviewer should not flag logic bugs; a logic-reviewer should not flag UI conventions).
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
- Merge issues from all specialist reviewers.
- Independently validate each finding candidate against the diff or an included untracked file, plus local source context. For each, answer internally: What exact event starts the failure? Does normal supported usage produce it? What current evidence makes it likely enough to matter? Does it require another independent failure? Is the remedy proportional to the demonstrated likelihood? Would an experienced maintainer reasonably block the commit over it? Discard the candidate if any answer is not concrete.
- Recompute the three confidence components and their minimum. Reject every finding candidate with trigger-likelihood confidence below 75 or overall confidence below 75, regardless of impact. Do not mention discarded candidates, low confidence scores, or possible defensive improvements in the final review.
- Keep nice-to-have simplification leads separate from finding candidates; apply their 40–74 confidence and proportionality rules instead of the finding threshold.
- Discard findings based on hypothetical concerns, style preferences, unsupported failure prevention, unverified assumptions, or exceptions already handled with an acceptable observable outcome.
- Deduplicate overlapping findings.
- After filtering and deduplicating, assign stable IDs in final-output order: `F1`, `F2`, … for findings and `S1`, `S2`, … for nice-to-have simplification leads. Reuse each finding ID in its inline/file comment when comments are supported.
- If simplification-reviewer ran, optionally include up to 3 clearly labeled "Nice-to-have simplification leads" after the findings. These are exploratory follow-ups, not blocking review issues, and must not be counted in "Found N issues".
- Whenever the final output reports `No issues found.`, always include exactly one `Suggested commit message:` line. Review-scope gaps, skipped or partially reviewed untracked files, and required unrun checks may prevent a ready-to-commit conclusion, but they must not suppress the commit message for the changes that were reviewed.
- If the eligible change set is empty, report `Nothing to review.` instead of `No issues found.` and do not suggest a commit message.
- Include `Ready to commit from review perspective.` only when the eligible change set is non-empty and fully reviewed, no important untracked files were skipped or only partially reviewed, and repository instructions do not require an unrun check. Otherwise, state the review limitation concisely while still including the suggested commit message.
- Derive the message from the reviewed change's actual outcome, not the review process. Return exactly one plain-language sentence that starts with an uppercase letter and ends with a period. Do not use a conventional-commit prefix, quotes, markdown code formatting, multiple alternatives, or vague wording such as "Update files".
- Produce final output.
- Do not include code snippets by default. Snippets are often noisy in the final combined review. Use only file/line attachments and concise explanations. Include a snippet only when the host cannot attach file/line references and the finding would otherwise be ambiguous.

Return the review in the final assistant response. In CLI-style hosts, terminal output is acceptable.

When the host supports inline/file comments, attach every finding directly to the relevant file and line range using the host's native mechanism. In Codex Desktop, emit one `::code-comment{...}` directive per finding after the human-readable summary. Use an absolute path, or a workspace-resolvable path that includes the workspace folder segment, and 1-based `start`/`end` line numbers. Keep each directive tightly scoped to the line(s) where the fix should happen, not the whole hunk or file.

Format — short sections, bullet list, no ordered lists, no tables, no JSON, no fenced code blocks unless absolutely necessary:

---

### Code review

Reviewed by: ui-reviewer, logic-reviewer  *(list whichever ran; mention single-agent fallback only if sub-agents were unavailable)*

Found N issues:

- **F1 · P1 `path/to/File.swift:42`** — brief description of what breaks and where to fix it.
- **F2 · P2 `path/to/Other.swift:87-89`** — brief description of what breaks and where to fix it.

Nice-to-have simplification leads:  *(only include when present)*

- **S1 `path/to/Helper.swift:14`** — brief non-blocking simplification opportunity.

Inline comments attached: N  *(only include this line when inline/file comments were actually emitted)*

Generated with hawk-quick-review

---

Or if no issues:

---

### Code review

Reviewed by: logic-reviewer  *(list whichever ran; mention single-agent fallback only if sub-agents were unavailable)*

No issues found.

Ready to commit from review perspective.

Suggested commit message: Add stable review IDs and a remediation workflow.

Generated with hawk-quick-review

---

## False positives to ignore

- Pre-existing issues not introduced by these changes
- Things that look like bugs but aren't
- Pedantic nitpicks a senior engineer wouldn't flag
- Issues a linter/compiler/typechecker/formatter would catch
- General quality issues (coverage, docs) unless required by repo instructions
- Repo instruction issues explicitly silenced in code (eg. lint-ignore comments)
- Intentional behavioral changes clearly part of the purpose of this change
- Real issues unrelated to modified, added, deleted, or untracked code
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

- Do not run builds, typechecks, or test suites unless the user explicitly asks for verification
- Do not post GitHub comments or review remote PRs; this skill is local-only
