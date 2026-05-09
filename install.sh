#!/usr/bin/env bash

set -euo pipefail

INSTALL_DIR="${TSUMIKI_INSTALL_DIR:-$HOME/.config/tsumiki}"
REPO_URL="${TSUMIKI_REPO_URL:-https://github.com/rubiin/Tsumiki.git}"
RUN_START=false
SKIP_INSTALL=false
SKIP_SETUP=false

log() {
    printf '%s\n' "$1"
}

die() {
    printf 'error: %s\n' "$1" >&2
    exit 1
}

usage() {
    cat <<'EOF'
Tsumiki curl installer

Usage:
  bash install.sh [--start] [--dir PATH] [--repo URL] [--no-install] [--no-setup]

Options:
  --start       Run init.sh -start after install/setup
  --dir PATH    Install into PATH instead of ~/.config/tsumiki
  --repo URL    Clone from custom git remote
  --no-install  Skip init.sh -install
  --no-setup    Skip init.sh -setup
  -h, --help    Show help
EOF
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
        assert_clean_repo
        git -C "$INSTALL_DIR" pull --ff-only
        return
    fi

    if [ -e "$INSTALL_DIR" ] && [ -n "$(find "$INSTALL_DIR" -mindepth 1 -maxdepth 1 2>/dev/null | head -n 1)" ]; then
        die "$INSTALL_DIR exists and is not an empty git repo"
    fi

    mkdir -p "$(dirname "$INSTALL_DIR")"
    log "==> Cloning Tsumiki into $INSTALL_DIR"
    git clone "$REPO_URL" "$INSTALL_DIR"
}

run_init() {
    local init_args=()

    if [ "$SKIP_INSTALL" = false ]; then
        init_args+=("-install")
    fi

    if [ "$SKIP_SETUP" = false ]; then
        init_args+=("-setup")
    fi

    if [ "$RUN_START" = true ]; then
        init_args+=("-start")
    fi

    if [ "${#init_args[@]}" -eq 0 ]; then
        log "==> Nothing to run. Repo ready at $INSTALL_DIR"
        return
    fi

    log "==> Running init.sh ${init_args[*]}"
    bash "$INSTALL_DIR/init.sh" "${init_args[@]}"
}

while [ "$#" -gt 0 ]; do
    case "$1" in
    --start)
        RUN_START=true
        ;;
    --dir)
        [ "$#" -ge 2 ] || die "--dir needs path"
        INSTALL_DIR="$2"
        shift
        ;;
    --repo)
        [ "$#" -ge 2 ] || die "--repo needs URL"
        REPO_URL="$2"
        shift
        ;;
    --no-install)
        SKIP_INSTALL=true
        ;;
    --no-setup)
        SKIP_SETUP=true
        ;;
    -h|--help)
        usage
        exit 0
        ;;
    *)
        die "unknown arg: $1"
        ;;
    esac
    shift
done

require_cmd git

bootstrap_repo
run_init
