#!/bin/bash

# Word of caution: changing this can break update module, be vigilant

DISTRO=""
DO_UPDATE=0
CHECK_FLATPAK=0
CHECK_SNAP=0
CHECK_BREW=0
TERMINAL="kitty"  # Default terminal

check_flatpak_updates() {
    local count=0
    if [[ "$CHECK_FLATPAK" -eq 1 && "$(command -v flatpak)" ]]; then
        count=$(flatpak remote-ls --updates 2>/dev/null | wc -l)
    fi
    echo "$count"
}

run_flatpak_update() {
    if [[ "$CHECK_FLATPAK" -eq 1 && "$(command -v flatpak)" ]]; then
        flatpak update -y || true
    fi
}

check_snap_updates() {
    local count=0
    if [[ "$CHECK_SNAP" -eq 1 && "$(command -v snap)" ]]; then
        count=$(snap refresh --list 2>/dev/null | grep -c "^\S")
    fi
    echo "$count"
}

run_snap_update() {
    if [[ "$CHECK_SNAP" -eq 1 && "$(command -v snap)" ]]; then
        sudo snap refresh || true
    fi
}

check_brew_updates() {
    local count=0
    if [[ "$CHECK_BREW" -eq 1 && "$(command -v brew)" ]]; then
        count=$(brew outdated --quiet | wc -l)
    fi
    echo "$count"
}

run_brew_update() {
    if [[ "$CHECK_BREW" -eq 1 && "$(command -v brew)" ]]; then
        brew update && brew upgrade || true
    fi
}

check_arch_updates() {
    local official_updates=0
    local aur_updates=0
    local flatpak_updates=0
    local snap_updates=0
    local brew_updates=0
    local tooltip=""

    if command -v checkupdates &>/dev/null; then
        official_updates=$(checkupdates 2>/dev/null | wc -l)
    fi

    local aur_helper="yay"
    if command -v paru &>/dev/null; then
        aur_helper="paru"
    fi

    if command -v "$aur_helper" &>/dev/null; then
        aur_updates=$($aur_helper -Qum 2>/dev/null | wc -l)
    fi

    tooltip="󰣇 Official $official_updates\n󰮯 AUR $aur_updates"

    if [[ "$CHECK_FLATPAK" -eq 1 ]]; then
        flatpak_updates=$(check_flatpak_updates)
        tooltip="$tooltip\n Flatpak $flatpak_updates"
    fi

    if [[ "$CHECK_SNAP" -eq 1 ]]; then
        snap_updates=$(check_snap_updates)
        tooltip="$tooltip\n Snap $snap_updates"
    fi

    if [[ "$CHECK_BREW" -eq 1 ]]; then
        brew_updates=$(check_brew_updates)
        tooltip="$tooltip\n Brew $brew_updates"
    fi

    local total_updates=$((official_updates + aur_updates + flatpak_updates + snap_updates + brew_updates))
    echo "{\"total\":\"$total_updates\", \"tooltip\":\"$tooltip\"}"
}

check_ubuntu_updates() {
    local official_updates=0
    local flatpak_updates=0
    if command -v apt-get &>/dev/null; then
        official_updates=$(apt-get -s -o Debug::NoLocking=true upgrade | grep -c ^Inst)
    fi
    flatpak_updates=$(check_flatpak_updates)

    local tooltip="󰕈 Official $official_updates"
    [[ "$CHECK_FLATPAK" -eq 1 ]] && tooltip="$tooltip\n Flatpak $flatpak_updates"

    local total_updates=$((official_updates + flatpak_updates))
    echo "{\"total\":\"$total_updates\", \"tooltip\":\"$tooltip\"}"
}

check_fedora_updates() {
    local official_updates=0
    local flatpak_updates=0
    if command -v dnf &>/dev/null; then
        official_updates=$(dnf check-update -q | grep -v '^Loaded plugins' | grep -v '^No match for' | wc -l)
    fi
    flatpak_updates=$(check_flatpak_updates)

    local tooltip="󰣛 Official $official_updates"
    [[ "$CHECK_FLATPAK" -eq 1 ]] && tooltip="$tooltip\n Flatpak $flatpak_updates"

    local total_updates=$((official_updates + flatpak_updates))
    echo "{\"total\":\"$total_updates\", \"tooltip\":\"$tooltip\"}"
}

check_opensuse_updates() {
    local official_updates=0
    local flatpak_updates=0
    if command -v zypper &>/dev/null; then
        official_updates=$(zypper lu | wc -l)
    fi
    flatpak_updates=$(check_flatpak_updates)

    local tooltip=" Official $official_updates"
    [[ "$CHECK_FLATPAK" -eq 1 ]] && tooltip="$tooltip\n Flatpak $flatpak_updates"

    local total_updates=$((official_updates + flatpak_updates))
    echo "{\"total\":\"$total_updates\", \"tooltip\":\"$tooltip\"}"
}

# Function to execute command in terminal
execute_in_terminal() {
    local command="$1"
    # Only allow safe terminal names (no spaces, no shell metacharacters)
    if [[ ! "$TERMINAL" =~ ^[a-zA-Z0-9._-]+$ ]]; then
        echo "Error: Terminal name contains invalid characters."
        exit 1
    fi
    # Check if terminal exists in PATH
    if ! command -v "$TERMINAL" >/dev/null 2>&1; then
        echo "Error: Terminal '$TERMINAL' not found in PATH."
        exit 1
    fi

    if [[ "$(basename "$TERMINAL")" == "kitty" ]]; then
        "$TERMINAL" --title systemupdate sh -c "${command}"
    elif [[ "$(basename "$TERMINAL")" == "alacritty" ]]; then
        "$TERMINAL" --title systemupdate -e sh -c "${command}"
    elif [[ "$(basename "$TERMINAL")" == "wezterm" ]]; then
        "$TERMINAL" start --title systemupdate -- sh -c "${command}"
    else
        "$TERMINAL" sh -c "${command}"
    fi
}

