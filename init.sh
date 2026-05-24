#!/bin/bash
# shellcheck source=/dev/null

set -e          # ❌ Exit immediately if a command exits with a non-zero status
set -u          # ⚠️ Treat unset variables as an error
set -o pipefail # 🛠️ Prevent errors in a pipeline from being masked

SCRIPT_PATH=$(readlink -f "$0")
INSTALL_DIR=$(dirname "$SCRIPT_PATH")
SCRIPT_NAME=$(basename "$0")

DETACHED_MODE=false
FORCE_REINSTALL=false

SHOULD_START=false
SHOULD_UPDATE=false
SHOULD_INSTALL=false
SHOULD_SETUP=false
SHOULD_STOP=false

log_info() { echo -e "\033[34m$1\033[0m"; }
log_success() { echo -e "\033[32m$1\033[0m"; }
log_warning() { echo -e "\033[33m$1\033[0m"; }
log_error() { echo -e "\033[31m$1\033[0m" >&2; }

die() {
	log_error "$1"
	exit 1
}

enter_install_dir() {
	cd "$INSTALL_DIR" || die "Directory $INSTALL_DIR does not exist."
}

check_prerequisites() {
	local cmd
	for cmd in git python3; do
		command -v "$cmd" &>/dev/null || die "$cmd is not installed. Please install it first. 📦"
	done
}

check_arch_distro() {
	if ! grep -qiE "arch|manjaro|endeavouros|arcolinux|garuda|artix|rebornos|archcraft|parabola|blackarch|chakra|cachyos" /etc/os-release; then
		log_warning "This script is designed to run on Arch-based systems (Arch, Manjaro, EndeavourOS, ArcoLinux, Garuda, Artix, RebornOS, Archcraft, Parabola, BlackArch, Chakra, CachyOS)."
		exit 1
	fi
}

ensure_venv() {
	local action=${1:-"check"}
	enter_install_dir

	case "$action" in
	check)
		if [ ! -d .venv ]; then
			die "❌ Virtual environment does not exist. Please run -setup first."
		fi
		;;
	setup)
		if [ ! -d .venv ]; then
			log_info "⚙️  Creating virtual environment..."
			python3 -m venv .venv || die "❌ Failed to create virtual environment."
			log_success "🎉 Virtual environment created successfully."
		else
			log_info "♻️  Using existing virtual environment."
		fi
		;;
	activate)
		source .venv/bin/activate || die "❌ Failed to activate virtual environment."
		;;
	*)
		die "Invalid action for ensure_venv: $action"
		;;
	esac
}

setup_venv() {
	ensure_venv setup

	log_info "📦 Installing Python dependencies..."
	local pip_args=(-r requirements.txt)
	local venv_python=.venv/bin/python

	if [ "$FORCE_REINSTALL" = true ]; then
		log_warning "🔄 Force reinstalling packages..."
		pip_args=(--force-reinstall "${pip_args[@]}")
	fi

	"$venv_python" -m pip install "${pip_args[@]}" || {
		die "❌ Failed to install packages from requirements.txt."
	}

	log_success "✅ Python dependencies installed successfully."
}

copy_config_files() {
	enter_install_dir
	local file src
	for file in config.toml theme.toml; do
		src="example/$file"
		if [ ! -f "$file" ]; then
			[ -f "$src" ] || die "$src not found. Cannot create default $file."
			log_warning "⚠️  $file not found. Copying from example..."
			cp "$src" "$file"
			log_success "✅ $file copied successfully."
		fi
	done
}

start_bar() {
	enter_install_dir
	local venv_python=.venv/bin/python

	copy_config_files

	VERSION=$(git tag --sort=-v:refname | head -n 1)

	ensure_venv check

	cat <<EOF

🎛️  Starting Tsumiki Bar 🎶

████████╗███████╗██╗   ██╗███╗   ███╗██╗██╗  ██╗██╗
╚══██╔══╝██╔════╝██║   ██║████╗ ████║██║██║ ██╔╝██║
   ██║   ███████╗██║   ██║██╔████╔██║██║█████╔╝ ██║
   ██║   ╚════██║██║   ██║██║╚██╔╝██║██║██╔═██╗ ██║
   ██║   ███████║╚██████╔╝██║ ╚═╝ ██║██║██║  ██╗██║
   ╚═╝   ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═╝╚═╝

version: $VERSION

EOF

	log_success "🐍 Using python: $venv_python"

	if [ "$DETACHED_MODE" = true ]; then
		log_warning "🛠️  Running in detached mode..."
		setsid "$venv_python" main.py >/dev/null 2>&1 &
		pid=$!
		sleep 0.1 # Give a moment for the process to potentially fail on startup.
		if ! ps -p "$pid" >/dev/null; then
			die "❌ Failed to start Tsumiki Bar in detached mode."
		fi
	else
		log_info "▶️  Starting Tsumiki Bar..."
		"$venv_python" main.py || die "❌ Failed to start Tsumiki Bar"
	fi
}

