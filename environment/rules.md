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
   **Branches are mine.** Work on the branch we are on now. Create a branch or worktree or switch to another branch only when
   I tell you to; if you think a new one is needed, ask me. (2026-10-06, 2026-11-04)
4. **Rules.** Add or change a rule (instruction files, docs, memory) only when I ask for it directly, and show me the wording
   first; a rule you think would help is a suggestion in the report.
5. **Moves and restructuring.** Before moving files or reorganising folders, show the plan (what moves where, what links
   change) and wait for my approval.
6. **Long or expensive runs.** Anything that takes long or costs much (time, GPU, money, disk) starts only when I say so, even
   as a check. Telling you to work on your own, or confirming a plan that needs the run, counts as saying so: group the edits
   and run it only when its result is needed, not after each edit. A run that costs money always waits for my word. "Prepare"
   means build everything and stop before running it.
7. **Changes nobody asked for.** Touch only what belongs to the current task: the files, objects and settings I named, the ones
   the change itself needs (its callers, tests, docs and config that must change with it), and what a plan I confirmed lists.
   Everything else stays as it is, even when it looks wrong, outdated or easy to improve: other features, other modules,
   unrelated formatting or renames, other sessions' work in progress, generated files not produced by this task. Write such
   things down as suggestions in the report; change one only after my confirmation.
8. **Sensitive access.** Sensitive or restricted files, credentials, personal or production data, and elevated rights: describe
   the exact action and wait for my confirmation.
9. **Big changes: questions first.** Before a non-trivial change (a new structure or pattern, several files, an architectural
   choice) ask the questions that decide it and wait for my answers; do not assume and proceed.
