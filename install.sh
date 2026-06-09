#!/usr/bin/env bash
set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$REPO_DIR/skills"
PUBLIC_REMOTE_URL="https://github.com/olwg199/hawk-skills.git"
SSH_PUSH_REMOTE_URL="git@github.com:olwg199/hawk-skills.git"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ok()   { echo -e "${GREEN}  ✓${NC} $1"; }
info() { echo -e "${YELLOW}  →${NC} $1"; }

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
    for skill_dir in "$SKILLS_DIR"/*/; do
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
    for skill_dir in "$SKILLS_DIR"/*/; do
        skill_name=$(basename "$skill_dir")
        ln -snf "$skill_dir" ~/.codex/skills/"$skill_name"
        ok "skill: /$skill_name"
    done
}

setup_autoupdate_claude() {
    local settings="$HOME/.claude/settings.json"
    local repo_arg
    repo_arg=$(printf '%q' "$REPO_DIR")
    local pull_cmd="git -C $repo_arg pull --ff-only --quiet 2>/dev/null || true"

    mkdir -p "$HOME/.claude"

    if [ ! -f "$settings" ]; then
        echo '{}' > "$settings"
    fi

    if grep -q "hawk-skills" "$settings" 2>/dev/null; then
        ok "auto-update hook already configured"
        return
    fi

    info "Add the following hook to $settings to enable auto-update on Claude startup:"
    echo ""
    echo '  "hooks": {'
    echo '    "Startup": ['
    echo '      {'
    echo '        "hooks": ['
    echo '          {'
    echo '            "type": "command",'
    echo "            \"command\": \"$pull_cmd\""
    echo '          }'
    echo '        ]'
    echo '      }'
    echo '    ]'
    echo '  }'
    echo ""
    info "Or run: /update-config to configure it interactively in Claude Code."
}

usage() {
    echo "Usage: $0 [--claude | --codex | --all] [--autoupdate]"
    echo ""
    echo "  --claude      Install for Claude Code"
    echo "  --codex       Install for Codex CLI"
    echo "  --all         Install for all CLIs (default)"
    echo "  --autoupdate  Print auto-update hook instructions for Claude Code"
}

INSTALL_CLAUDE=false
INSTALL_CODEX=false
AUTOUPDATE=false

if [ $# -eq 0 ]; then
    INSTALL_CLAUDE=true
    INSTALL_CODEX=true
fi

for arg in "$@"; do
    case $arg in
        --claude)     INSTALL_CLAUDE=true ;;
        --codex)      INSTALL_CODEX=true ;;
        --all)        INSTALL_CLAUDE=true; INSTALL_CODEX=true ;;
        --autoupdate) AUTOUPDATE=true ;;
        --help|-h)    usage; exit 0 ;;
        *) echo "Unknown option: $arg"; usage; exit 1 ;;
    esac
done

save_repo_path
normalize_origin_remote
$INSTALL_CLAUDE && install_claude_code
$INSTALL_CODEX  && install_codex
$AUTOUPDATE     && setup_autoupdate_claude

echo ""
echo "Done. Restart your CLI to pick up new skills."
