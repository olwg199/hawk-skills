<!-- Packaged from docs/doc-writing.md in hawk-skills. Edit that source and run scripts/sync-agent-instructions.py --write. -->

# Writing project docs

How Hawk skills write and update project documentation so it is correct the first time: plans, decision logs and
registers, area guides, READMEs, rule docs, findings docs and skill working records. It applies the same way in Claude
Code and Codex. A skill's own record format sets which sections a record has and where it lives; this file sets how
they are written. Code comments are covered only by [the comment rule](#code-comments).

## Before writing

1. **Find the owner.** Start from the project's docs index (such as `docs/README.md`) and update the one doc that
   already covers the topic. Create a new doc only when none does, and say in its first line what it covers. A skill's
   working record under `docs/generated/<skill>/` keeps that skill's format.
2. **Research before writing.** Check every behavior a doc promises against the code it relies on before writing it,
   including the empty, missing, refused and error cases, and write those cases into the doc. The failure this
   prevents: a plan said "Review opens with the checked rolls", but the endpoint reads an empty list as "all rolls".
3. **Cite only what was opened.** Write a register ID, decision ID or doc link only after opening that row or section
   and seeing it says what the sentence claims. Anchors must point to real headings.

## While writing

- **Point, don't copy.** Never list fields, values, versions, paths or names that live in code or tool output; name
  the class, file or command instead. Each fact lives in one place ([where facts live](#where-facts-live)); elsewhere
  link to it.
- **Log decisions in the same turn.** A decision the user makes in chat goes into the project's decision log in the
  same turn it is written into a plan, following [decision logs](#decision-logs). The plan's Decided entry then cites
  the row ID with the question it answers, never the answer, so a changed decision leaves no stale copy.
- **One status owner.** Work status lives only where the project keeps it (for example a plan's Status column, or a
  skill's record when no project plan owns it). Never repeat it elsewhere, never write Git state (commits, branches,
  "not committed") into docs, and never create handoff, prompt or next-chat files.

## Where facts live

Each kind of fact has one owner, so a change is made in one place:

| Fact | Lives in | Elsewhere |
|---|---|---|
| How an area behaves now | the area doc | link to the area doc |
| Decisions | the area's decision log | only the area doc, active plans, skill records and [code comments](#code-comments) cite the ID; other docs link to the area doc |
| Work status | the active plan, or a skill's record when no plan owns it | never repeated |
| Fields, values, versions, paths, commands | the code or tool output | named, never copied |
| Rules for agents | `AGENTS.md`, or a rules doc linked from it | link |

## Writing rules

- One topic per doc, said in its first line. Headings, lists and tables, not running prose.
- Plain words: no shorthand, and no bare IDs without a few words on what they mean.
- As few words as the point needs. No changelog or history for its own sake; keep history only where it explains the
  current state (why it was chosen, what was tried and failed).
- Link only where the reader must go next; no "for reference" link lists.
- Delete what became outdated instead of adding a correction beside it.
- Plans describe what is built and why: pages, fields, rules, data written, open questions. No step-by-step
  instructions or commands telling an agent how to build it; a work item's Verification may name the check that
  proves it.

## Grouping docs

- One topic per doc. An area that outgrows one file becomes a folder `docs/<area>/` with a `README.md` that says what
  the area is and links to its files.
- When a change makes a doc cross about 200 lines or gives it a second topic, propose a split: what moves where and
  which links change. Split only after the user approves it. Never split or reorganize docs the task does not change.
- Skill working records under `docs/generated/<skill>/` belong to their skill: only that skill edits them, and they are
  never split, cleaned up or rewritten to follow these rules. When a doc they link to moves, only those link targets
  are repaired.

## Decision logs

- A project's own convention (one log, an ADR folder, a Decisions section) wins. Without one, decisions go into one
  log per area, `docs/decisions/<area>.md`, listed in the docs index.
- Use the log's own columns; a new log uses ID, question, decision, why, confirmed (who, date), history. IDs follow the
  log's scheme; a new log uses an area prefix and a number (`REVIEW-1`). New rows go at the end.
- An ID names the question, not the answer. A new question gets a new row and ID.
- **Changed decision:** edit the row in place and keep its ID, so no citation changes. Write one line in history only
  when it stops someone from repeating a mistake ("all rolls was tried: reviewers saw rolls they did not choose");
  otherwise leave it empty. Git keeps the rest.
- **Obsolete decision** (the question no longer exists): delete the row, then search the whole repository for its ID
  (for example `git grep`), docs and code comments alike, and in the same turn remove or rewrite every citation. Skill
  records under `docs/generated/` keep the old ID as history.

## Done plans

When every work item of a project plan is done or excluded and its acceptance checks pass, move any lasting fact it
holds that is not yet in the area doc or decision log there, then delete the plan in the same turn and report it under
Done. Git keeps the plan; nothing stale stays behind. A plan that a skill record or a skill's index links to is closed
by that skill, which updates its own links first; any other writer only reports that the plan is done.

## Plan shape

A plan for a feature, fix or change has these parts, scaled to the task (a small change is one work item):

- **Outcome:** the observable result.
- **Needed:** what the user asked for and their constraints.
- **Decided:** choices already made, each with the reason or the decision-log row that holds it.
- **Work items** `W1`, `W2`…: each with **Why**, **Work**, **Paths**, **Verification** and one status: `needs details`,
  `needs decision`, `waiting approval`, `approved`, `in progress`, `done`, `excluded`.
- **Boundaries:** what is out of scope and what must not change.
- **Acceptance checks:** what the user will see when it is done.

A skill may add fields of its own to this shape; it never drops one.

## Open decisions

An open decision in a doc is a question, then **Options** (each: what it is, Good, Bad, Cost) and a
**Recommendation** in one line. Once decided, it moves to Decided (or the decision log) and the question is deleted.

## Code comments

A code comment holds only what code and docs cannot show: one short line pointing to the doc or decision ID, given
once where the behavior happens. Longer explanations go into the docs.

## Rule files

- Change rule files (`AGENTS.md`, `CLAUDE.md`, instruction docs, agent memory) only when the user asks for it directly,
  and show the wording first.
- Project rules are edited only in `AGENTS.md`; `CLAUDE.md` holds `@AGENTS.md` and only lines Claude alone needs. Rules
  that always apply stay in `AGENTS.md`; detailed rules for one area go under `docs/`, linked from `AGENTS.md` with when
  to read them.

## Files

- Keep each file's line endings: check with `git ls-files --eol` and convert back if a tool changed them. Edit with the
  agent's edit tools, never PowerShell `Set-Content`, `Add-Content`, `Out-File` or `>`.
- Touch only the docs the task needs; anything else that looks wrong goes into Suggestions.

## Self-check before reporting

Re-read every changed section, not only the edited lines, and check each claim against the code and the register. Fix
what is wrong in the sections being changed; list problems found elsewhere as suggestions.
