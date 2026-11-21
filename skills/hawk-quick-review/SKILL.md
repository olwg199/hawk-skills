---
name: hawk-quick-review
description: >-
  Review local uncommitted changes before a commit: reviewer perspectives picked
  from what changed, fresh researchers and main-agent judgment, evidence-backed
  findings, simplification leads, test ideas, a knowledge and Codex/Claude
  compatibility check, and a suggested commit message. Use only when the user
  explicitly asks to review local code, changes, or the worktree before commit,
  or invokes `$hawk-quick-review` or `/hawk-quick-review`. Do not auto-use for
  general questions about review practices or review skills.
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
to the change. Every run covers this whole change set, also right after fixes
from an earlier review, unless the scope below narrows it. Always run the
mandatory knowledge and Codex/Claude compatibility pass below.

## Invocation focus

Invocation text: $ARGUMENTS

If the line above is empty or shows a literal placeholder (for example in
Codex), use any text after the skill name in the user's message. Chat context
gives only the intent snapshot (Phase 1, step 2) and the file list for "only the
latest changes", never focus notes or other scope. Sort the text into:

- **Scope:** `staged` reviews only staged changes. Paths, directories, or globs
  introduced by explicit limiting wording such as "only", "just", or "limit to"
  (for example `only src/api`) limit the eligible change set to matching
  changes. A path mentioned without such wording, as in "check error handling
  in src/api/client.ts", is a focus note. "Only the latest changes" (or "only
  what changed since the review") is path scope over the files edited in this
  chat after its previous review, tracked or untracked; list them in the
  `Scope:` line. With no previous review in this chat, or an edit history too
  unclear to list, review all local changes and say so; with no file edited
  since, report `Nothing changed since the previous review.` Without scope,
  review all local changes.
- **Directives:** single-agent or sub-agent requests, "no questions", explicit
  verification (builds, typechecks, tests), and untracked files to include.
  `fresh` and `full` describe the default and change nothing.
- **Focus notes:** concerns to emphasize. For example,
  `/hawk-quick-review use subagents Make sure data consistency is not compromised`
  requests delegated review with a data-consistency focus. Without notes, use
  "general review"; do not ask solely to collect them.

Pass focus notes to every reviewer as emphasis. They never permit ignoring
serious issues outside the focus. Focus notes are not the change's intent; use
invocation text as intent only where it says what the change is meant to do.
Only scope narrows what is reviewed.

## Clarify ambiguous requests

