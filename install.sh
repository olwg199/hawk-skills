#!/usr/bin/env bash
set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$REPO_DIR/skills"
PUBLIC_REMOTE_URL="https://github.com/olwg199/hawk-skills.git"
SSH_PUSH_REMOTE_URL="git@github.com:olwg199/hawk-skills.git"

GREEN='\033[0;32m'
NC='\033[0m'

ok()   { echo -e "${GREEN}  ✓${NC} $1"; }

CLAUDE_COMMANDS_MANIFEST="$HOME/.hawk-skills-claude-commands"

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
        fi
    done
}

remove_legacy_copied_commands() {
    local commands_dir="$1"
    local command_path

    [ -d "$commands_dir" ] || return

    # TODO(next-commit): remove this temporary prefix migration cleanup.
    # One-time migration for old unprefixed and h-prefixed skill commands.
    for skill_name in quick-review hawk-skills-update h-quick-review h-skills-update; do
        command_path="$commands_dir/$skill_name.md"
        [ -f "$command_path" ] || continue
        [ -L "$command_path" ] && continue

        if grep -Eq "^name: ($skill_name|Hawk Quick Review|Hawk Skills Update)$" "$command_path"; then
            rm "$command_path"
        fi
    done
}

remove_claude_command_mirrors() {
    local commands_dir="$1"
    local link target skill_name command_path

    remove_stale_skill_links "$commands_dir" "Claude command"

    [ -d "$commands_dir" ] || return

    for link in "$commands_dir"/*; do
        [ -L "$link" ] || continue

        target=$(readlink "$link")
        skill_name=$(skill_name_from_target "$target" || true)
        [ -n "$skill_name" ] || continue

        rm "$link"
    done

    # TODO(next-commit): remove this copied mirror cleanup after one migration cycle.
    for skill_dir in "$SKILLS_DIR"/*/; do
        [ -f "$skill_dir/SKILL.md" ] || continue
        skill_name=$(basename "$skill_dir")
        command_path="$commands_dir/$skill_name.md"
        [ -f "$command_path" ] || continue
        [ -L "$command_path" ] && continue

        if grep -q "^name: $skill_name$" "$command_path"; then
            rm "$command_path"
        fi
    done

    if [ -f "$CLAUDE_COMMANDS_MANIFEST" ]; then
        while IFS= read -r skill_name; do
            [ -n "$skill_name" ] || continue
            command_path="$commands_dir/$skill_name.md"
            [ -f "$command_path" ] || continue
            [ -L "$command_path" ] && continue
            rm "$command_path"
        done < "$CLAUDE_COMMANDS_MANIFEST"
    fi

    rm -f "$CLAUDE_COMMANDS_MANIFEST"
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
    remove_stale_skill_links "$HOME/.claude/skills" "Claude skill"
    remove_legacy_copied_commands "$HOME/.claude/commands"

    if $NO_CLAUDE_COMMANDS; then
        remove_claude_command_mirrors "$HOME/.claude/commands"
    else
        remove_stale_skill_links "$HOME/.claude/commands" "Claude command"
    fi

    installed_commands=()
    for skill_dir in "$SKILLS_DIR"/*/; do
        [ -f "$skill_dir/SKILL.md" ] || continue
        skill_name=$(basename "$skill_dir")
        if ! $NO_CLAUDE_COMMANDS; then
            installed_commands+=("$skill_name")
            ln -sf "$skill_dir/SKILL.md" ~/.claude/commands/"$skill_name.md"
            ok "command: /$skill_name"
        fi
        ln -snf "$skill_dir" ~/.claude/skills/"$skill_name"
        ok "skill:   /$skill_name (agent + slash command)"
    done

    if $NO_CLAUDE_COMMANDS; then
        rm -f "$CLAUDE_COMMANDS_MANIFEST"
    else
        printf '%s\n' "${installed_commands[@]}" > "$CLAUDE_COMMANDS_MANIFEST"
    fi
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
    echo "Usage: $0 [--claude | --codex | --all] [--no-claude-commands | --claude-commands]"
    echo ""
    echo "  --claude              Install for Claude Code"
    echo "  --codex               Install for Codex CLI"
    echo "  --all                 Install for all CLIs (default)"
    echo "  --no-claude-commands  Remove and skip legacy Claude command mirrors (default)"
    echo "  --claude-commands     Install legacy Claude command mirrors for older Claude Code versions"
}

INSTALL_CLAUDE=false
INSTALL_CODEX=false
NO_CLAUDE_COMMANDS=true
CLAUDE_COMMANDS=false
EXPLICIT_NO_CLAUDE_COMMANDS=false

if [ $# -eq 0 ]; then
    INSTALL_CLAUDE=true
    INSTALL_CODEX=true
fi

for arg in "$@"; do
    case $arg in
        --claude)     INSTALL_CLAUDE=true ;;
        --codex)      INSTALL_CODEX=true ;;
        --all)        INSTALL_CLAUDE=true; INSTALL_CODEX=true ;;
        --no-claude-commands) NO_CLAUDE_COMMANDS=true; EXPLICIT_NO_CLAUDE_COMMANDS=true ;;
        --claude-commands)    CLAUDE_COMMANDS=true; NO_CLAUDE_COMMANDS=false ;;
        --help|-h)    usage; exit 0 ;;
        *) echo "Unknown option: $arg"; usage; exit 1 ;;
    esac
done

if $EXPLICIT_NO_CLAUDE_COMMANDS && $CLAUDE_COMMANDS; then
    echo "Use only one of --no-claude-commands or --claude-commands"
    exit 1
fi

save_repo_path
normalize_origin_remote
$INSTALL_CLAUDE && install_claude_code
$INSTALL_CODEX  && install_codex

echo ""
echo "Done. Restart your CLI to pick up new skills."
