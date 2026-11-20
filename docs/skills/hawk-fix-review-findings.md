# hawk-fix-review-findings

Fixes the findings (`F1`) and simplification leads (`S1`) of a review you supply.

## When to use

- When you ask to fix or address supplied review output. Comments can skip or prioritize items by ID
  ("Skip F2; prioritize F1 and S1").
- Not for new reviews, general bug fixes or test suggestions.

## How it works

- Starts from each reported file and line and reads only the code it needs; never reruns the review.
- Independent findings can go to up to three parallel subagents.
- Fixes the demonstrated outcome in the clearest safe way, preferring the project's existing error handling.
- Runs the smallest relevant checks once for the batch; never changes tests.
- Closes the project docs the fixes settled and reports them in a `Docs:` line. Never commits or pushes.

## Invoke

- Claude Code: `/hawk-fix-review-findings`
- Codex: `$hawk-fix-review-findings Fix the findings from the preceding review`

The full workflow is in [SKILL.md](../../skills/hawk-fix-review-findings/SKILL.md).
