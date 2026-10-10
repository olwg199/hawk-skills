# Shared instructions and knowledge layout

Knowledge Transfer and Quick Review use this one maintained specification. It is
packaged inside each skill so neither depends on the other being installed.

## Startup instructions

- Keep concise, essential project-wide instructions directly in `AGENTS.md`:
  authorization and deployment boundaries, safety requirements, critical
  conventions, and other rules that must apply to every task. Preserve each
  rule's meaning, scope, and host conditions. Do not replace these rules with
  instructions to open another file later.
- `CLAUDE.md` imports the applicable `AGENTS.md` using an actual `@AGENTS.md`
  line outside code formatting. A wrapper under `.claude/` targeting root uses
  `@../AGENTS.md`. This shares essential rules without a second editable copy.
  Preserve any necessary host-specific conditions during consolidation.
- Keep detailed area-specific procedures and explanations under `docs/`.
  Link them from `AGENTS.md` with explicit read conditions, such as “For data
  changes, read docs/data-contracts.md.” Links are on-demand guidance, not
  substitutes for essential startup instructions.
- Preserve directory scope and inspect applicable overrides before changing
  instructions. Give delegates the essential rules and relevant scoped docs.
  Only the coordinator edits shared instructions, docs, and working records.
- `CODEX.md` is optional. Do not create or require it; its absence never blocks
  review. If present, retain applicable rules while making it an ordinary
  Markdown pointer to `AGENTS.md`. Do not use Claude imports as Codex instructions.

Use both Codex and Claude as the project standard, even if only one is used
currently. Keep the working-with-agents page's Knowledge and Codex/Claude
compatibility section current from project evidence. Do not require a preview
approval step for clearly requested documentation work: make the changes and
report their paths, outcomes, and unresolved gaps for Git review. Ask only when
an unresolved conflict materially affects meaning or scope.

## Record migration

New working records belong under `docs/generated/<skill>/`. Existing records
are migrated only when the user explicitly requests migration; a normal build,
review, or documentation refresh does not authorize it. Continue discovering
legacy records until they are migrated, and keep their existing formats.

Copy the complete file unchanged using native file-copy commands and verify the
copy. Preserve the recorded knowledge—its facts, decisions, rationale,
constraints, status, and history—with the same meaning and level of detail.
Then update only references, paths, or routing required by the new structure.
Changes to the knowledge itself must be handled separately from migration.
Never recreate, summarize, regenerate, or retype a record to relocate it.

For each requested record:

1. Resolve source and destination paths, preserving IDs and filenames unless
   a rename is needed. Check existing destinations before copying. If they
   differ, resolve the conflict rather than silently overwriting either record.
2. Create missing destination folders and use `Copy-Item` in PowerShell,
   `cp` on POSIX, or an available native equivalent. Examples for a single file:

   ```powershell
   Copy-Item -LiteralPath $source -Destination $destination
   (Get-FileHash -LiteralPath $source).Hash -eq (Get-FileHash -LiteralPath $destination).Hash
   ```

   ```sh
   cp -p "$source" "$destination"
   cmp -s "$source" "$destination"
   ```

3. Require copy verification to pass before editing the destination. A directory
   migration uses native recursive copying and verifies every migrated file;
   do not copy unrelated tool configuration just because it shares a folder.
4. Make targeted structural edits and repair live links. Retain historical path
   mentions as provenance when they do not control current routing. Report the
   copied paths, equality-check result, and exact structural edits. Review the
   diff for changes to recorded knowledge, not only whether links now resolve.
5. If source removal is part of the requested migration, remove only the exact
   migrated originals after copy verification and structural checks. Otherwise
   retain them. Never delete an entire tool directory or unrelated files.

Hawk destinations:

- `.codex/hawk-build.md` → `docs/generated/hawk-build/project.md`
- `.codex/hawk-build/design/` → `docs/generated/hawk-build/design/`
- `.build/` records/index → `docs/generated/hawk-build/builds/`, retaining filenames
- `.codex/mobile-ui-builder.md` → `docs/generated/hawk-mobile-ui-builder/project.md`

## Review gate

Scope this gate to the eligible changes and the user's explicit review target.
Check changed docs, current docs/knowledge describing affected behavior or
contracts, and instructions governing the reviewed paths with their required
imports and applicable docs read conditions. Follow only links needed for these
checks; do not audit all docs, instruction links, or records. The
working-with-agents compatibility section and installation/handoff guidance are
review evidence only when changed, targeted, or needed for the reviewed work.
With no eligible changes or explicit docs/setup target, limit the pass to
applicable startup instructions and required imports.

Check essential-rule presence in startup instructions, actual Claude imports,
relevant docs routes, scope preservation, current knowledge, and affected record
locations. Do not flag essential policies for making `AGENTS.md` more than a
routing index. Do not impose a line-count gate or invent new project rules.

Flag an incomplete migration when affected active knowledge or history still
uses a legacy location and has no usable canonical counterpart. Give the exact
source/destination paths and an explicit Knowledge Transfer migration command.
A missing destination folder alone, an old path in historical text, or a retained
original after a completed copy is not a migration defect. Review reports and
blocks on the gap; it never migrates files itself.

If a migration is in the reviewed changes, assess full-copy evidence and targeted
edits separately. Flag demonstrated knowledge loss, changed decisions/status,
regenerated records, broken links, or unauthorized removal. Do not treat rewritten
prose as successful migration merely because the destination file exists.

Pre-existing documentation/setup defects qualify only when they govern or
document the reviewed work; identify that connection in each finding. Unrelated
docs left unread are outside scope, not an incomplete check or readiness blocker.

Accepted defects are ordinary blocking findings. Always report Knowledge and
Codex/Claude compatibility as `passed`, `blocked`, or `not verified` with concrete
project evidence and the inspected paths' relevance. Essential rules stranded in
on-demand docs, broken required imports, lost knowledge, and relevant incomplete
migration prevent readiness.
The review remains read-only; this is a review gate, not a Git hook.
