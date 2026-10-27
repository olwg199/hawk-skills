---
name: hawk-docs
description: >-
  Write and update project documentation so it is correct the first time:
  plans, decision logs and registers, area guides, READMEs, rule docs and
  findings docs. Finds the doc that owns the topic, checks every promised
  behavior and cited ID against the code and register, logs decisions in the
  same turn, keeps docs grouped by topic, and self-checks before reporting. Use
  whenever you write or change a project doc, including plain requests such as
  "update the plan", "write the doc for X" or "clean up the docs", even when the
  skill is not named. Also supports `$hawk-docs`
  and `/hawk-docs`. Do not use for skill working records under
  docs/generated/ (a build record or build plan is hawk-build's), code comments
  beyond the docs side of the comment rule, migrating knowledge records
  (hawk-knowledge-transfer), or reviewing project rules
  (hawk-project-rules-review).
---

# Hawk Docs

Write or update project documentation so a full review passes it on the first try. Every rule this skill enforces is
in [doc-writing rules](references/doc-writing.md); read it before writing anything. Reports and questions follow
[report and question format](references/report-format.md).

Invocation text: $ARGUMENTS

If that line is empty or shows a literal placeholder (for example in Codex), use any text after the skill name in the
user's message. Together with recent chat context, it names the doc or topic and what should change.

## Scope

- **Covers:** project plans, decision logs, area guides, READMEs, rule docs and findings docs.
- **Does not cover:** skill working records under `docs/generated/<skill>/`, which only their own skill edits (build
  records, build plans and the build index belong to `hawk-build`; only their link targets are repaired when a doc they
  point to moves); code comments (except the docs side of the comment rule); migrating knowledge records (an explicit
  `hawk-knowledge-transfer` request); reviewing project rules (`hawk-project-rules-review`).
- **Rule files** (`AGENTS.md`, `CLAUDE.md`, instruction docs, agent memory) change only when the user asks for it
  directly, and the wording is shown first ([rule files](references/doc-writing.md#rule-files)).

## Clarify ambiguous requests

Resolve material ambiguity before acting on a user message.

- Inspect the current message, relevant recent chat context, and available project evidence before asking.
- If one reasonable interpretation is low-risk and does not materially change scope, behavior, files, output, or external state, state the assumption and continue.
- If two or more plausible interpretations would lead to materially different work, pause and ask a targeted clarification. Name the likely meanings and their practical difference; prefer “Did you mean A or B?” over “Can you clarify?”
- Write the choice in the question shape of [report and question format](references/report-format.md), then use the host's questions or structured user-input tool when available. Offer 2–3 choices, mutually exclusive unless parts of them can be combined (then offer the parts and allow several to be picked when the host supports it), put the recommended interpretation first when evidence supports one, and allow a free-form answer when the host supports it. Otherwise ask the same concise question in normal chat.
- Ask only the smallest set of blocking questions. Do not repeat questions answered by the request or context, and do not treat ambiguity as permission to broaden scope or make a consequential change.

## Workflow

Follow [doc-writing rules](references/doc-writing.md) in this order:

1. Find the doc that owns the topic ([before writing](references/doc-writing.md#before-writing)); propose a split when
   the change makes it too big ([grouping docs](references/doc-writing.md#grouping-docs)).
2. Check every promised behavior against the code, including the empty, missing, refused and error cases.
3. Open each decision, row or section before citing it.
4. Put each fact where [where facts live](references/doc-writing.md#where-facts-live) says, and link to it elsewhere.
5. Log decisions in the same turn; edit a changed decision in place and delete an obsolete one
   ([decision logs](references/doc-writing.md#decision-logs)).
6. Delete a project plan once all its work is done and its acceptance checks pass
   ([done plans](references/doc-writing.md#done-plans)). If a record or index under `docs/generated/` links to it
   (`git grep` the plan's file name there), leave it to that skill and report the plan as done.
7. Self-check every changed section, and run `doc-tool.py check` on the changed docs when they cite decisions or link
   to other docs.
8. Report as [report and question format](references/report-format.md) describes.

## Clean-up mode

Only when the user asks to clean up or organize docs (for a named area, or the whole docs folder when they say so):

1. Read the docs index, the decision logs and the docs in scope; run `doc-tool.py dupes` and `doc-tool.py check` on
   them.
2. Propose a plan in the [plan shape](references/doc-writing.md#plan-shape), one work item per area so each can be
   accepted on its own: repeated text replaced by links, big or mixed docs split into `docs/<area>/` folders, one large
   log split into per-area logs, obsolete decisions and done plans deleted.
3. Change nothing until the user picks "Apply". Then use `move`, `extract` and `drop` with `--apply`, finish the text
   by hand, and run `check` on the same docs.

Outside this mode, existing docs and logs are never reorganized.

## Doc tool

`scripts/doc-tool.py` in this skill's folder (Python 3, standard library only). Run it from the project root with
`python3` (`python` on Windows), calling it by this skill folder's path. Pass docs and folders explicitly. In folders,
`check`, `move` and `extract` include skill records under `generated/` but only check or repair their links; `dupes`
and `drop` skip them, so records keep old IDs as history. A command only sees the docs it is given, so `move`, `extract`, `drop` and `check` always get every place
that can link into `docs/`: the `docs` folder plus the root Markdown files (`AGENTS.md`, `CLAUDE.md`, `README.md` and any
other `.md` at the root). Commands that change files only preview unless `--apply` is given, and keep each file's line
endings.

| Command | Does |
|---|---|
| `check [--register LOGS --pattern ID] DOCS` | Lists cited decision IDs with no row (a row's ID is the first ID on it) and links or anchors that do not resolve, including wrong letter case |
| `dupes DOCS` | Lists sentences and list items repeated across docs, with `path:line` |
| `move SRC DST DOCS` | Moves a doc and rewrites every link to it in DOCS |
| `extract SRC ANCHOR DST DOCS` | Moves the section under a heading into DST and repoints links to its anchors |
| `drop ID --register LOGS --pattern ID DOCS` | Deletes the decision row, removes plain `(ID)` citations, lists the rest to rewrite |

`--pattern` lists the project's own prefixes, for example `"(?:REVIEW|BILLING)-\d+"`; a generic pattern such as
`[A-Z]+-\d+` also catches words like UTF-8. Exit code 0 means done or nothing found, 1 problems or repeats found, 2 a
usage or read error. The tool cannot judge whether a cited ID is the right one: step 3 stays a manual check.
