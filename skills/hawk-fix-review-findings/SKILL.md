---
name: hawk-fix-review-findings
description: >-
  Fix explicitly supplied local code-review findings and nice-to-have
  simplification leads. Use only when the user asks to address, fix, or
  remediate supplied review output, or invokes $hawk-fix-review-findings. Do not
  auto-use for general bug fixes, feature work, test suggestions, or a new code
  review.
---

# Hawk Fix Review Findings

Treat the supplied review report as the scope of work. Repair its findings; do not turn this into a second general review.

## Clarify ambiguous requests

Before acting on an unclear request, follow [unclear requests](references/report-format.md#unclear-requests).

## Input

Invocation text: $ARGUMENTS

If that line is empty or shows a literal placeholder (for example in Codex), use any text after the skill name in the user's message. It may contain the review report, finding IDs to prioritize or skip, or other instructions for the steps below.

1. Before editing, read applicable root and directory-local `AGENTS.md`,
   `AGENTS.override.md`, `CLAUDE.md`, and referenced docs instructions. Read
   `CODEX.md` only if present; its absence is not a valid repair item. Use the review
   findings supplied in the request, recent conversation, or pasted report. If none are available, ask the user to provide them; do not run a new review unless explicitly asked.
2. Include reported findings and **Nice-to-have simplification leads** by default. Test suggestions are advisory and outside this skill's scope.
3. Treat user comments as instructions to prioritize, skip, or clarify listed items. Do not treat them as unrelated new work.
4. Preserve `F1`, `F2`, … finding IDs and `S1`, `S2`, … simplification IDs when present. For legacy text without IDs, assign them in report order and show the mapping before acting on user comments.
5. Track each item in your working notes for this run (no file): its ID, source location, requested outcome, and status: `active`, `fixed`, `skipped`, `blocked`, or `verification failed`. The report shows each item with its status; `fixed` and `skipped` are resolved, the others are not.

## Scope and decisions

Work one active review item at a time:

- Start at its reported file and line. Read only the changed code, directly related definitions, callers, tests, or contracts needed to understand and repair it.
- Expand investigation only when the local evidence requires it. Do not read or re-review the full diff, perform broad repository sweeps, or reopen general review questions.
- Do not repeat the full review, but inspect enough local context to confirm the reported trigger and outcome and choose a proportionate repair. Skip a finding when direct context makes it stale, duplicate, invalid, already resolved, dependent on an imaginary edge case, or already handled with the required observable outcome; state why.
- Before editing, identify any active review item that needs a breaking API or data-contract change, migration, permission change, or unresolved product-behavior choice. If one exists, present the affected item and concrete options in the question shape of [report and question format](references/report-format.md), then wait for direction before editing any files. Keep the batch atomic.
- Fix the demonstrated outcome with the clearest safe root-cause patch, not necessarily the reviewer's suggested mechanism or the fewest files or lines. Do not add unrelated refactors, cleanups, or behavior changes.
- Shape every repair by the [clear-code rules](references/code-clarity.md): methods, splitting, error handling and comments. When several real failures require the same outcome, repair them at the project's existing error boundary.
- Supplied knowledge or Codex/Claude compatibility findings are repair items.
  Fix their documented inconsistency, links, or imports within supplied scope;
  preserve essential rules directly in `AGENTS.md`, shared through `CLAUDE.md`'s
  actual import, and detailed area guidance in linked docs. Do not demote critical
  rules or migrate records as a routine repair; report an incomplete migration
  with an explicit action unless the user requested that migration. `CODEX.md` remains optional;
  do not create it to fix a finding that merely reports its absence. The coordinator owns shared
  docs and instructions, and delegates their applicable rules with each assignment.
- Preserve established logging, cleanup, state restoration, and user-facing error behavior.
- Split a large file only along the responsibilities the finding exposes; no unrelated large-file cleanup.
- Never create, generate, modify, rewrite, or delete tests or test-owned artifacts in this skill. A review's test suggestion is not a repair item; test implementation is separate work.
- If an existing test fails, diagnose whether the production behavior is wrong and fix an in-scope production regression when supported. Otherwise leave the test unchanged and report the test, the failure in one line, and that the test was left unchanged.

## Delegation

This skill is shared by Claude Code and Codex; do not assume a host-specific agent API or model name.

1. Unless the user requests single-agent work or disables sub-agents, discover and use sub-agents when the active review items can be separated safely.
2. Group active review items into at most three non-overlapping path or subsystem scopes. Delegate only independent groups.
3. Give every implementation agent its review-item IDs, owned paths, relevant local context, constraints to preserve, and these rules: edit only owned paths; do not run tests, typechecks, linters, builds, commits, or checks; never mutate tests or test-owned artifacts; do not edit shared planning/output files; return control before expanding edit scope.
4. Allow parallel writers only when each agent has exclusive paths. Otherwise, use agents for focused investigation and have the coordinator apply the edits sequentially.
5. Integrate delegated changes before starting verification. Resolve conflicts and preserve all accepted finding fixes.
6. If sub-agents are unavailable or the review items are coupled, complete the same item-local workflow sequentially. Mention an unavailable-tooling fallback only when it caused the sequential mode.

## Combined verification

Run verification only after all accepted fixes are integrated.

1. Read applicable repository instructions and identify existing targeted tests, typechecks, linters, or build commands for the combined changed areas.
2. Run the smallest relevant existing checks once for the whole batch. Do not run a full suite unless repository instructions require it or the user asks.
3. If a check fails because of this batch, diagnose and correct in-scope production code first, then rerun the affected check. Never mutate a test artifact. Do not validate individual delegated patches in isolation.
4. If a failing test remains, report the command, the test, the failure in one line, and that the test was left unchanged. Do not create a follow-up decision protocol inside this skill.
5. If a check is unavailable, fails for an apparent pre-existing reason, or cannot cover a finding, report that limitation plainly.
6. Inspect the final diff only to confirm that it contains the intended fixes and no accidental out-of-scope edits; do not perform another code review.

## Close the docs

After verification, the coordinator closes the project docs the fixes settled, as
[after work](references/doc-writing.md#after-work) says: finished work items, answered open questions and facts
the fixes made wrong. Delegated agents never edit docs.

## Output

Return short sections, bullets, and no code snippets unless needed to explain a blocker. Write the report as [report and question format](references/report-format.md)
describes; a fixed item adds the real cause in a few words only when it differed from the finding, and remaining
options appear as statements under the blocked item:

### Fix review findings

- **Fixed `F1` `path/to/file:42`** — unknown status saved as `draft` → mapped to the fallback.
- **Fixed `S1` `path/to/helper:14`** — duplicate rules → the shared validator.
- **Skipped `F2` `path/to/file:87`** — stale, duplicate or already handled.
- **Blocked `F3` `path/to/file:19` — short title**
  - **Decision needed:** what must be decided, one line.
  - **Options:** one line each, what it gives and what it costs.

Verification:

- `command` — passed / failed / unavailable, one line each by the check rule in [report and question format](references/report-format.md). For a remaining failing test, name the test, the failure in one line, and `test unchanged`.

Docs: `path/to/doc.md` — `W2` done, the export question moved to the decision log.  *(or `nothing to update`)*

Generated with hawk-fix-review-findings

Do not commit, push, post remote comments, or rerun the review automatically. Human review remains required before integration.
