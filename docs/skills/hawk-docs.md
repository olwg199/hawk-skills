# hawk-docs

Writes and updates project docs (plans, decision logs, area guides, READMEs, rule docs, findings docs) so each fact
lives in one place and is correct the first time.

## When to use

- Whenever a project doc is written or changed, also in plain words ("update the plan").
- Not for skill working records under `docs/generated/`, code comments, record migration
  ([hawk-knowledge-transfer](hawk-knowledge-transfer.md)) or rule reviews
  ([hawk-project-rules-review](hawk-project-rules-review.md)).

## How it works

- Finds the doc that owns the topic, checks every promised behavior against the code, logs decisions in the decision
  log, the one source of truth.
- Closes docs after work: finished work items become `done`, answered questions move to the decision log.
- A fresh agent reads a new doc and answers its reader's questions; gaps are fixed.
- Clean-up of existing docs only when you ask, with a plan per area and nothing changed until you pick Apply.
- `doc-tool.py` checks IDs and links, finds repeated text, moves docs while fixing links, and lists open questions
  (`open`) and doc lines touched by changed files (`touched`).

The rules it follows are in [doc-writing rules](../doc-writing.md), shared with the other writing skills.

## Invoke

- Claude Code: `/hawk-docs Update the plan with the review decision`
- Codex: `$hawk-docs Write the doc for order synchronization`

The full workflow is in [SKILL.md](../../skills/hawk-docs/SKILL.md).