update_arch() {
    if command -v paru &> /dev/null; then
		aur_helper="paru"
	else
		aur_helper="yay"
	fi

command="
    # Cute Penguin ASCII Art with tsumiki text
    echo '      .--.  '
    echo '     |o_o | '
    echo '     |:_/ | '
    echo '    //   \\ \\ '
    echo '   (|     | )'
    echo '  /\'\\_   _/\'\\'
    echo '  \\___)=(___/ '
    echo ''
    echo '   tsumiki chan'
    echo ''\

    $aur_helper -Syyu
    flatpak update -y || true
    read -n 1 -p 'Press any key to continue...'
"

    execute_in_terminal "${command}"
    # --- dynamic tooltip construction ---
    local tooltip="󰣇 Official 0\n󰮯 AUR 0"
    [[ "$CHECK_FLATPAK" -eq 1 ]] && tooltip="$tooltip\n Flatpak 0"
    [[ "$CHECK_SNAP"   -eq 1 ]] && tooltip="$tooltip\n Snap 0"
    [[ "$CHECK_BREW"   -eq 1 ]] && tooltip="$tooltip\n Brew 0"

    echo "{\"total\":\"0\", \"tooltip\":\"$tooltip\"}"
}


update_ubuntu() {
    local command="
    sudo apt update && sudo apt upgrade -y
    flatpak update -y || true
    read -n 1 -p 'Press any key to continue...'
    "
    execute_in_terminal "$command"

    # --- dynamic tooltip construction ---
    local tooltip="󰣇 Official 0\n󰮯 AUR 0"
    [[ "$CHECK_FLATPAK" -eq 1 ]] && tooltip="$tooltip\n Flatpak 0"
    [[ "$CHECK_SNAP"   -eq 1 ]] && tooltip="$tooltip\n Snap 0"
    [[ "$CHECK_BREW"   -eq 1 ]] && tooltip="$tooltip\n Brew 0"

    echo "{\"total\":\"0\", \"tooltip\":\"$tooltip\"}"
}

update_fedora() {
    local command="
    sudo dnf upgrade --assumeyes
    flatpak update -y || true
    read -n 1 -p 'Press any key to continue...'
    "
    execute_in_terminal "$command"
    # --- dynamic tooltip construction ---
    local tooltip="󰣇 Official 0\n󰮯 AUR 0"
    [[ "$CHECK_FLATPAK" -eq 1 ]] && tooltip="$tooltip\n Flatpak 0"
    [[ "$CHECK_SNAP"   -eq 1 ]] && tooltip="$tooltip\n Snap 0"
    [[ "$CHECK_BREW"   -eq 1 ]] && tooltip="$tooltip\n Brew 0"

    echo "{\"total\":\"0\", \"tooltip\":\"$tooltip\"}"
}

update_opensuse() {
    local command="
    sudo zypper update -y
    flatpak update -y || true
    read -n 1 -p 'Press any key to continue...'
    "
    execute_in_terminal "$command"
    # --- dynamic tooltip construction ---
    local tooltip="󰣇 Official 0\n󰮯 AUR 0"
    [[ "$CHECK_FLATPAK" -eq 1 ]] && tooltip="$tooltip\n Flatpak 0"
    [[ "$CHECK_SNAP"   -eq 1 ]] && tooltip="$tooltip\n Snap 0"
    [[ "$CHECK_BREW"   -eq 1 ]] && tooltip="$tooltip\n Brew 0"

    echo "{\"total\":\"0\", \"tooltip\":\"$tooltip\"}"
}

# New os= style argument parsing
for arg in "$@"; do
    case "$arg" in
        os=arch)   DISTRO="arch" ;;
        os=ubuntu) DISTRO="ubuntu" ;;
        os=fedora) DISTRO="fedora" ;;
        os=suse)   DISTRO="suse" ;;
        --terminal=*)
            # Extract terminal value and validate it contains only safe characters
            terminal_value="${arg#*=}"
            if [[ "$terminal_value" =~ ^[a-zA-Z0-9_-]+$ ]]; then
                TERMINAL="$terminal_value"
            else
                echo "Error: Terminal name contains invalid characters. Only alphanumeric, underscore, and dash allowed."
                exit 1
            fi
            ;;
        --flatpak) CHECK_FLATPAK=1 ;;
        --snap)    CHECK_SNAP=1 ;;
        --brew)    CHECK_BREW=1 ;;
        up)        DO_UPDATE=1 ;;
        *)
            echo "Usage: $0 os=<arch|ubuntu|fedora|suse> [--terminal=<terminal>] [--flatpak] [--snap] [--brew] [up]"
            exit 1
            ;;
    esac
done

# Validate that DISTRO was set
if [[ -z "$DISTRO" ]]; then
    echo "Error: Missing required argument 'os=<arch|ubuntu|fedora|suse>'"
    exit 1
fi

# Run appropriate action
case "$DISTRO" in
    arch)   (( DO_UPDATE )) && update_arch     || check_arch_updates ;;
    ubuntu) (( DO_UPDATE )) && update_ubuntu   || check_ubuntu_updates ;;
    fedora) (( DO_UPDATE )) && update_fedora   || check_fedora_updates ;;
    suse)   (( DO_UPDATE )) && update_opensuse || check_opensuse_updates ;;
esac
