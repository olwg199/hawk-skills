#!/usr/bin/env bash
set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$REPO_DIR/skills"
PUBLIC_REMOTE_URL="https://github.com/olwg199/hawk-skills.git"
SSH_PUSH_REMOTE_URL="git@github.com:olwg199/hawk-skills.git"

GREEN='\033[0;32m'
NC='\033[0m'

ok()   { echo -e "${GREEN}  ✓${NC} $1"; }

skill_exists() {
    [ -f "$SKILLS_DIR/$1/SKILL.md" ]
}

skill_name_from_target() {
    local target="$1"
    local rest

    case "$target" in
        "$SKILLS_DIR"/*)
            rest="${target#"$SKILLS_DIR"/}"
            ;;
        "$SKILLS_DIR"//*)
            rest="${target#"$SKILLS_DIR"//}"
            ;;
        *)
            return 1
            ;;
    esac

    rest="${rest#/}"
    printf '%s\n' "${rest%%/*}"
}

remove_stale_skill_links() {
    local link_dir="$1"
    local label="$2"
    local link target skill_name

    [ -d "$link_dir" ] || return

    for link in "$link_dir"/*; do
        [ -L "$link" ] || continue

        target=$(readlink "$link")
        skill_name=$(skill_name_from_target "$target" || true)
        [ -n "$skill_name" ] || continue

        if ! skill_exists "$skill_name"; then
            rm "$link"
            ok "removed stale $label: $(basename "$link")"
        fi
    done
}

save_repo_path() {
    echo "$REPO_DIR" > ~/.hawk-skills-repo
    ok "repo path saved to ~/.hawk-skills-repo"
}

normalize_origin_remote() {
    if ! git -C "$REPO_DIR" rev-parse --git-dir >/dev/null 2>&1; then
        return
    fi

    local origin_url
    origin_url=$(git -C "$REPO_DIR" remote get-url origin 2>/dev/null || true)

    case "$origin_url" in
        git@github.com:olwg199/hawk-skills.git|ssh://git@github.com/olwg199/hawk-skills.git)
            git -C "$REPO_DIR" remote set-url origin "$PUBLIC_REMOTE_URL"
            git -C "$REPO_DIR" remote set-url --push origin "$SSH_PUSH_REMOTE_URL"
            ok "origin fetch switched to HTTPS; push preserved over SSH"
            ;;
    esac
}

install_claude_code() {
    echo "Installing for Claude Code..."
    mkdir -p ~/.claude/commands ~/.claude/skills
    remove_stale_skill_links "$HOME/.claude/commands" "Claude command"
    remove_stale_skill_links "$HOME/.claude/skills" "Claude skill"

    for skill_dir in "$SKILLS_DIR"/*/; do
        [ -f "$skill_dir/SKILL.md" ] || continue
        skill_name=$(basename "$skill_dir")
        ln -sf "$skill_dir/SKILL.md" ~/.claude/commands/"$skill_name.md"
        ok "command: /$skill_name"
        ln -snf "$skill_dir" ~/.claude/skills/"$skill_name"
        ok "skill:   $skill_name (for agent invocation)"
    done
}

install_codex() {
    echo "Installing for Codex CLI..."
    mkdir -p ~/.codex/skills
    remove_stale_skill_links "$HOME/.codex/skills" "Codex skill"

    for skill_dir in "$SKILLS_DIR"/*/; do
        [ -f "$skill_dir/SKILL.md" ] || continue
        skill_name=$(basename "$skill_dir")
        ln -snf "$skill_dir" ~/.codex/skills/"$skill_name"
        ok "skill: /$skill_name"
    done
}

usage() {
    echo "Usage: $0 [--claude | --codex | --all]"
    echo ""
    echo "  --claude      Install for Claude Code"
    echo "  --codex       Install for Codex CLI"
    echo "  --all         Install for all CLIs (default)"
}

INSTALL_CLAUDE=false
INSTALL_CODEX=false

if [ $# -eq 0 ]; then
    INSTALL_CLAUDE=true
    INSTALL_CODEX=true
fi

for arg in "$@"; do
    case $arg in
        --claude)     INSTALL_CLAUDE=true ;;
        --codex)      INSTALL_CODEX=true ;;
        --all)        INSTALL_CLAUDE=true; INSTALL_CODEX=true ;;
        --help|-h)    usage; exit 0 ;;
        *) echo "Unknown option: $arg"; usage; exit 1 ;;
    esac
done

save_repo_path
normalize_origin_remote
$INSTALL_CLAUDE && install_claude_code
$INSTALL_CODEX  && install_codex

echo ""
echo "Done. Restart your CLI to pick up new skills."
