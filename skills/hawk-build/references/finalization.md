# Git and finalization

Read when preparing a user-authorized related commit or finalizing a full build. For lightweight builds, only the commit guidance applies; completion follows SKILL.md.

For each user-authorized related commit, prepare a concise subject and include this trailer:

```text
Build: <build-id>
```

Never create commits automatically. Read related history from Git using this trailer; do not copy hashes, subjects, branch state, or commit status into task artifacts. Preserve a legacy **Related commits** section as historical evidence, but do not append to it. Review establishes readiness for commit.

Complete **Final outcome** with delivered behavior, dated verification results, and a compact plan-versus-actual summary, referencing existing evidence rather than repeating it. Complete any knowledge-maintenance item and date **Project memory** status with check evidence. Read [project knowledge and history](knowledge.md) to upsert the compact history entry; do not backfill unrelated builds.

Finalize statuses only in their owner. Mark an owning record `complete` with date and evidence only when all authorized work and final documentation are complete. When a project plan owns remaining work, retain the record as `history` and route its index entry to the plan; do not label the plan's unfinished work complete. Keep **Current checkpoint** limited to the owner link, settled contract links, and last dated verification summary. Any retained **Next steps** heading links to the owner instead of listing actions.

Keep a manual readiness prerequisite as an unresolved item in the owner only when the coordinator cannot safely complete it within authorized scope; state when it is needed and the observable completion result. Commit, push, deployment, release, and post-deployment actions are not build completion prerequisites. Suggest a separate review when useful; the build does not depend on another skill to finish.

At completion, report outcome, verification, owning record or plan path, and unresolved items by reference. Give the fixed resume prompt from SKILL.md when work remains. Do not create a handoff file or duplicate the owner's progress in the history record.
