#!/usr/bin/env bash
#
# Claude Toolkit Installer
# Installs skills, agents, commands, hooks, and settings to your project or globally.
#
# Usage:
#   ./install.sh                    # Interactive menu
#   ./install.sh --all              # Install everything
#   ./install.sh --global           # Install to ~/.claude (global)
#   ./install.sh --skills           # Install all skills
#   ./install.sh --skills testing-webapps frontend-design
#   ./install.sh --list             # List available components
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR=".claude"
GLOBAL=false

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════╗"
    echo "║       Claude Toolkit Installer        ║"
    echo "╚═══════════════════════════════════════╝"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_info() {
    echo -e "${BLUE}→${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}!${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# List available components in a category
list_category() {
    local category=$1
    local dir="$SCRIPT_DIR/$category"

    if [[ -d "$dir" ]] && [[ -n "$(ls -A "$dir" 2>/dev/null)" ]]; then
        echo -e "\n${BLUE}$category:${NC}"
        for item in "$dir"/*; do
            if [[ -d "$item" ]]; then
                local name=$(basename "$item")
                local desc=""

                # Try to get description from SKILL.md
                if [[ -f "$item/SKILL.md" ]]; then
                    # Try YAML frontmatter first
                    desc=$(grep -m1 "^description:" "$item/SKILL.md" 2>/dev/null | sed 's/description: *"\([^"]*\)".*/\1/' | head -c 80)
                    # If empty, try table format (| name | description |)
                    if [[ -z "$desc" ]]; then
                        desc=$(grep -m1 "^| $name" "$item/SKILL.md" 2>/dev/null | cut -d'|' -f3 | sed 's/^ *//;s/ *$//' | head -c 80)
                    fi
                elif [[ -f "$item.md" ]]; then
                    desc=$(head -1 "$item.md" | head -c 80)
                fi

                if [[ -n "$desc" ]]; then
                    echo "  • $name - $desc..."
                else
                    echo "  • $name"
                fi
            elif [[ -f "$item" ]]; then
                echo "  • $(basename "$item")"
            fi
        done
    fi
}

# List all available components
list_all() {
    print_header
    echo "Available components:"

    list_category "skills"
    list_category "agents"
    list_category "commands"
    list_category "hooks"
    list_category "settings"
    list_category "statusline"
    list_category "plugins"

    echo ""
}

# Install a single component
install_component() {
    local category=$1
    local name=$2
    local source="$SCRIPT_DIR/$category/$name"
    local dest="$TARGET_DIR/$category/$name"

    if [[ ! -e "$source" ]]; then
        print_error "Not found: $category/$name"
        return 1
    fi

    mkdir -p "$(dirname "$dest")"

    if [[ -d "$source" ]]; then
        cp -r "$source" "$dest"
    else
        cp "$source" "$dest"
    fi

    print_success "Installed $category/$name"
}

# Install all components in a category
install_category() {
    local category=$1
    shift
    local items=("$@")

    local source_dir="$SCRIPT_DIR/$category"

    if [[ ! -d "$source_dir" ]]; then
        print_warning "No $category directory found"
        return 0
    fi

    if [[ ${#items[@]} -eq 0 ]]; then
        # Install all items in category
        for item in "$source_dir"/*; do
            if [[ -e "$item" ]]; then
                local name=$(basename "$item")
                install_component "$category" "$name"
            fi
        done
    else
        # Install specific items
        for name in "${items[@]}"; do
            install_component "$category" "$name"
        done
    fi
}

# Install statusline
install_statusline() {
    local source="$SCRIPT_DIR/statusline/statusline.sh"
    local dest="$TARGET_DIR/statusline.sh"

    if [[ ! -f "$source" ]]; then
        print_warning "No statusline found"
        return 0
    fi

    cp "$source" "$dest"
    chmod +x "$dest"
    print_success "Installed statusline to $dest"
    print_info "Add to settings.json: \"statusLine\": { \"type\": \"command\", \"command\": \"$dest\" }"
}

# Install everything
install_all() {
    print_info "Installing all components to $TARGET_DIR"
    echo ""

    for category in skills agents commands hooks settings plugins; do
        if [[ -d "$SCRIPT_DIR/$category" ]] && [[ -n "$(ls -A "$SCRIPT_DIR/$category" 2>/dev/null)" ]]; then
            install_category "$category"
        fi
    done

    install_statusline

    echo ""
    print_success "All components installed!"
}

# Interactive menu
interactive_menu() {
    print_header

    echo "Where would you like to install?"
    echo "  1) Current project (./.claude)"
    echo "  2) Global (~/.claude)"
    echo "  3) Cancel"
    echo ""
    read -p "Choice [1]: " location_choice
    location_choice=${location_choice:-1}

    case $location_choice in
        1) TARGET_DIR=".claude" ;;
        2) TARGET_DIR="$HOME/.claude"; GLOBAL=true ;;
        3) echo "Cancelled."; exit 0 ;;
        *) echo "Invalid choice"; exit 1 ;;
    esac

    echo ""
    echo "What would you like to install?"
    echo "  1) Everything"
    echo "  2) Skills only"
    echo "  3) Select individual components"
    echo "  4) Cancel"
    echo ""
    read -p "Choice [1]: " install_choice
    install_choice=${install_choice:-1}

    case $install_choice in
        1) install_all ;;
        2) install_category "skills" ;;
        3) select_components ;;
        4) echo "Cancelled."; exit 0 ;;
        *) echo "Invalid choice"; exit 1 ;;
    esac
}

# Select individual components
select_components() {
    echo ""
    echo "Available skills:"

    local i=1
    local items=()

    for skill in "$SCRIPT_DIR/skills"/*; do
        if [[ -d "$skill" ]]; then
            local name=$(basename "$skill")
            echo "  $i) $name"
            items+=("skills:$name")
            ((i++))
        fi
    done

    for agent in "$SCRIPT_DIR/agents"/*; do
        if [[ -f "$agent" ]]; then
            local name=$(basename "$agent")
            echo "  $i) agents/$name"
            items+=("agents:$name")
            ((i++))
        fi
    done

    echo ""
    echo "Enter numbers separated by spaces (e.g., '1 3 4'), or 'all':"
    read -p "> " selections

    if [[ "$selections" == "all" ]]; then
        install_all
        return
    fi

    for sel in $selections; do
        if [[ $sel =~ ^[0-9]+$ ]] && [[ $sel -ge 1 ]] && [[ $sel -le ${#items[@]} ]]; then
            local item="${items[$((sel-1))]}"
            local category="${item%%:*}"
            local name="${item#*:}"
            install_component "$category" "$name"
        else
            print_warning "Invalid selection: $sel"
        fi
    done

    echo ""
    print_success "Installation complete!"
}

# Parse arguments
main() {
    if [[ $# -eq 0 ]]; then
        interactive_menu
        exit 0
    fi

    local category=""
    local items=()

    while [[ $# -gt 0 ]]; do
        case $1 in
            --global|-g)
                TARGET_DIR="$HOME/.claude"
                GLOBAL=true
                shift
                ;;
            --list|-l)
                list_all
                exit 0
                ;;
            --all|-a)
                install_all
                exit 0
                ;;
            --skills)
                category="skills"
                shift
                while [[ $# -gt 0 ]] && [[ ! "$1" =~ ^-- ]]; do
                    items+=("$1")
                    shift
                done
                install_category "$category" "${items[@]}"
                items=()
                ;;
            --agents)
                category="agents"
                shift
                while [[ $# -gt 0 ]] && [[ ! "$1" =~ ^-- ]]; do
                    items+=("$1")
                    shift
                done
                install_category "$category" "${items[@]}"
                items=()
                ;;
            --commands)
                category="commands"
                shift
                while [[ $# -gt 0 ]] && [[ ! "$1" =~ ^-- ]]; do
                    items+=("$1")
                    shift
                done
                install_category "$category" "${items[@]}"
                items=()
                ;;
            --hooks)
                category="hooks"
                shift
                while [[ $# -gt 0 ]] && [[ ! "$1" =~ ^-- ]]; do
                    items+=("$1")
                    shift
                done
                install_category "$category" "${items[@]}"
                items=()
                ;;
            --settings)
                category="settings"
                shift
                while [[ $# -gt 0 ]] && [[ ! "$1" =~ ^-- ]]; do
                    items+=("$1")
                    shift
                done
                install_category "$category" "${items[@]}"
                items=()
                ;;
            --statusline)
                shift
                install_statusline
                ;;
            --help|-h)
                echo "Claude Toolkit Installer"
                echo ""
                echo "Usage:"
                echo "  ./install.sh                    Interactive menu"
                echo "  ./install.sh --list             List available components"
                echo "  ./install.sh --all              Install everything"
                echo "  ./install.sh --global           Install to ~/.claude"
                echo "  ./install.sh --skills           Install all skills"
                echo "  ./install.sh --skills NAME...   Install specific skills"
                echo "  ./install.sh --agents           Install all agents"
                echo "  ./install.sh --commands         Install all commands"
                echo "  ./install.sh --hooks            Install all hooks"
                echo "  ./install.sh --statusline       Install custom statusline"
                echo ""
                echo "Examples:"
                echo "  ./install.sh --skills testing-webapps"
                echo "  ./install.sh --global --all"
                echo "  ./install.sh --skills --agents"
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                echo "Use --help for usage information"
                exit 1
                ;;
        esac
    done
}

main "$@"
