---
name: quick-review
description: >-
  Adaptive code review — picks specialist agents based on what changed. Works
  on local uncommitted changes or a specific PR. Use when asked to review code,
  check a PR, or audit recent changes.
allowed-tools: Bash(gh issue view:*), Bash(gh search:*), Bash(gh issue list:*), Bash(gh pr comment:*), Bash(gh pr diff:*), Bash(gh pr view:*), Bash(gh pr list:*), Bash(git diff:*), Bash(git status:*), Bash(git log:*)
---

Provide a code review using an adaptive 3-phase pipeline that picks reviewers based on what actually changed.

Works in two modes:
- **PR mode**: if a PR number or URL is passed as an argument, review that pull request.
- **Local mode**: if no argument is given, review all uncommitted local changes (`git diff HEAD`, including staged).

---

## Phase 1 — Read diff and pick specialists (Haiku agent)

Use a Haiku agent to:

1. Fetch the full diff:
   - PR mode: use `gh pr diff`
   - Local mode: use `git diff HEAD` (plus `git diff --cached` for staged-only files)

2. Identify all changed file paths.

3. Collect relevant CLAUDE.md files: root CLAUDE.md + any CLAUDE.md in directories containing changed files. Return their paths.

4. In PR mode only: check if the PR is closed, draft, trivial/automated, or already reviewed by you. If so, stop.

5. Analyze what kind of changes are present and select **1 to 3 specialist agents** from the list below. Pick only the ones that are genuinely relevant — do not pick a specialist just to fill slots. Return the selected specialist names and a short reason for each.

Note: **simplification-reviewer always runs** — do not select or skip it, it is launched unconditionally in Phase 2.

**Available specialists (pick 1–3 based on the diff):**

- **ui-reviewer**: For changes to views, layouts, components, styles, animations, or any visual layer code. Focuses on layout correctness, visual regressions, accessibility, and platform UI conventions.
- **logic-reviewer**: For changes to business logic, algorithms, state machines, control flow, or data transformations. Focuses on correctness, edge cases, and subtle bugs.
- **data-reviewer**: For changes to models, persistence, migrations, serialization, caching, or database code. Focuses on data integrity, schema correctness, and consistency.
- **security-reviewer**: For changes touching auth, permissions, encryption, token handling, input validation, or any security boundary. Focuses on vulnerabilities and exposure risks.
- **api-reviewer**: For changes to network calls, API contracts, error handling, request/response parsing, or backend integration. Focuses on failure modes, retry logic, and contract mismatches.

---

## Phase 2 — Specialist review (parallel Sonnet agents)

Launch one Sonnet agent per selected specialist **plus always one simplification-reviewer**, all in parallel. Each agent receives: the full diff, the list of CLAUDE.md file paths, and its specialist focus.

**simplification-reviewer** always runs regardless of what changed. It focuses on: duplicated code that could be extracted into a shared helper or component, repeated patterns across files, overly verbose implementations where a simpler equivalent exists, and reuse opportunities for existing utilities or abstractions already present in the codebase. It should read beyond the diff to check whether similar logic already exists elsewhere before flagging.

Each agent should:
- Read the diff.
- Read enough surrounding context in the actual source files to understand each change — typically 20–40 lines around each hunk, or the full function/class if small.
- Review only through the lens of its specialty (a ui-reviewer should not flag logic bugs; a logic-reviewer should not flag UI conventions).
- Check compliance with the provided CLAUDE.md files where relevant to its specialty.
- Return a list of issues. For each issue include:
  - File path and line number
  - A 1–3 line code snippet from the actual file (not the diff)
  - A short explanation
  - Confidence score (0–100):
    - 0: False positive or pre-existing issue.
    - 25: Might be real but unverified; stylistic issue not in CLAUDE.md.
    - 50: Real but minor or infrequent.
    - 75: Real, important, likely hit in practice, or directly in CLAUDE.md.
    - 100: Confirmed, definitely real, will happen frequently.

---

## Phase 3 — Filter and output (Haiku agent)

Use a Haiku agent to:
- Merge issues from all specialist agents.
- Filter to issues with confidence ≥ 80.
- Deduplicate overlapping findings.
- Produce final output.

**In PR mode:** post a comment with `gh pr comment`.
**In local mode:** print directly to the terminal.

Format — numbered list, no tables, no JSON:

---

### Code review

Reviewed by: ui-reviewer, logic-reviewer  *(list whichever ran)*

Found N issues:

1. **`path/to/File.swift` line 42** — brief description (CLAUDE.md says "..." or: bug because <reason>)
   ```swift
   let x = doSomething()
   return x + 1
   ```
   https://github.com/owner/repo/blob/[full-sha]/path/to/File.swift#L40-L44
   *(omit link in local mode)*

2. **`path/to/Other.swift` line 87** — brief description
   ```swift
   // snippet
   ```

🤖 Generated with [Claude Code](https://claude.ai/code)

---

Or if no issues:

---

### Code review

Reviewed by: logic-reviewer  *(list whichever ran)*

No issues found.

🤖 Generated with [Claude Code](https://claude.ai/code)

---

## False positives to ignore

- Pre-existing issues not introduced by these changes
- Things that look like bugs but aren't
- Pedantic nitpicks a senior engineer wouldn't flag
- Issues a linter/compiler/typechecker/formatter would catch
- General quality issues (coverage, docs) unless required by CLAUDE.md
- CLAUDE.md issues explicitly silenced in code (eg. lint-ignore comments)
- Intentional behavioral changes clearly part of the purpose of this change
- Real issues on lines that were not modified

## Notes

- In PR mode, do not build, run tests, or typecheck — CI handles those separately
- In local mode, agents may run a quick typecheck or build if it helps confirm a specific suspicion, but should not do a full test suite run
- Use `gh` for all GitHub interaction in PR mode
- Links must use full SHA: https://github.com/owner/repo/blob/[full-sha]/path/file#L[start]-L[end]
- Provide at least 1 line of context before and after each flagged line in links