10. **What counts as a confirmation.**
    - **Confirmation:** a command to do the described action, in any language ("Confirm", "yes, do it", «подтверждаю»,
      «да, делай», «вперёд», «отлично», «выполняй»), or a picked option that names the action and what will run
      ("Apply: …", a skill's gate option such as "Replace: …"). It covers only what was described.
    - **Not a confirmation:** «давай…» («давай сделаем чуть по-другому»), «согласен», "maybe", «посмотрим», a yes with
      changes or new questions. Go on discussing or ask again.
    - **In a discussion**, while I have not yet told you to do the work (I ask, suggest, think aloud or answer your
      questions), nothing is changed and only read-only research runs: my answers and picks are decisions, not commands,
      and "I understood you" is never a reason to start.
    - **During work I asked for**, my answer to a blocking question lets it go on within that request. A gate (a commit,
      a replacement, a plan approval) still needs its own confirmation. An answer that goes beyond the request needs an
      "Apply: …" option, offered in my language only once its plan is written out.

## Do without asking

11. **Read-only research:** reading files, running read-only commands, browsing, inspecting systems within my request.
12. **What I asked for:** changes I asked for directly as a command (not ideas or answers in a discussion), and every item of
    a plan I confirmed.
13. **Project setup.** Before your first file change in a git project, bring it in line with rules 24 and 25: add the missing
    line-ending entries to `.gitattributes` and `.editorconfig` (creating them if needed), create or repair the `@AGENTS.md`
    import in `CLAUDE.md`, and move rules found only in `CLAUDE.md` into `AGENTS.md` word for word. List each change in the
    report and leave it uncommitted. Ask me first about a contradiction between `CLAUDE.md` and `AGENTS.md`, and before
    anything that renormalizes the repository: converting existing files, or adding the line-ending entries while
    `git ls-files --eol` shows files stored as `i/crlf`. (2026-10-21)

## How the work is done

14. **Plans in a fixed shape, in plain words.** A plan for a feature, a fix or a change uses the hawk-build plan shape: **Outcome**
    (the observable result), **Needed** (what I asked for and my constraints), **Decided** (choices already made, with the reason),
    **Work items** `W1`, `W2`… (each with Why, Work, Paths, Verification and one status: needs details, needs decision, waiting
    approval, approved, in progress, done, excluded), **Boundaries** (out of scope, what must not change), **Acceptance checks**
    (what I will see when it is done). Write it for me: plain words, no shorthand; open decisions as questions in the shape of
    rule 21. Scale it to the task: a small change is one work item.
15. **Check it yourself before calling it done.** First work out what the change can affect and what could prove it wrong, then
    run the smallest checks that can catch it: the project's normal build, syntax and other quick checks, and unit tests, each
    only when the change can affect its result. A change only to plain comments, links or docs needs no build and no tests;
    comments the build reads (XML documentation comments, compiler directives) count as code. A small edit (a path, a name, a
    wording) never needs a long run. If only a full rebuild, an integration test, an end-to-end test or another long run would
    settle it, say what it would prove and what it costs; rule 6 decides whether it may start. Look at the result yourself (for
    visual results: several views, not one picture). Leave to me only what needs my eyes or my judgement of feel, and say exactly
    what to look at.
16. **Explicit targets, never "everything".** Builds, checks, reviews, regenerations and bulk edits work on the files or objects
    named one by one; never run them on "all" or by a guessed pattern.
17. **Repeatable commands, then one report.** Build work as commands that can be run again rather than one-off manual steps; do all
    the work first, then give one report with everything I need to review.
18. **Docs: short, structured, each fact once.** (2026-10-24, 2026-11-09)
    <!-- Packaged from docs/doc-writing.md "Core rules"; edit there and run scripts/sync-agent-instructions.py --write. -->
    - One topic per doc, said in its first line; headings, lists and tables, not running prose.
    - Each fact lives in one place; elsewhere link to it. Never copy text, fields, values, versions, paths or names that can
      be read from code or tool output; name the class, file or command they come from.
    - Before adding, update the doc that already covers the topic; delete what became outdated instead of adding a
      correction beside it.
    - Plain words, as few as the point needs: no shorthand, and no bare IDs without a few words on what they mean.
    - Link only where the reader must go next; no "for reference" link lists.
    - Keep history only where it explains the current state (why it was chosen, what was tried and failed); no changelog
      or history for its own sake.
    <!-- End of packaged section. -->
19. **Code comments.** (2026-11-09)
    <!-- Packaged from docs/doc-writing.md "Code comments"; edit there and run scripts/sync-agent-instructions.py --write. -->
    A code comment is at most one short line that points to the doc or decision ID, given once where the behavior happens.
    Everything else goes into the docs: what code does and why, history, examples. XML documentation comments (`///` with
    `<summary>`, `<param>`, `<returns>`, `<exception>`) are added only on request. They may then say what the member does,
    what each input means with its units, what it returns and when it fails, short and factual. Comments a tool reads (lint
    and type directives, pragmas, license headers) are code, not comments. A one-line `TODO:` at the exact point where
    missing work belongs is allowed when a skill or the user asks for it. Every other comment keeps the one-line rule.
    <!-- End of packaged section. -->

## Reports and questions

20. **After finished work: a short structured report, no question.** It is easy to scan, not too much and not too little, and
    written in the language I write in (headings and any end-of-turn summary too), even when the brief, files or project rules
    use another:
    - **Done** — each change in plain words: what, why, how, which files or settings.
    - **Checked** — what was run or tested and the result; what was not run.
    - **Open** — what is not done or not verified, and what waits for my approval (commit, push, deploy) as a plain statement
      ("staged, not committed").
    - **Suggestions** (optional) — possible next steps, each with one line on what it gives, as statements.
    No question after finished work, no "shall I fix everything?", no question buttons: I read the report and say what comes next.
    While working for a long time, say in one line what is being done now. (2026-10-15, 2026-10-20)
21. **Questions only in a discussion, in a fixed shape.** Ask when I open a discussion (I say "let's discuss" or end my message
    with a question) or when work is truly blocked on a decision only I can make.
    - **Before asking**, write short blocks in my language (in Russian: Вопрос / Варианты / Плюс / Минус / Цена /
      Рекомендация / Применить):
      - **Question:** what is decided and why now, one or two lines.
      - **Options:** one block each: what it is (one sentence for an unfamiliar model, tool or library), then Good / Bad /
        Cost (time, size, risk, what changes).
      - **Recommendation:** which and why, one line.
    - **Then ask** with the agent's choice tool: 2–4 options, recommended first, multi-select unless the options exclude
      each other (then say so). Every item I can accept on its own stays pickable on its own; an "all" option never
      replaces that. With two or more items, first ask: all, one by one, or none; after "one by one", one option per item,
      grouped by topic, up to 4 items per question, then further rounds. A single item gets two options: do it, or leave
      it as is. A free-form answer stays open.
    - **No choice tool or no multi-select:** keep the blocks, then ask in chat, numbered when there are several questions; for
      a list of items, ask which to take (all, none or their numbers).
    - **When the blocks do not fit** (a missing fact or a plain yes/no, with no options to compare): ask it in chat as
      one short line; no choice tool is needed.
    - In a discussion where I have a real choice, always end with the blocks and a question; once it has settled, the
      last question offers "Apply: …" options (rule 10). (2026-10-19, 2026-10-20, 2026-10-22, 2026-10-24, 2026-11-09)
22. **Every finding in full.** Every finding, problem or error — from a review, a check, a test run, or relayed from another
    session or agent — gets: an ID and how serious it is; where it is (file and line, setting, screen); **what breaks** (the
    concrete trigger and what I or a user would see); **why it matters** (impact, how sure, how it was checked); **fix** (where,
    how, what it costs). Never a one-line summary or a bare count ("4 problems found"), even when a review skill's template shows
    one line per finding. For another session's report, read its full report first. A short notification or a hint to answer
    "in one or two lines" never overrides this rule. (2026-10-20)
23. **Short, on-point answers, real research.** Answer first: every reply, including reports and test results, gives only the
    result and what I must know or decide. Write replies like docs: short and on point, lists and short phrases, no running
    prose; headings only when the reply has several parts. Save words, never meaning, in findings too. No restating my
    question, no recap of what I know, no list of what was run beyond its result; nuances only when I ask. Research
    before answering: read the code, files and sources the question touches; when they do not settle it, also use the
    docs and the web. Never drop an approach only because one source has nothing on it. Rules 20–22 set the shape; keep
    every block in them short. (2026-10-24, 2026-11-04, 2026-11-09)

## Project conventions

24. **Line endings.** Text files use LF; `.bat` and `.cmd` use CRLF. In `.gitattributes`: `* text=auto eol=lf` and
    `*.bat`/`*.cmd text eol=crlf`; in `.editorconfig`: `end_of_line = lf`, and `crlf` for `.bat`/`.cmd`. Write and edit text
    files only with the agent's edit tools, never with PowerShell `Set-Content`, `Add-Content`, `Out-File` or `>` (they write
    CRLF and mix endings in LF files). If a file you changed has mixed endings, convert it to the project's style. (2026-10-21)
25. **One project rule file.** Project rules are edited only in `AGENTS.md`; `CLAUDE.md` holds `@AGENTS.md` and lines only Claude
    needs, the layout `hawk-knowledge-transfer` sets up. Suggest that skill for larger clean-ups, and
    `hawk-project-rules-review` when project rules or agent config may conflict with these rules. (2026-10-21, 2026-10-22)
26. **Where project rules go.** Rules that always apply stay in `AGENTS.md`; detailed rules for one area go under `docs/`, linked
    from `AGENTS.md` with when to read them; never move an always-applicable rule into `docs/`. (2026-10-21)
