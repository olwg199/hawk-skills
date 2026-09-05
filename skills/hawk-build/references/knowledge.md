# Project knowledge and build history

Read when planning or completing knowledge maintenance, or checking whether a note is reliable. Keep current design separate from historical outcomes. The coordinator alone maintains these records.

## Current project knowledge

Use `.codex/hawk-build.md` as the project index. Keep entries short: topic, purpose, keywords or source paths, and a link to a focused note or existing maintained documentation. Aim for at most 500 words; search relevant entries rather than reading a large index in full. Do not duplicate existing documentation.

Store useful design notes under `.codex/hawk-build/design/`. UI, Data, and Architecture are possible categories, not required files. Split growing categories into cohesive subjects such as forms, navigation, or synchronization. Create notes incrementally from verified task work; do not scan the repository to populate them.

A note should explain relationships that would otherwise require reading multiple source files:

- Current ownership, behavior, boundaries, and relevant data or event flow.
- Accepted architectural decisions, brief rationale, and contracts to preserve.
- Representative source paths or symbols and focused verification commands.
- The date and build ID that last verified or changed the documented facts.

Keep notes concise and task-selectable. Link cross-topic contracts instead of copying them. Store detailed decision history in the task build record; describe the current accepted design in the note. Do not include code dumps, logs, or proposed decisions as established behavior.

Notes guide discovery but do not replace inspecting code to be edited. A verification date is provenance, not proof of freshness. Check relevant source and contracts; if they contradict a note, current evidence wins. Correct affected stale facts during the task's knowledge maintenance. Do not revalidate unrelated notes.

For an existing `.codex/hawk-build.md` map, read relevant sections as before. Extract a focused note only when the current task benefits, leaving a short index entry and preserving unrelated knowledge. No bulk migration is required.

## Knowledge work item

During planning, add a work item when the task changes durable architecture, contracts, or reusable patterns, or requires correcting affected stale knowledge. Name the affected note/index paths and the facts to establish. Its verification checks the note against implemented source and relevant verification results. Complete it after those facts are verified; a proposed plan is not sufficient evidence. A routine change following documented patterns needs no knowledge item.

## Build-history index

At finalization, upsert one compact entry per completed build in `.build/index.md`. Include build ID/date, title, a short delivered-outcome summary and material decision rationale, relevant keywords/symbols, affected paths, and a relative link to the full build record. Lightweight entries follow the compact format in SKILL.md and are themselves the record: they include verification and need no separate file link. Preserve incomplete lightweight entries as incomplete; do not treat them as delivered outcomes. Update an existing entry when a resumed build is finalized again; do not append duplicates. Mark known superseded decisions with a link to the replacing build when relevant, without auditing all history.

Example:

```markdown
### b042 — Signup keyboard spacing — 2026-09-04
- Outcome: Adopted insets mode so keyboard appearance preserves flexible form spacing.
- Keywords: UI, forms, signup, keyboard, KeyboardAwareScrollView
- Paths: src/features/signup/
- Record: [b042](b042-signup-keyboard.md)
```

Search entries by concepts, symbols, and paths, allowing synonyms; keywords are retrieval aids, not an exhaustive relevance filter. Read the matching entry before opening the full build. If no entry matches, use targeted current-source research or a bounded historical search when the unresolved question requires it. Never load the whole build archive to compensate for missing entries, and do not backfill old builds by default.

The history index is not the source of truth for current architecture. Load it only to resolve a prior-decision or regression question, not as a routine task-start requirement.
