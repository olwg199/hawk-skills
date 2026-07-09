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
- **logic-reviewer**: For changes to business logic, algorithms, state machines, control flow, or data transformations. Focuses on correctness, edge cases, and subtle bugs.
- **data-reviewer**: For changes to models, persistence, migrations, serialization, caching, database code, or changed data contracts. Focuses on data integrity, schema correctness, and consistency introduced by the diff. Do not select it for ordinary UI display data, sample data, labels, or simple in-memory arrays unless those changes alter persistence, schema, serialization, or cross-process contracts.
- **security-reviewer**: For changes touching auth, permissions, encryption, token handling, input validation, or any security boundary. Focuses on vulnerabilities and exposure risks.
- **api-reviewer**: For changes to network calls, API contracts, error handling, request/response parsing, or backend integration. Focuses on failure modes, retry logic, and contract mismatches.

---

## Phase 2 — Specialist review

Run one review pass per selected specialist. Include **simplification-reviewer** only if Phase 1 selected it.

When sub-agents are available and the user has not opted out, launch these review passes in parallel. In Codex, use the discovered sub-agent tool and prefer read-only explorer/default agents for these bounded review tasks. Keep each spawned reviewer prompt compact:

```text
Read-only <specialist> review. Do not edit files.
Inputs: intent snapshot, review focus notes, full diff, included untracked files, changed files, repo instructions, and needed source context.
Scope: review only through your specialty; report only issues introduced by changed lines. Read changed files plus directly referenced definitions, call sites, schemas, or tests needed to verify a candidate issue. Do not do broad repo sweeps, external research, or unrelated architecture review.
Output: high-signal findings only, each with file path, start_line/end_line, fix-location note, explanation, evidence chain (trigger → changed code path → incorrect outcome), and confidence. Do not include code snippets unless a deleted-code finding cannot be located any other way.
```

When sub-agents are unavailable or the user opted out, perform the same reviewer passes sequentially in the main agent and keep their findings separated by reviewer role until Phase 3. Mention unavailable tooling once in the final output only when it caused the fallback.

**simplification-reviewer** runs only when selected in Phase 1. It focuses on simplification opportunities visible from the changed code: duplicated changed code that could be extracted into a shared helper or component, repeated patterns across changed files, overly verbose changed implementations where a simpler equivalent exists nearby, and reuse opportunities for existing utilities or abstractions already imported, referenced, or colocated with the changed files. Its project scope is the current repository and the changed project area only. It may inspect nearby helpers, directly referenced utilities, colocated components, or immediately adjacent files, but must not use external research, inspect files outside the repository, or perform repo-wide searches for every possible similar implementation.

When the simplification-reviewer sees a plausible improvement but cannot prove it is worth changing, it should return it as a **nice-to-have simplification lead**, not as a review finding. Nice-to-have leads must be project-local, non-blocking, confidence 40–74, and limited to at most 3 items. Do not attach inline/file comments for nice-to-have leads.

**data-reviewer** must stay bounded to changed data behavior. It may inspect directly referenced model, migration, schema, serializer, cache, fixture, or API contract files needed to validate the diff. It must not inventory the full data model, audit unrelated tables/entities, or research upstream/downstream data flows unless the changed code directly modifies that contract.

Each reviewer should:
- Read the diff.
- Read the intent snapshot and treat clearly intentional behavior changes as non-issues, while still flagging changed code that appears to violate that intent or introduce high-impact bugs.
- Read the review focus notes and prioritize those concerns without ignoring serious issues in the assigned specialty.
- Read enough surrounding context in the actual source files to understand each change — typically 20–40 lines around each hunk, or the full function/class if small.
- Stop gathering context once the reviewer can either support a concrete finding or rule out the concern. Prefer "no issue found" over expanding into adjacent systems.
- Before reporting an issue, verify and state its evidence chain: a concrete trigger, the changed code path it reaches, and the resulting incorrect outcome. Do not report a finding unless this chain can be established from the diff or an included untracked file, plus local source context.
- Review only through the lens of its specialty (a ui-reviewer should not flag logic bugs; a logic-reviewer should not flag UI conventions).
- Check compliance with provided repo instruction files where relevant to its specialty. Prefer files named `CLAUDE.md`, `CODEX.md`, `AGENTS.md`, directly applicable `.codex/*.md` / `.agents/*.md` files, or files explicitly referenced by those instructions.
- Return a list of issues. For each issue include:
  - Repo-relative file path
  - Exact start_line and end_line in the current file where the fix should be made
  - If the finding concerns removed code or a missing block, attach it to the nearest surviving line where the replacement, guard, call site, or restored behavior should be added
  - A short fix-location note when the relevant failing behavior spans multiple files or the best fix is not on the changed line
  - A short explanation
  - Evidence chain: trigger → changed code path → incorrect outcome
  - Confidence score (0–100):
    - 0: False positive or pre-existing issue.
    - 25: Might be real but unverified; stylistic issue not in repo instructions.
    - 50: Real but minor or infrequent.
    - 75: Real, important, likely hit in practice, or directly in repo instructions.
    - 100: Confirmed, definitely real, will happen frequently.

---

## Phase 3 — Filter and output

Use the main agent or the host's lightweight planning agent to:
- Merge issues from all specialist reviewers.
- Independently validate each candidate's evidence chain against the diff or an included untracked file, plus local source context. Discard findings that rely on hypothetical concerns, style preferences, or unverified assumptions.
- Filter to issues with confidence ≥ 75.
- Deduplicate overlapping findings.
- After filtering and deduplicating, assign stable IDs in final-output order: `F1`, `F2`, … for findings and `S1`, `S2`, … for nice-to-have simplification leads. Reuse each finding ID in its inline/file comment when comments are supported.
- If simplification-reviewer ran, optionally include up to 3 clearly labeled "Nice-to-have simplification leads" after the findings. These are exploratory follow-ups, not blocking review issues, and must not be counted in "Found N issues".
- Offer a commit message only when the review has no findings, the eligible change set is non-empty and fully reviewed, no important untracked files were skipped or only partially reviewed, and repository instructions do not require an unrun check. Do not offer one when there are findings, review-scope gaps, required unrun checks, or no changes to commit.
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

## Notes

- Do not run builds, typechecks, or test suites unless the user explicitly asks for verification
- Do not post GitHub comments or review remote PRs; this skill is local-only
