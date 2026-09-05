# Git and finalization

Read when preparing a user-authorized commit or finalizing a build.

For each user-authorized related commit, prepare a concise subject and include this trailer:

```text
Build: <build-id>
```

Never create commits automatically. At finalization, discover related commits from this trailer and list their short SHA and subject under **Related commits**. If a commit predates the trailer convention, list it only when the user identifies it as related.

Complete **Final outcome** with delivered behavior, verification results, and a compact plan-versus-actual summary. Finalize the **Project memory** status and update `.codex/hawk-build.md` when verified outcomes changed durable project knowledge. Keep **Work items** at their final statuses and summarize material changes by linking to **Plan deviations**. Mark the record `complete` only when all authorized work the coordinator can perform and the final record are complete. Keep any outstanding local code-readiness actions only in **Current checkpoint** under **Next steps**.

At finalization, use **Next steps** only for actions required before the final review of the current local changes. Include a manual readiness prerequisite only when the coordinator cannot safely complete it within the authorized scope; state when it is needed and the observable completion result. Never list commit, push, deployment, release, or post-deployment actions. When `hawk-quick-review` is available, append exactly one review action as the final **Next steps** item. The review owns the code-readiness conclusion.