install_packages() {

	# Fun ASCII stays untouched 👍

	echo -e "\e[1;34m 📦 Installing prerequisites, this may take a while...\e[0m\n"

	# Install packages using pacman
	pacman_deps=(
		pipewire
		playerctl
		dart-sass
		power-profiles-daemon
		networkmanager
		brightnessctl
		pkgconf
		wf-recorder
		kitty
		python
		pacman-contrib
		gtk3
		cairo
		gtk-layer-shell
		libgirepository
		noto-fonts-emoji
		gobject-introspection
		gobject-introspection-runtime
		python-pip
		libnotify
		cliphist
		satty
		nvtop
	)

	# Install packages from AUR using yay
	aur_deps=(
		gnome-bluetooth-3.0
		slurp
		imagemagick
		tesseract
		tesseract-data-eng
		ttf-jetbrains-mono-nerd
		grimblast-git
		glace-git
		matugen-bin
	)

	sudo pacman -S --noconfirm --needed "${pacman_deps[@]}" || {
		log_error "❌ Failed to install pacman dependencies."
		exit 1
	}

	if command -v yay &>/dev/null; then
		aur_helper="yay"
	elif command -v paru &>/dev/null; then
		aur_helper="paru"
	else
		log_error "❌ AUR helper (yay or paru) not found. Please install one first."
		log_warning "⚠️  You can manually install: python-fabric-git"
		exit 1
	fi

	$aur_helper -S --noconfirm --needed "${aur_deps[@]}" || {
		log_error "❌ Failed to install some AUR dependencies."
		exit 1
	}

	log_success "🎉 System packages installed successfully."
}

usage() {
	log_info "Usage: $SCRIPT_NAME [OPTION]..."
	log_info "Execute one or more operations in sequence."
	log_success "✅ Available options:"
	log_success "  ▶️  -start         Start the bar"
	log_success "  🔄  -d             Enable detached mode (run in background)"
	log_success "  🔁  -f             Force reinstall Python packages during setup"
	log_success "  🛑  -stop          Stop running instances"
	log_success "  ⬆️  -update        Update from git"
	log_success "  📦  -install       Install system packages"
	log_success "  🐍  -setup         Setup virtual environment and Python dependencies"
	log_success "  🔁  -restart       Kill existing instances and start the bar"
	log_success "  ❓  -h, --help     Show this help message"

	echo ""

	log_warning "⚡ Examples:"
	log_info "  $SCRIPT_NAME -start                    # ▶️ Just start the bar"
	log_info "  $SCRIPT_NAME -d -start                 # ▶️ Detached start"
	log_info "  $SCRIPT_NAME -f -setup                 # 🔄 Force reinstall Python packages"
	log_info "  $SCRIPT_NAME -stop                     # 🛑 Stop running instances"
	log_info "  $SCRIPT_NAME -update -start            # ⬆️ Update then start"
	log_info "  $SCRIPT_NAME -install -setup -start    # 📦 Full setup and start"
	log_info "  $SCRIPT_NAME -restart                  # 🔁 Restart the bar"
}

kill_existing() {
	log_warning "🛑 Stopping existing Tsumiki instances..."
	pkill -x tsumiki || true
	while pgrep -x "tsumiki" >/dev/null; do
		sleep 0.1
	done
	log_success "✅ Existing instances stopped."
}

if [ "$#" -eq 0 ]; then
	usage
	exit 0
fi

NEEDS_ENV_CHECK=false

for arg in "$@"; do
	case "$arg" in
	-h|--help)
		usage
		exit 0
		;;
	-start)
		SHOULD_START=true
		NEEDS_ENV_CHECK=true
		;;
	-d)
		log_warning "Detached mode enabled 🔄"
		DETACHED_MODE=true
		;;
	-f)
		log_warning "Force reinstall mode enabled 🔁"
		FORCE_REINSTALL=true
		;;
	-stop)
		SHOULD_STOP=true
		;;
	-update)
		SHOULD_UPDATE=true
		NEEDS_ENV_CHECK=true
		;;
	-install)
		SHOULD_INSTALL=true
		NEEDS_ENV_CHECK=true
		;;
	-setup)
		SHOULD_SETUP=true
		NEEDS_ENV_CHECK=true
		;;
	-restart)
		SHOULD_STOP=true
		SHOULD_START=true
		NEEDS_ENV_CHECK=true
		;;
	*)
		log_error "Unknown command: $arg"
		usage >&2
		exit 1
		;;
	esac
done

if [ "$SHOULD_START" = false ] && [ "$SHOULD_STOP" = false ] && [ "$SHOULD_UPDATE" = false ] && [ "$SHOULD_INSTALL" = false ] && [ "$SHOULD_SETUP" = false ]; then
	log_warning "No operation selected."
	usage
	exit 1
fi

if [ "$NEEDS_ENV_CHECK" = true ]; then
	check_arch_distro
	check_prerequisites
fi

if [ "$SHOULD_STOP" = true ]; then
	log_info "=== 🛑 Stopping Tsumiki ==="
	kill_existing
fi

if [ "$SHOULD_UPDATE" = true ]; then
	log_info "=== ⬆️  Updating from Git ==="
	cd "$INSTALL_DIR" && git fetch --all && git reset --hard origin/$(git rev-parse --abbrev-ref HEAD)
	log_success "✅ Update completed."

	if ! git diff --quiet HEAD@{1} HEAD -- requirements.txt; then
		echo "📌 requirements.txt changed in the last update. Please update packages."
	fi
fi

if [ "$SHOULD_INSTALL" = true ]; then
	log_info "=== 📦 Installing System Packages ==="
	install_packages
fi

if [ "$SHOULD_SETUP" = true ]; then
	log_info "=== 🐍 Setting up Virtual Environment ==="
	setup_venv
fi

if [ "$SHOULD_START" = true ]; then
	log_info "=== ▶️ Starting Bar ==="
	start_bar
fi
