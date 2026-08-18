#!/usr/bin/env bash

set -euo pipefail

INSTALL_DIR="$HOME/.config/tsumiki"
REPO_URL="https://github.com/rubiin/tsumiki.git"
BIN_DIR="$HOME/.local/bin"
TSU_PATH="$BIN_DIR/tsu"

# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

print_banner() {
    cat <<'EOF'
████████╗███████╗██╗   ██╗███╗   ███╗██╗██╗  ██╗██╗
╚══██╔══╝██╔════╝██║   ██║████╗ ████║██║██║ ██╔╝██║
   ██║   ███████╗██║   ██║██╔████╔██║██║█████╔╝ ██║
   ██║   ╚════██║██║   ██║██║╚██╔╝██║██║██╔═██╗ ██║
   ██║   ███████║╚██████╔╝██║ ╚═╝ ██║██║██║  ██╗██║
   ╚═╝   ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═╝╚═╝
EOF
}

log() {
    printf "${BLUE}%s${NC}\n" "$1"
}

success() {
    printf "${GREEN}%s${NC}\n" "$1"
}

warn() {
    printf "${YELLOW}%s${NC}\n" "$1"
}

die() {
    printf "${RED}error:${NC} %s\n" "$1" >&2
    exit 1
}

require_cmd() {
    command -v "$1" >/dev/null 2>&1 || die "'$1' is required but not installed. Please install it and retry."
}

assert_clean_repo() {
    git -C "$INSTALL_DIR" diff --quiet || die "Local changes detected in $INSTALL_DIR. Commit or stash them before updating."
    git -C "$INSTALL_DIR" diff --cached --quiet || die "Staged changes detected in $INSTALL_DIR. Please clean up before proceeding."
}

bootstrap_repo() {
    if [ -d "$INSTALL_DIR/.git" ]; then
        log "🔄 Existing installation detected"
        log "🔍 Checking for uncommitted changes..."
        assert_clean_repo

        log "→ Pulling latest updates from remote repository..."
        git -C "$INSTALL_DIR" pull --ff-only

        success "✅ Repository successfully updated"
        return
    fi

    log "📁 Preparing installation directory"
    if [ -e "$INSTALL_DIR" ] && [ -n "$(find "$INSTALL_DIR" -mindepth 1 -maxdepth 1 2>/dev/null | head -n 1)" ]; then
        die "Directory $INSTALL_DIR already exists and is not empty. Refusing to overwrite."
    fi

    mkdir -p "$(dirname "$INSTALL_DIR")"

    log "📦 Cloning repository"
    log "→ Source: $REPO_URL"
    log "→ Destination: $INSTALL_DIR"

    git clone "$REPO_URL" "$INSTALL_DIR"

    success "✅ Repository cloned successfully"
}

run_init() {
    log "🛠️  Running setup script"
    log "🚀 This will install dependencies and configure Tsumiki"

    bash "$INSTALL_DIR/tsumiki.sh" -install -setup

    success "✅ Setup completed successfully"
}

ensure_path_entry() {
    local rc_file="$1"
    local path_line='export PATH="$HOME/.local/bin:$PATH"'

    [ -f "$rc_file" ] || return

    if ! grep -Fq "$path_line" "$rc_file"; then
        log "📝 Updating PATH in $rc_file"
        printf '\n%s\n' "$path_line" >>"$rc_file"
        success "✅ PATH updated"
    fi
}

setup_tsu_command() {
    log "⚙️  Configuring 'tsu' command"

    mkdir -p "$BIN_DIR"
    chmod +x "$INSTALL_DIR/tsumiki.sh"

    ln -sfn "$INSTALL_DIR/tsumiki.sh" "$TSU_PATH"

    log "🔗 Symlink created:"
    log "→ $TSU_PATH → $INSTALL_DIR/tsumiki.sh"

    ensure_path_entry "$HOME/.bashrc"
    ensure_path_entry "$HOME/.zshrc"

    warn "⚠ You may need to restart your terminal or run:"
    warn "  source ~/.bashrc  (or ~/.zshrc)"
}

# --- Main ---
log "🚀 Starting Tsumiki installer"
log "→ Install path: $INSTALL_DIR"

require_cmd git

print_banner
bootstrap_repo
run_init
setup_tsu_command

success "🎉 Installation complete! You can now run 'tsu'"
