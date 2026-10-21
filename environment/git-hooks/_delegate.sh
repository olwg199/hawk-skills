#!/bin/sh
# Runs the repository's own hook of the same name (.git/hooks/<name>), so Git LFS and other repo hooks keep working.
# Git runs hooks from the work tree root, so a plain .git folder is checked first without starting git again.
# reference-transaction, post-index-change, push-to-checkout and fsmonitor-watchman are not wrapped: the first two run
# many times per commit and made every commit seconds slower, and a push-to-checkout hook replaces git's own
# updateInstead behaviour.
name="$1"; shift
if [ -d .git ]; then common=.git; else common="$(git rev-parse --git-common-dir 2>/dev/null)"; fi
own="$common/hooks/$name"
if [ -x "$own" ]; then exec "$own" "$@"; fi
exit 0
