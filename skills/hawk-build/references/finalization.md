# Git and finalization

Read when preparing a user-authorized related commit or finalizing a full build. For lightweight builds, only the commit guidance applies; completion follows SKILL.md.

For each user-authorized related commit, prepare a concise subject and include this trailer:

```text
Build: <build-id>
```

Never create commits automatically. Read related history from Git using this trailer; do not copy hashes, subjects, branch state, or commit status into task artifacts. Preserve a legacy **Related commits** section as historical evidence, but do not append to it. Review establishes readiness for commit.

Complete any knowledge-maintenance item first, then read [project knowledge and history](knowledge.md) to upsert the compact history entry; do not backfill unrelated builds.

Finalize statuses only in their owner. Mark an owning record `complete` with date and evidence only when all authorized work and final documentation are complete. When a project plan owns remaining work, retain the record as `history` and route its index entry to the plan; do not label the plan's unfinished work complete. Until the record is closed below, keep **Current checkpoint** limited to the owner link, settled contract links, and last dated verification summary, and any retained **Next steps** heading links to the owner instead of listing actions.

Close the record with its findings only when it becomes `complete`, or when the project plan that took it over completes. First move every **Decided** entry and rationale not yet in a decision log or design note there, as [project knowledge and history](knowledge.md) describes. Then keep the frontmatter and replace every other section with **Findings**:

- **Outcome:** the delivered behavior in one or two lines.
- **Lessons:** the confirmed cause for a fix, approaches tried and rejected with the reason, and surprises a later build needs.
- **Contracts to keep:** links to the design notes and decision-log rows that hold them, not copies.
- **Last verification:** date, check, and result.

Delete **Current checkpoint**, **Plan**, **Research**, **Project memory**, **Plan deviations**, **Delegated work**, **Implementation iterations**, and any legacy **Final outcome** or **Next steps** in the same turn; Git keeps them. Keep a legacy **Related commits** section. When a project plan took the record over, close it in this order once the plan completes: write the delivered outcome into the index entry and point it at the record, close the record, then delete the plan ([done plans](doc-writing.md#done-plans)). Never trim a record that was already `complete`, or a `history` record whose plan is still open.

Keep a manual readiness prerequisite as an unresolved item in the owner only when the coordinator cannot safely complete it within authorized scope; state when it is needed and the observable completion result. Commit, push, deployment, release, and post-deployment actions are not build completion prerequisites. Suggest a separate review when useful; the build does not depend on another skill to finish.

At completion, report outcome, verification, owning record or plan path, and unresolved items by reference. Give the fixed resume prompt from SKILL.md when work remains. Do not create a handoff file or duplicate the owner's progress in the history record.