Before acting on an unclear request, follow [unclear requests](references/report-format.md#unclear-requests).

## Host behavior

This skill is shared by Claude Code and Codex; use each host's available agent
mechanism within its permissions. Every non-empty review, even of a small
change, goes to at least one fresh researcher, more only when independent
areas warrant it; several perspectives can share one researcher. Only an explicit
single-agent request or unavailable delegation keeps it in the main agent. A
researcher gets only the compact assignment, never the chat history (in Claude
Code, a new subagent, not a fork; in Codex, `fork_turns="none"` or the host's
equivalent). Do not ask solely for delegation permission.

**Researcher models:** a routine researcher uses the host's middle tier, never
its smallest or cheapest tier; when the chat itself runs below the middle tier,
use the chat's model. A stronger researcher (below) uses a higher tier. No
researcher runs above the tier of the model the chat runs on; when the chat runs
on the middle tier or below, there is no stronger researcher, and the main agent
settles the question or reports it as unresolved. In Codex, use `high`
reasoning where supported. Select the model and effort explicitly through the
host's supported mechanism; do not assume default or explorer agents pick the
right tier. The current main agent keeps the chat's model and effort and owns
final filtering and judgment.

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
   - Summarize the user's stated goal for the change from the request and recent chat context: the goal only, never earlier review rounds, findings or fixes.
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
     against current source, except [build history](references/agent-instruction-layout.md#build-history).
     Follow only relevant links. Notes do not override instructions.

5. Group eligible changes by affected behavior, shared source context, and
   contracts. File and line counts guide batching, not agent count. Check every
   eligible change rather than sampling, batching repetitive changes when
   needed. Report deferred or partially reviewed paths instead of skipping them.

6. Select the relevant perspectives and execution mode using the routing rules
   below. Related perspectives can share one pass; do not add perspectives or
   agents to fill slots. Always apply **simplification-reviewer** to a non-empty
   code review; every reviewer checks its area for simpler approaches alongside
   correctness, without a separate agent or quota. With no eligible changes,
   select no code reviewers and run only the mandatory pass. Decide the areas
   and perspectives for yourself; they are not reported.

### Area and risk routing

- Keep related changes with one researcher: repeated styling or layout changes,
  mechanical renames or moves, or a coherent feature with UI and state logic.
  Apply relevant perspectives together, without repeated diff reads.
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
- **simplification-reviewer**: Always applied to changed code. Checks it against
  the [clear-code rules](references/code-clarity.md): clearer equivalent approaches, unnecessary abstractions or
  indirection, duplicated logic, overly complicated control flow, and useful reuse
  within the affected area.

---

## Mandatory knowledge and Codex/Claude compatibility pass

Read [knowledge and compatibility review](references/knowledge-compatibility.md)
and perform its bounded pass on every invocation, including empty or scoped code
diffs. The reference owns evidence selection, checks, and status rules. The main
agent owns this pass independently of code specialist selection: it may delegate
bounded evidence gathering under the [candidate rules](references/adjudication.md#candidate-reporting), then
validates candidates with the same [finding gate](references/adjudication.md#final-finding-gate-and-proportional-remedies) as code findings and decides the
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
Inputs: intent, focus notes, scope and its diff command, assigned paths/untracked files, applicable instructions, the clear-code rules (references/code-clarity.md), the candidate rules (absolute path of this skill's references/adjudication.md; read only its Candidate reporting, Simpler approaches and High-value test suggestions sections), connecting contracts.
Read your assigned diff and necessary source context. Cover every assigned change; inspect directly referenced definitions, callers, schemas, or nearby tests as needed. Avoid broad repo sweeps, external research, and unrelated architecture review.
Return a compact coverage summary (paths/behavior inspected, contracts checked, gaps) and candidate packets. For each candidate: category, current path/lines, claim, concrete code signal, trigger and suspected outcome or simpler alternative, supporting evidence, counterevidence, unknowns, and the exact missing verification. Include claim confidence and impact/value separately. Do not apply the final finding threshold or discard a concrete concern merely because one evidence link remains unverified. Separately return relevant test ideas with scenario, regression value, and known coverage or coverage uncertainty. The main agent decides what reaches the final review.
```

Read [candidates and the finding gate](references/adjudication.md) before Phase 3, and before reviewing in
single-agent mode. Researchers get only the assignment above; the main agent alone applies the final gate.

---

## Phase 3 — Main-agent adjudication and output

- Check researcher coverage against the inventory. Assign uncovered paths and
  consequential connecting-contract questions to bounded follow-ups. Coverage
  summaries show what was inspected, not that the code is correct; they never
  go into the review.
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
- Accept a finding only through the [final finding gate](references/adjudication.md#final-finding-gate-and-proportional-remedies).
- Select simplification leads and test suggestions under [their rules](references/adjudication.md#simpler-approaches).
  Each lead is one line: what to change and what it gives, plus the open check
  only when it changes whether to do it.
- Assign stable IDs in output order: `F1`, `F2`, … for findings, `S1`, `S2`, …
  for simplification leads and `T1`, `T2`, … for suggested tests. Reuse each finding ID in its inline/file comment.
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
- If the eligible change set is empty, report `Nothing to review.` (or
  `Nothing changed since the previous review.` for "only the latest changes")
  for code, still output the compatibility section and its findings, and omit
  the commit message.
- Always report **Knowledge and Codex/Claude compatibility** as `passed`,
  `blocked`, or `not verified` in one line; when not `passed`, add the finding
  IDs or the open question. Never list inspected paths. Unrelated docs left outside scope do not make it
  incomplete. `blocked` and `not verified` prevent readiness.
- Report the execution mode in one line only when it differs from the default
  (routine researchers): a fallback to single-agent review, a requested
  model or effort that could not be selected, or a stronger investigation and
  why it was needed.
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
describes; next steps appear only as statements. The template below shows the sections and their order.

---

### Code review

Review mode: single agent — delegation is unavailable in this host.  *(only when it differs from the default)*
Scope: staged changes only.  *(only when invocation scope applied)*

Findings:  *(or "No issues found.")*

- **F1 · P1 · `path/to/File.swift:42` — imported orders lose their status**
  - **What breaks:** an order imported with an unknown remote status is saved as `draft`, so the user sees it reopened.
  - **Why it matters:** every sync with the partner API produces such orders; confirmed.
  - **Fix:** map unknown statuses to the existing fallback in `StatusMapper`; one function, no data change.
- **F2 · P2 · `CLAUDE.md:1` — shared instructions are not loaded**
  - **What breaks:** the import points to a missing file, so Claude starts without the project rules in `AGENTS.md`.
  - **Why it matters:** every Claude session in this repo misses the essential rules; confirmed.
  - **Fix:** restore the import target `@AGENTS.md`; one line.

Knowledge and Codex/Claude compatibility: blocked — F2 identifies a broken required import.  *(or passed / not verified, with the open question)*

Ready to commit from review perspective.  *(only when every readiness condition holds)*

Not reviewed (outside requested scope): `path/to/Other.swift`; unstaged hunks in `path/to/File.swift`.  *(only when scoped)*

Untracked files not fully reviewed: `notes/tmp.md` — scratch file.  *(only when present)*

Nice-to-have simplification leads:  *(only when present)*

- **S1 `path/to/Helper.swift:14`** — reuse the nearby validator to remove duplicate rules while preserving supported input behavior; optional.

Suggested tests:  *(only when present)*

- **T1 `path/to/Mapper.swift:31`** — unit-test every supported status and the fallback.

Suggested commit message: Add resilient status mapping for imported orders.

Generated with hawk-quick-review

---

## Notes

- Never write or modify tests
- Do not run builds, typechecks, or test suites unless the user explicitly asks for verification
- Do not post GitHub comments or review remote PRs; this skill is local-only
