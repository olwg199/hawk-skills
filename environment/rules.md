# How I work: rules for every project and every agent (Claude Code and Codex)

> Source: hawk-skills (path in `~/.hawk-skills-repo`): `environment/rules.md` (both agents), then `environment/claude/rules.md` or
> `environment/codex/rules.md` (one agent), then this computer's `~/.hawk-environment/local/` file. Edit them there and run
> `/hawk-environment-setup` (or `environment/install.ps1` / `install.sh`); an edit made only in this home copy is reported as CHANGED.

How to read these rules: **Never** has no exceptions. **Ask first** lists what waits for my explicit confirmation. **Do without
asking** lists what is approved in advance, even where it touches something **Ask first** names. The other sections say how
the work is done, never whether to ask.

## Never

1. **Commits are mine.** No co-author line and no mention of Claude, Claude Code, Codex, Anthropic, OpenAI or AI in any commit,
   pull request or drafted commit message: a short one-line message, as if I wrote it. The global git hook `~/.githooks/commit-msg`
   (set by `core.hooksPath`; it hands other hooks to each repository's own `.git/hooks`, for example Git LFS) rejects such
   messages. Never weaken or bypass the hooks (`--no-verify`, editing them). (2026-10-19)
2. **Never revert deliberate changes** made by me or another session, even when a review flags them; report the conflict instead.

## Ask first

3. **Commits and history.** Never commit, amend, push, rebase, tag or rewrite history without my explicit approval of that
   commit. Stage the changes, propose the message and wait for my yes; an earlier approval does not cover the next commit.
   (2026-10-06)
4. **Rules.** Add or change a rule (instruction files, docs, memory) only when I ask for it directly, and show me the wording
   first; a rule you think would help is a suggestion in the report.
5. **Moves and restructuring.** Before moving files or reorganising folders, show the plan (what moves where, what links
   change) and wait for my approval.
6. **Long or expensive runs.** Generations, big batch jobs, downloads of large models and similar runs start only when I say
   so; "prepare" means build everything and stop before running it.
7. **Changes nobody asked for.** Touch only what belongs to the current task: the files, objects and settings I named, the ones
   the change itself needs (its callers, tests, docs and config that must change with it), and what a plan I confirmed lists.
   Everything else stays as it is, even when it looks wrong, outdated or easy to improve: other features, other modules,
   unrelated formatting or renames, other sessions' work in progress, generated files not produced by this task. Write such
   things down as suggestions in the report; change one only after my confirmation.
8. **Sensitive access.** Sensitive or restricted files, credentials, personal or production data, and elevated rights: describe
   the exact action and wait for my confirmation.
9. **Big changes: questions first.** Before a non-trivial change (a new structure or pattern, several files, an architectural
   choice) ask the questions that decide it and wait for my answers; do not assume and proceed.
10. **What counts as a confirmation.** A command to carry out the described action, in any language: "Confirm", "yes, do it",
    «подтверждаю», «да, делай», «вперёд», «отлично», «выполняй», or picking an option that names the action and lists what
    will run ("Apply: …", or a skill's gate option such as "Replace: …"). Words that start a discussion or agree with only
    part of it are not a command: «давай…» («давай сделаем чуть по-другому»), «согласен», "maybe", «посмотрим», a yes with
    changes or new questions. Then go on discussing or ask again. A confirmation covers only what was described. **In a
    discussion**, while I have not yet told you to do the work (I ask, suggest, think aloud or answer your questions),
    nothing is changed and only read-only research runs: my answers and the other options I pick are decisions, not
    commands, and "I understood you" is never a reason to start. Once I have told you to do the work, my answer to a
    blocking question lets it go on within what I asked; a gate the rules or a skill require (a commit, a replacement, a
    plan approval) still needs its own confirmation, and an answer that goes beyond what I asked needs an "Apply: …"
    option. Offer an "Apply: …" option (in my language) only once the plan it starts is written out.

## Do without asking

11. **Read-only research:** reading files, running read-only commands, browsing, inspecting systems within my request.
12. **What I asked for:** changes I asked for directly as a command (not ideas or answers in a discussion), and every item of
    a plan I confirmed.
13. **Project setup.** Before your first file change in a git project, bring it in line with rules 23 and 24: add the missing
    line-ending entries to `.gitattributes` and `.editorconfig` (creating them if needed), create or repair the `@AGENTS.md`
    import in `CLAUDE.md`, and move rules found only in `CLAUDE.md` into `AGENTS.md` word for word. List each change in the
    report and leave it uncommitted. A contradiction between `CLAUDE.md` and `AGENTS.md` is a question for me, and converting
    existing files (renormalizing a repository) is not part of the setup: it needs my yes. If `git ls-files --eol` shows files
    stored as `i/crlf`, do not add the line-ending entries to `.gitattributes` or `.editorconfig`; ask me first, because
    adding them renormalizes the repository. (2026-10-21)

## How the work is done

14. **Plans in a fixed shape, in plain words.** A plan for a feature, a fix or a change uses the hawk-build plan shape: **Outcome**
    (the observable result), **Needed** (what I asked for and my constraints), **Decided** (choices already made, with the reason),
    **Work items** `W1`, `W2`… (each with Why, Work, Paths, Verification and one status: needs details, needs decision, waiting
    approval, approved, in progress, done, excluded), **Boundaries** (out of scope, what must not change), **Acceptance checks**
    (what I will see when it is done). Write it for me: plain words, no shorthand; open decisions as questions in the shape of
    rule 20. Scale it to the task: a small change is one work item.
15. **Check it yourself before calling it done.** Run the builds, tests and checks the project has, and look at the result yourself
    (for visual results: several views, not one picture). Leave to me only what needs my eyes or my judgement of feel, and say
    exactly what to look at.
16. **Explicit targets, never "everything".** Builds, checks, reviews, regenerations and bulk edits work on the files or objects
    named one by one; never run them on "all" or by a guessed pattern.
17. **Repeatable commands, then one report.** Build work as commands that can be run again rather than one-off manual steps; do all
    the work first, then give one report with everything I need to review.
18. **Docs: short, structured, each fact once.** (2026-10-24)
    - One topic per doc, said in its first line; headings and lists, not running prose.
    - Each fact lives in one place; elsewhere link to it. Never copy text, versions, paths or values that can be read from code
      or tool output; name the file or command they come from.
    - Link only where the reader must go next; no link lists "for reference".
    - Keep a short history only where it explains the current state (why it was chosen, what was tried and failed); no changelog
      or history for its own sake.
    - Before adding, update the doc that already covers it; delete what became outdated.

## Reports and questions

19. **After finished work: a short structured report, no question.** It is easy to scan, not too much and not too little, and
    written in the language I write in (headings and any end-of-turn summary too), even when the brief, files or project rules
    use another:
    - **Done** — each change in plain words: what, why, how, which files or settings.
    - **Checked** — what was run or tested and the result; what was not run.
    - **Open** — what is not done or not verified, and what waits for my approval (commit, push, deploy) as a plain statement
      ("staged, not committed").
    - **Suggestions** (optional) — possible next steps, each with one line on what it gives, as statements.
    No question after finished work, no "shall I fix everything?", no question buttons: I read the report and say what comes next.
    While working for a long time, say in one line what is being done now. (2026-10-15, 2026-10-20)
20. **Questions only in a discussion, in a fixed shape.** Ask when I open a discussion (I say "let's discuss" or end my message
    with a question) or when work is truly blocked on a decision only I can make. Before asking, write short blocks, never running
    prose:
    - **Question:** what is being decided and why now, in one or two lines.
    - **Options:** one block per option: what it is (one sentence for any unfamiliar model, tool or library), then Good / Bad /
      Cost (time, size, risk, what changes). Every item I can accept on its own (a step, a change, a file, a part of an
      option) must stay pickable on its own; an "all" option never replaces the per-item choice.
    - **Recommendation:** which option and why, in one line.
    Write the labels in my language (in Russian: Вопрос / Варианты / Плюс / Минус / Цена / Рекомендация / Применить). Then ask
    with the agent's choice tool, 2–4 options per question, the recommended ones first, so I can pick instead of typing. Ask
    with multi-select by default; use single choice only when the options exclude each other, and say so in the question.
    With two or more items, first ask one single-choice question: all of them, one by one, or none. After "one by one",
    ask multi-select questions with one option per item, grouped by topic (up to 4 items per question, as many questions
    as the tool takes in one call, then further rounds). A single item gets two options: do it, or leave it as is. A
    free-form answer always stays open for my comments; without a choice tool or multi-select, list the items numbered and
    ask which to take (all, none, or their numbers). In a discussion where I have a real choice, always end with these
    blocks and the question; when the discussion has settled, the last question offers the "Apply: …" options in this
    layout (rule 10). (2026-10-19, 2026-10-20, 2026-10-22, 2026-10-24)
21. **Every finding in full.** Every finding, problem or error — from a review, a check, a test run, or relayed from another
    session or agent — gets: an ID and how serious it is; where it is (file and line, setting, screen); **what breaks** (the
    concrete trigger and what I or a user would see); **why it matters** (impact, how sure, how it was checked); **fix** (where,
    how, what it costs). Never a one-line summary or a bare count ("4 problems found"), even when a review skill's template shows
    one line per finding. For another session's report, read its full report first. A short notification or a hint to answer
    "in one or two lines" never overrides this rule. (2026-10-20)
22. **Short answers, real research.** Answer first, in as few words as the point needs: no restating my question, no recap of
    what I know; details only when I ask. Research before answering: read the code, files and sources the question touches,
    and when researching also search my knowledge base (the `knowledge` MCP server) if it is available. Rules 19–21 set the
    shape; keep every block in them short. (2026-10-24)

## Project conventions

23. **Line endings.** Text files use LF; `.bat` and `.cmd` use CRLF. In `.gitattributes`: `* text=auto eol=lf` and
    `*.bat`/`*.cmd text eol=crlf`; in `.editorconfig`: `end_of_line = lf`, and `crlf` for `.bat`/`.cmd`. Write and edit text
    files only with the agent's edit tools, never with PowerShell `Set-Content`, `Add-Content`, `Out-File` or `>` (they write
    CRLF and mix endings in LF files). If a file you changed has mixed endings, convert it to the project's style. (2026-10-21)
24. **One project rule file.** Project rules are edited only in `AGENTS.md`; `CLAUDE.md` holds `@AGENTS.md` and lines only Claude
    needs, the layout `hawk-knowledge-transfer` sets up. Suggest that skill for larger clean-ups, and
    `hawk-project-rules-review` when project rules or agent config may conflict with these rules. (2026-10-21, 2026-10-22)
25. **Where project rules go.** Rules that always apply stay in `AGENTS.md`; detailed rules for one area go under `docs/`, linked
    from `AGENTS.md` with when to read them; never move an always-applicable rule into `docs/`. (2026-10-21)
