---
name: hawk-fix-review-findings
description: >-
  Fix explicitly supplied local code-review findings, including nice-to-have
  simplification leads, from the preceding hawk-quick-review output or pasted
  review text. Use only when the user asks to address, fix, or remediate review
  findings, or invokes $hawk-fix-review-findings. Do not auto-use for general
  bug fixes, feature work, or a new code review.
---

# Hawk Fix Review Findings

Treat the supplied review report as the scope of work. Repair its findings; do not turn this into a second general review.

## Input

1. Read the immediately preceding `hawk-quick-review` output. Include every reported issue and every **Nice-to-have simplification lead** by default.
2. If that output is unavailable, ask the user to paste the review findings. Do not rerun `hawk-quick-review` unless the user explicitly asks.
3. Treat user comments supplied with the review as instructions to prioritize, skip, or clarify listed findings. Do not treat them as unrelated new work.
4. Preserve the review's stable IDs: `F1`, `F2`, … for findings and `S1`, `S2`, … for simplification leads. For pasted legacy review text without IDs, assign those IDs in report order and show the mapping before acting on user comments. Record each item with its ID, source location, requested outcome, and current status. An item may be `active`, `fixed`, `skipped`, `blocked`, or `verification failed`.

## Scope and decisions

Work one finding at a time:

- Start at its reported file and line. Read only the changed code, directly related definitions, callers, tests, or contracts needed to understand and repair it.
- Expand investigation only when the local evidence requires it. Do not read or re-review the full diff, perform broad repository sweeps, or reopen general review questions.
- Do not require a second proof of every review finding. Skip a finding only when direct local context makes it clearly stale, duplicate, invalid, or already resolved; state why.
- Before editing, identify any finding that needs a breaking API or data-contract change, migration, permission change, or unresolved product-behavior choice. If one exists, present the affected finding and concrete options, then wait for direction before editing any files. Keep the batch atomic.
- Make the smallest root-cause patch that resolves the finding. Do not add unrelated refactors, cleanups, or behavior changes.
- Add or update focused regression coverage when the repository has an established nearby test pattern that can exercise the corrected behavior. Do not run it yet.

## Delegation

This skill is shared by Claude Code and Codex; do not assume a host-specific agent API or model name.

1. Unless the user requests single-agent work or disables sub-agents, discover and use sub-agents when the active findings can be separated safely.
2. Group active findings into at most three non-overlapping path or subsystem scopes. Delegate only independent groups.
3. Give every implementation agent its finding IDs, owned paths, relevant local context, constraints to preserve, and these rules: edit only owned paths; do not run tests, typechecks, linters, builds, commits, or checks; do not edit shared planning/output files; return control before expanding edit scope.
4. Allow parallel writers only when the host provides isolated workspaces or each agent has exclusive paths. Otherwise, use agents for focused investigation and have the coordinator apply the edits sequentially.
5. Integrate delegated changes before starting verification. Resolve conflicts and preserve all accepted finding fixes.
6. If sub-agents are unavailable or the findings are coupled, complete the same finding-local workflow sequentially. Mention an unavailable-tooling fallback only when it caused the sequential mode.

## Combined verification

Run verification only after all accepted fixes are integrated.

1. Read applicable repository instructions and identify existing targeted tests, typechecks, linters, or build commands for the combined changed areas.
2. Run the smallest relevant existing checks once for the whole batch. Do not run a full suite unless repository instructions require it or the user asks.
3. If a check fails because of this batch, make the focused correction, restore the complete batch, and rerun the affected check only after that correction is in place. Do not validate individual delegated patches in isolation.
4. If a check is unavailable, fails for an apparent pre-existing reason, or cannot cover a finding, report that limitation plainly.
5. Inspect the final diff only to confirm that it contains the intended fixes and no accidental out-of-scope edits; do not perform another code review.

## Output

Return short sections, bullets, and no code snippets unless needed to explain a blocker:

### Fix review findings

Fixed N of M supplied findings:

- **Fixed `F1` `path/to/file:42`** — concise repair summary.
- **Fixed `S1` `path/to/helper:14`** — concise simplification summary.
- **Skipped `F2` `path/to/file:87`** — concise direct reason.
- **Blocked `F3` `path/to/file:19`** — decision required and available options.

Verification:

- `command` — passed / failed / unavailable, with a concise consequence.

Changed files: `path/to/file`, `path/to/test`

Generated with hawk-fix-review-findings

Do not commit, push, post remote comments, or rerun the review automatically. Human review remains required before integration.
