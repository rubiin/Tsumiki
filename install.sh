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
NC='\033[0m' # No Color

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
    printf '%s\n' "$1"
}

die() {
    printf 'error: %s\n' "$1" >&2
    exit 1
}

require_cmd() {
    command -v "$1" >/dev/null 2>&1 || die "$1 not found"
}

assert_clean_repo() {
    git -C "$INSTALL_DIR" diff --quiet || die "existing repo has uncommitted changes in $INSTALL_DIR"
    git -C "$INSTALL_DIR" diff --cached --quiet || die "existing repo has staged changes in $INSTALL_DIR"
}

bootstrap_repo() {
    if [ -d "$INSTALL_DIR/.git" ]; then
        log "==> Updating existing repo in $INSTALL_DIR"
        log "==> Verifying repo has no local changes"
        assert_clean_repo
        git -C "$INSTALL_DIR" pull --ff-only
        log "==> Repo update complete"
        return
    fi

    log "==> Checking install directory state"
    if [ -e "$INSTALL_DIR" ] && [ -n "$(find "$INSTALL_DIR" -mindepth 1 -maxdepth 1 2>/dev/null | head -n 1)" ]; then
        die "$INSTALL_DIR exists and is not an empty git repo"
    fi

    mkdir -p "$(dirname "$INSTALL_DIR")"
    log "==> Cloning Tsumiki into $INSTALL_DIR"
    git clone "$REPO_URL" "$INSTALL_DIR"
    log "==> Clone complete"
}

run_init() {
    log "==> Preparing install + setup"
    log "==> Running init.sh -install -setup"
    bash "$INSTALL_DIR/init.sh" -install -setup
    log "==> init.sh finished successfully"
}

ensure_path_entry() {
    local rc_file="$1"
    local path_line='export PATH="$HOME/.local/bin:$PATH"'

    [ -f "$rc_file" ] || return

    if ! grep -Fq "$path_line" "$rc_file"; then
        log "==> Adding ~/.local/bin to PATH in $rc_file"
        printf '\n%s\n' "$path_line" >>"$rc_file"
    fi
}

setup_tsu_command() {
    log "==> Setting up tsu command"
    mkdir -p "$BIN_DIR"
    chmod +x "$INSTALL_DIR/init.sh"
    ln -sfn "$INSTALL_DIR/init.sh" "$TSU_PATH"
    log "==> Linked $TSU_PATH -> $INSTALL_DIR/init.sh"

    ensure_path_entry "$HOME/.bashrc"
    ensure_path_entry "$HOME/.zshrc"

    log "==> tsu command ready . restart your terminal or source your shell config to use it"
}

log "==> Starting Tsumiki installer"
log "==> Target directory: $INSTALL_DIR"
require_cmd git

print_banner
bootstrap_repo
run_init
setup_tsu_command
log "==> Done. Tsumiki ready in $INSTALL_DIR"
