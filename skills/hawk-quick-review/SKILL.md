---
name: hawk-quick-review
description: >-
  Adaptive code review that picks specialist reviewer roles based on what
  changed. Uses parallel sub-agents when the host supports and permits them,
  otherwise runs the same review roles sequentially. Reviews local uncommitted
  changes, considering the user's stated intent from the current request and
  available chat context. Use when asked to review code, audit local changes,
  or check the current worktree before commit.
allowed-tools: Bash(git diff:*), Bash(git status:*), Bash(git log:*)
---

Provide a code review using an adaptive 3-phase pipeline that picks reviewers based on what actually changed.

Reviews local uncommitted changes only. Fetch the diff with `git diff HEAD`, including staged and unstaged tracked changes. If `HEAD` is unavailable, combine `git diff --cached` and `git diff`. Also check `git status --short --untracked-files=all` for untracked files, but do not assume every untracked file belongs to the change.

---

## Host behavior

This skill is shared by Claude Code and Codex, so do not assume a specific agent API or model name.

**In Codex:**

1. Before Phase 2, discover whether sub-agents are available using the host's tool-discovery or native subagent mechanism when one is exposed.
2. If a sub-agent tool is available and the current user request explicitly permits sub-agents, delegation, or parallel agent work, use it for Phase 2. Example permission phrases include "use sub-agents", "parallel agents are allowed", or "delegate the specialist review passes".
3. Do not add cost-based model restrictions for Codex. Let Codex choose or inherit the model according to the host's policy, unless the user explicitly requests a model or the task clearly needs a specific override.
4. If sub-agents are unavailable, undiscoverable, not visible in the current UI, or not explicitly permitted by the current user request, run the selected reviewer roles sequentially in the main agent. This is normal single-agent mode, not a failure.
5. Do not ask solely for permission to use sub-agents. Only ask if the user requested parallelism but the permission is ambiguous.

**In Claude Code:**

Use Claude Code's available task/sub-agent mechanism for Phase 2 when possible. Use Haiku for planning/filtering and Sonnet for routine specialist review.

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

3. Identify all changed file paths.
   - Include tracked paths from the diff.
   - Classify untracked files from `git status --short --untracked-files=all` as candidates, not automatically part of the change.
   - Automatically review untracked files only when they look like intentional source/config/test/migration files in normal project paths.
   - Do not read obvious scratch, log, cache, build output, generated, vendored, binary, or secret-looking untracked files unless the user explicitly asks.
   - If untracked files are skipped or only partially reviewed, list them in the final output under "Untracked files not fully reviewed" with a short reason.
   - If important-looking untracked files are ambiguous, ask the user to stage them or rerun with explicit instructions to include them.

4. Collect relevant repo instruction files:
   - Root and directory-local `CLAUDE.md`, `CODEX.md`, and `AGENTS.md`.
   - `.codex/*.md` and `.agents/*.md` only when directly applicable to the changed paths.
   - Other files only when explicitly referenced by one of the instruction files above.
   Return the paths that were used.

5. If the diff is large or touches many files, group changed paths by risk area and review in batches. Do not silently skip files because of context size; summarize any files that were deferred or only partially reviewed.

6. Analyze what kind of changes are present and select **1 to 3 specialist reviewer roles** from the list below. Pick only the ones that are genuinely relevant — do not pick a specialist just to fill slots. Return the selected specialist names and a short reason for each.

Note: **simplification-reviewer always runs** — do not select or skip it, it runs unconditionally in Phase 2.

**Available specialists (pick 1–3 based on the diff):**

- **ui-reviewer**: For changes to views, layouts, components, styles, animations, or any visual layer code. Focuses on layout correctness, visual regressions, accessibility, and platform UI conventions.
- **logic-reviewer**: For changes to business logic, algorithms, state machines, control flow, or data transformations. Focuses on correctness, edge cases, and subtle bugs.
- **data-reviewer**: For changes to models, persistence, migrations, serialization, caching, or database code. Focuses on data integrity, schema correctness, and consistency.
- **security-reviewer**: For changes touching auth, permissions, encryption, token handling, input validation, or any security boundary. Focuses on vulnerabilities and exposure risks.
- **api-reviewer**: For changes to network calls, API contracts, error handling, request/response parsing, or backend integration. Focuses on failure modes, retry logic, and contract mismatches.

---

## Phase 2 — Specialist review

Run one review pass per selected specialist **plus always one simplification-reviewer**.

When sub-agents are available and permitted, launch these review passes in parallel. In Codex, use the discovered sub-agent tool and prefer read-only explorer/default agents for these bounded review tasks. Each spawned reviewer must be told:

- This is a read-only code review task.
- Do not edit files.
- Review only through the assigned specialty.
- Use the intent snapshot, full diff, changed file list, relevant repo instructions (`CLAUDE.md`, `CODEX.md`, `AGENTS.md`, etc.), and surrounding source context.
- Return only high-signal findings for issues introduced by the changed lines.

When sub-agents are unavailable or not permitted, perform the same reviewer passes sequentially in the main agent and keep their findings separated by reviewer role until Phase 3. If the user did not request parallel sub-agents, do not call attention to missing authorization; at most say "single-agent mode" in the Reviewed by line when useful.

**simplification-reviewer** always runs regardless of what changed. It focuses on: duplicated code that could be extracted into a shared helper or component, repeated patterns across files, overly verbose implementations where a simpler equivalent exists, and reuse opportunities for existing utilities or abstractions already present in the codebase. It should read beyond the diff to check whether similar logic already exists elsewhere before flagging.

Each reviewer should:
- Read the diff.
- Read the intent snapshot and treat clearly intentional behavior changes as non-issues, while still flagging changed code that appears to violate that intent or introduce high-impact bugs.
- Read enough surrounding context in the actual source files to understand each change — typically 20–40 lines around each hunk, or the full function/class if small.
- Review only through the lens of its specialty (a ui-reviewer should not flag logic bugs; a logic-reviewer should not flag UI conventions).
- Check compliance with provided repo instruction files where relevant to its specialty. Prefer files named `CLAUDE.md`, `CODEX.md`, `AGENTS.md`, directly applicable `.codex/*.md` / `.agents/*.md` files, or files explicitly referenced by those instructions.
- Return a list of issues. For each issue include:
  - File path and line number
  - A 1–3 line code snippet from the actual file (not the diff)
  - For deletion-only findings where the relevant code no longer exists, include the relevant diff hunk plus the nearest surviving context instead
  - A short explanation
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
- Filter to issues with confidence ≥ 75.
- Deduplicate overlapping findings.
- Produce final output.

Return the review in the final assistant response. In CLI-style hosts, terminal output is acceptable.

Format — numbered list, no tables, no JSON:

---

### Code review

Reviewed by: ui-reviewer, logic-reviewer  *(list whichever ran; mention single-agent fallback only if sub-agents were unavailable or not permitted)*

Found N issues:

1. **`path/to/File.swift` line 42** — brief description (repo instructions say "..." or: bug because <reason>)
   ```swift
   let x = doSomething()
   return x + 1
   ```
2. **`path/to/Other.swift` line 87** — brief description
   ```swift
   // snippet
   ```

Generated with hawk-quick-review

---

Or if no issues:

---

### Code review

Reviewed by: logic-reviewer  *(list whichever ran; mention single-agent fallback only if sub-agents were unavailable or not permitted)*

No issues found.

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
