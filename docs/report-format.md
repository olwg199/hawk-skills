# Report and question format

Shared by every Hawk skill that reports results or asks the user something. It applies the same way in Claude Code and
Codex. A skill's own output template sets which sections and lines appear; this file sets how they are written. Where a
skill template shows a one-line finding, write the full finding block below instead.

## Language

Write the whole report and every question in the language the user writes in, including headings and option labels.
Keep code identifiers, paths, commands, IDs (`F1`, `P1`, `S1`) and fixed status phrases that other tools or users
search for (`Ready to commit from review perspective.`, `Generated with <skill>`) as they are. A suggested commit
message follows the project's commit language, English when the project has no rule.

## Findings

Every finding, problem or error gets a block, never a single line or a bare count ("4 problems found"):

- **F1 · P1 · `path/to/file:42` — short title in plain words**
  - **What breaks:** the concrete situation that triggers it and what the user or system would see.
  - **Why it matters:** the impact, how sure you are and how it was checked.
  - **Fix:** where and how to repair it and what that costs (size, risk, what else changes).

Use the same block for findings relayed from a sub-agent or another session, after reading its full report. Keep
optional items (simplification leads, improvement opportunities, test ideas) short: one line saying what to change and
what it gives.

## After finished work: report, no question

End finished work with a short structured report the user can scan quickly, not too much and not too little:

- **Done:** each change in plain words: what, why, how (and which files).
- **Checked:** what was run or verified and the result; what was not run.
- **Open:** what is not done or not verified, and what waits for the user's approval (commit, push, deploy) as a plain
  statement ("staged, not committed").
- **Suggestions** (optional): possible next steps or options, each with one line on what it gives, written as
  statements.

Do not end finished work with a question, a "shall I fix everything?" prompt or question buttons; the user reads the
report and says what to do next. A host's end-of-turn summary box gets the recap only.

## Questions

Ask only when the user opens a discussion (asks to discuss, or ends the message with a question) or when work is
truly blocked on a decision only the user can make (the skill's clarification and approval gates). Before asking,
write the choice in this shape, as short blocks rather than running prose:

- **Question:** one or two lines on what is being decided and why it matters now.
- **Options:** one block per option:
  - **<Option name>:** what it is (one sentence for any unfamiliar tool, model or term)
    - Good: what it gives.
    - Bad: what it costs or risks.
    - Cost: time, size, files or behaviour that change.

  When parts of different options can be combined, offer the parts as separate options and allow several to be picked
  where the tool supports it (otherwise list them and ask which to take); say so when options exclude each other.
- **Recommendation:** the option you recommend and why, in one line.

Then ask through the host's structured question tool when it has one (Claude Code: `AskUserQuestion`; Codex: its
structured user-input tool), with 2–4 options, the recommended one first, and room for a free-form answer. Without such a
tool, ask the same question once in plain chat after the blocks.

Work starts only from the user's command or from a picked option that names the action and lists what will run
("Apply: …", or a gate option such as "Replace: …", in the user's language). Until then, any other answer or picked
option is a decision: nothing is changed because of it, and only read-only research runs. Once the user has asked for
the work (a direct request or the skill's invocation), an answer to a blocking question lets it go on within that
request; a gate the skill requires still needs its own confirmation, and an answer that goes beyond the request needs an
"Apply: …" option. Offer an "Apply: …" option only once the plan it starts is written out.
