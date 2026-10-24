# Rules comparison

Shared by the Hawk skills that compare a narrower set of rules (one computer's local rules, one project's rules and agent
config) with the broader rules that already apply (the user's global rules). It applies the same way in Claude Code and
Codex. The skill names what is compared with what; this file sets how each item is judged, reported and changed.

## Categories

Read the broader rules in full first, then put every rule or setting of the narrower set into exactly one category:

- **Duplicate:** says the same as a broader rule in other words, or a broader rule already includes it, so it adds
  nothing. Examples: "never add a co-author line to commits" when the global rules forbid co-author lines; "ask before
  pushing" when they require approval for every commit, push and history change.
- **Contradiction:** following both is impossible, or the narrower one undoes the broader one without saying so. Example:
  "commit after each finished step" against a global rule that commits wait for approval; `attribution` set in a project
  settings file against a global rule that commits never mention an AI.
- **Deliberate override:** a contradiction the narrower set marks as intended, with a line such as `Overrides global rule:
  <rule> because <reason>`. Keep it; report it only when the reason is missing or no longer true.
- **Belongs elsewhere:** not about this computer or project. Examples: a general working rule in a computer's local file
  (belongs in the global rules), a machine path in a project file (belongs in that computer's local rules), an
  always-applicable project rule hidden in `docs/` (belongs in `AGENTS.md`).
- **Stale:** points to something that is gone or has changed: a missing file, doc, command, script, skill or setting, or a
  value that no longer matches the code.
- **Keep:** specific to this computer or project, consistent with the broader rules, and in the file where it belongs.
  A correct rule in the wrong file is Belongs elsewhere.

When unsure between Duplicate and Keep, prefer Keep and say why in the report. A narrower rule that is stricter than the
broader one (it asks for more, never less) is Keep, not a contradiction.

## Report

Every item that is not Keep is a finding written as the [report and question format](report-format.md) describes: ID
and severity, where it is (file and line, or setting), what breaks or what is repeated (quote the narrower line and name
the broader rule), why it matters, and the fix. Contradictions are P1 or higher when they can lead to an action the user
did not approve (a commit, a push, a run, an AI mention).

After the findings, write the plan of changes, one line per change, then ask in the all / one by one / none layout of the
[report and question format](report-format.md), with one "Apply: …" option per change. A Contradiction gets its own
single-choice question. Change only what the user picks or commands, and nothing before that.

## Changes

- **Duplicate:** remove from the narrower set after Apply. When other people or machines read the narrower set (project
  rules in git), a duplicate of the user's own global rule stays unless the user confirms the project is theirs alone;
  otherwise it is Keep, noted in the report.
- **Contradiction:** never resolve it yourself. Ask which side wins: remove the narrower rule, mark it as a deliberate
  override with the reason, or change the broader rule (the last is only a suggestion; the skill never edits the broader
  rules).
- **Belongs elsewhere:** move only what lives inside the files the skill may edit, word for word; anything that would go
  into the broader rules is a suggestion.
- **Stale:** fix the reference when the right target is certain; otherwise ask.
- Move or keep rule text word for word; never reword a rule while moving it.
- After the changes, compare the result with the state before them: each removed item must still be covered by the
  broader rules, and nothing else may have changed.
