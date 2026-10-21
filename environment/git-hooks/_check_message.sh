#!/bin/sh
# Rejects a commit message that names an AI helper or a co-author (user rule: commits are the user's own).
# Allowed: CLAUDE.md, .claude, file and folder paths with a slash that end in an extension or a slash
# (environment/claude/rules.md), git's own "Merge branch ..." line, and the diff that commit -v adds below the scissors
# line. Keep the word list in step with ~/.claude/hooks/hawk/no_ai_in_pr.py, which checks GitHub PR text.
msg_file="$1"
path='(^|[[:space:]'"'"'"=])[^[:space:]'"'"'"=:]*\/[^[:space:]'"'"'"]*(\.[[:alnum:]]{1,8}|\/)([[:space:]'"'"'",;:)!?.]|$)'
body=$(sed -e '/^# -* >8 -*$/,$d' "$msg_file" | grep -v '^#' | sed -E \
  -e '/^Merge (remote-tracking )?branch(es)? /d' \
  -e 's/[Cc][Ll][Aa][Uu][Dd][Ee]\.[Mm][Dd]//g' \
  -e 's/\.[Cc][Ll][Aa][Uu][Dd][Ee]([^[:alnum:]_]|$)/\1/g' \
  -e "s/$path/\\1\\3/g" -e "s/$path/\\1\\3/g")
# Whole words only, so "Regenerated", "philanthropic" or "generated with TRELLIS" pass.
bad=$(printf '%s\n' "$body" | grep -inE 'co-authored-by|(^|[^[:alpha:]])(claude|anthropic)([^[:alpha:]]|$)|(^|[^[:alpha:]])generated (with|by) ai([^[:alpha:]]|$)|ai-generated' | head -3)
robot_emoji=$(printf '\360\237\244\226')
robot=$(printf '%s\n' "$body" | LC_ALL=C grep -F "$robot_emoji" | head -1)
if [ -n "$robot" ]; then bad="$bad
$robot"; fi
if [ -n "$bad" ]; then
  echo "COMMIT REJECTED: the message mentions an AI helper or a co-author. Commits are the user's own: one short line, no AI." >&2
  printf '%s\n' "$bad" | sed 's/^/  > /' >&2
  exit 1
fi
exit 0
