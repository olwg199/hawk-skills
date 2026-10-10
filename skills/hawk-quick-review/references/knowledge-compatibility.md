# Mandatory knowledge and Codex/Claude compatibility review

Run this bounded, read-only pass on every invocation, even with no code diff.
It is an explicit exception to changed-lines-only review for applicable project
instructions, knowledge, and documentation. It is not a repository-wide inventory.
The coordinator owns it independently of code specialist selection. Mandatory
means the pass always runs, not that every project document is in scope.

Read the shared [instructions and migration specification](agent-instruction-layout.md)
on every pass. Knowledge Transfer uses the same packaged source. Support both
Codex and Claude as the Hawk project standard, even if one is used today.
`CODEX.md` is optional; its absence is never a finding or limitation.

## Select relevant evidence

Start from the eligible change set and the user's stated review target. Include
only:

- Changed documentation and included untracked knowledge files.
- Current docs/knowledge that describe behavior, contracts, commands, or records
  affected by the work, even when those documents were not edited.
- Startup instructions and scoped rules governing the reviewed paths, their
  required imports, and docs whose read conditions apply to this work.

Use changed paths, affected symbols/commands, and applicable instruction routes
for targeted discovery. Before opening another document, identify its connection
to the work or a required instruction dependency. Follow links only as needed to
verify that connection; a link in an index does not make its target relevant.
Do not enumerate/read all docs, traverse every instruction link, or load unrelated
knowledge archives. Stop once the applicable checks have enough evidence.

Read the working-with-agents compatibility section, installation guidance, and
handoff/ownership docs only when changed, explicitly targeted, or needed to
verify setup used by the reviewed work. A missing section unrelated to the work
is outside scope. With no eligible changes and no explicit documentation/setup
target, check only applicable startup instructions and required imports; an empty
diff does not authorize a documentation audit.

Include relevant untracked generated Markdown as evidence; skip logs, binaries,
secrets, and caches. Generated knowledge does not override project instructions.

## Evidence and checks

- Keep essential project-wide rules in startup-loaded `AGENTS.md`, shared by an
  actual Claude import. Look for demonstrated critical requirements stranded
  only in on-demand docs, lost during organization, or changed in scope. Do not
  demand that `AGENTS.md` be only an index, flag its substantive essential rules,
  or invent a universal policy checklist.
- Verify required import targets and relevant docs links: relative paths, case,
  and read conditions. Do not check unrelated links in the same instruction file.
  Preserve local overrides and host-specific conditions. `CODEX.md` is inspected
  only when present and is never created by review.
- Check applicable current docs/knowledge against changed behavior, contracts,
  command definitions, or placement. Require a demonstrated contradiction or a
  documented missing update; routine edits need not change every knowledge file.
- Discover affected legacy `.codex/hawk-build.md`, its design notes,
  `.codex/mobile-ui-builder.md`, and `.build/` history when no usable canonical
  counterpart exists. If active affected records still need migration, make it
  a blocking finding and name source/destination paths. Give an explicit action,
  for example `$hawk-knowledge-transfer Migrate the affected Hawk records to
  docs/generated using native copies, verify them, and repair structural links`.
  Do not invoke that skill or migrate during review.
- Apply the shared full-copy/knowledge-preservation rule to reviewed migrations.
  Distinguish the equality check before edits from the final structural diff.
  Inspect any copy evidence, Git history, retained source, or other available
  provenance before judging knowledge loss. Lack of a recorded tool transcript
  is not itself a finding; if evidence cannot establish a material preservation
  question, report that specific limitation instead of inventing data loss.
- Check required project skills/resources through the documented installation,
  and that handoffs/concurrent ownership do not depend exclusively on private
  sessions. Inspect only relevant project evidence; do not read global user
  settings, install tools, or require online platform research.

Keep the compatibility section grounded in actual project evidence. Do not
require vendor-doc citations or verification dates. Missing required startup
rules, an actual required import, or a required compatibility section within the
selected scope remain setup gaps; a missing optional file or unused directory
alone does not.

## Findings and readiness

Use the same realistic-trigger/confidence gate as code findings. A normal task
missing a known essential instruction, a documented command that no longer
exists, a broken required import/link, demonstrated lost knowledge, or affected
unmigrated active records is concrete evidence. Dates, wording preferences,
harmless duplication, and missing tests are not blockers. Historical old paths
and decisions remain provenance; inspect live routes and current knowledge.

Keep accepted defects as ordinary prioritized `F1` findings with precise repair
locations and migration actions where relevant. They count toward the total and
can be supplied for explicit repair. Attach inline comments only to real current
lines, including the nearest owner location for a missing artifact. This scoped
pass may keep pre-existing setup/knowledge issues only when they govern or
document the reviewed work. Each such finding must identify that connection;
unrelated existing documentation/setup defects remain excluded.

Always report Knowledge and Codex/Claude compatibility as `passed`, `blocked`,
or `not verified`, with evidence and finding IDs counted once. Known defects mean
`blocked`; a material unresolved evidence gap within the selected scope means
`not verified`. Both prevent readiness. Unrelated docs intentionally left unread
are not a limitation and cannot block readiness. Report the inspected paths and
their relevance; a complete applicable static pass with no defects can be `passed`;
do not imply runtime host execution. For an empty eligible change set, report
`Nothing to review.` for code plus this section/findings, without a commit message.
Review never repairs files: give exact actions for a user-requested migration,
Knowledge Transfer, or remediation. This is a readiness gate, not a Git hook.
