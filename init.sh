#!/bin/bash
# shellcheck source=/dev/null

set -e          # ❌ Exit immediately if a command exits with a non-zero status
set -u          # ⚠️ Treat unset variables as an error
set -o pipefail # 🛠️ Prevent errors in a pipeline from being masked

# --- Check Arch-based distro ---
if ! grep -qiE "arch|manjaro|endeavouros|arcolinux|garuda|artix|rebornos|archcraft|parabola|blackarch|chakra|cachyos" /etc/os-release; then
	echo "⚠️  This script is designed to run on Arch-based systems (Arch, Manjaro, EndeavourOS, ArcoLinux, Garuda, Artix, RebornOS, Archcraft, Parabola, BlackArch, Chakra, CachyOS)."
	exit 1
fi

SCRIPT_PATH=$(readlink -f "$0")
INSTALL_DIR=$(dirname "$SCRIPT_PATH")

DETACHED_MODE=false
FORCE_REINSTALL=false

SHOULD_START=false
SHOULD_UPDATE=false
SHOULD_INSTALL=false
SHOULD_SETUP=false
SHOULD_STOP=false

log_info() { echo -e "\033[34mℹ️  $1\033[0m"; }
log_success() { echo -e "\033[32m✅ $1\033[0m"; }
log_warning() { echo -e "\033[33m⚠️  $1\033[0m"; }
log_error() { echo -e "\033[31m❌ $1\033[0m" >&2; }

check_prerequisites() {
	if ! command -v git &>/dev/null; then
		log_error "Git is not installed. 📦 Please install git first."
		exit 1
	fi

	if ! command -v python3 &>/dev/null; then
		log_error "Python3 is not installed. 🐍 Please install python3 first."
		exit 1
	fi
}

ensure_venv() {
	local action=${1:-"check"}

	cd "$INSTALL_DIR" || {
		log_error "📂 Directory $INSTALL_DIR does not exist."
		exit 1
	}

	case "$action" in
	check)
		if [ ! -d .venv ]; then
			log_error "❌ Virtual environment does not exist. Please set it up first."
			exit 1
		fi
		;;
	setup)
		if [ ! -d .venv ]; then
			log_info "⚙️  Creating virtual environment..."
			if ! python3 -m venv .venv; then
				log_error "❌ Failed to create virtual environment."
				exit 1
			fi
			log_success "🎉 Virtual environment created successfully."
		else
			log_info "♻️  Using existing virtual environment."
		fi
		;;
	activate)
		if ! source .venv/bin/activate; then
			log_error "❌ Failed to activate virtual environment."
			exit 1
		fi
		;;
	*)
		log_error "Invalid action for ensure_venv: $action"
		exit 1
		;;
	esac
}

setup_venv() {
	ensure_venv setup
	ensure_venv activate

	log_info "📦 Installing Python dependencies..."

	if [ "$FORCE_REINSTALL" = true ]; then
		log_warning "🔄 Force reinstalling packages..."
		if ! pip install --force-reinstall -r requirements.txt; then
			log_error "❌ Failed to force reinstall packages from requirements.txt."
			deactivate
			exit 1
		fi
	else
		if ! pip install -r requirements.txt; then
			log_error "❌ Failed to install packages from requirements.txt."
			deactivate
			exit 1
		fi
	fi

	log_success "✅ Python dependencies installed successfully."

	deactivate
}

copy_config_files() {
	cd "$INSTALL_DIR" || {
		log_error "📂 Directory $INSTALL_DIR does not exist."
		exit 1
	}

	if [ ! -f config.toml ]; then
		if [ -f example/config.toml ]; then
			log_warning "⚠️  config.toml not found. Copying from example..."
			cp example/config.toml config.toml
			log_success "✅ config.toml copied successfully."
		else
			log_error "❌ example/config.toml not found. Cannot create default config."
			exit 1
		fi
	fi

	if [ ! -f theme.toml ]; then
		if [ -f example/theme.toml ]; then
			log_warning "⚠️  theme.toml not found. Copying from example..."
			cp example/theme.toml theme.toml
			log_success "✅ theme.toml copied successfully."
		else
			log_error "❌ example/theme.toml not found. Cannot create default theme."
			exit 1
		fi
	fi
}

start_bar() {
	cd "$INSTALL_DIR" || {
		log_error "📂 Directory $INSTALL_DIR does not exist."
		exit 1
	}

	copy_config_files

	VERSION=$(git tag --sort=-v:refname | head -n 1)

	ensure_venv activate

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

	log_success "🐍 Using python: $(which python)"

	if [ "$DETACHED_MODE" = true ]; then
		log_warning "🛠️  Running in detached mode..."
		setsid python3 main.py >/dev/null 2>&1 &
		pid=$!
		sleep 0.1 # Give a moment for the process to potentially fail on startup.
		if ! ps -p "$pid" >/dev/null; then
			log_error "❌ Failed to start Tsumiki Bar in detached mode."
			exit 1
		fi
	else
		log_info "▶️  Starting Tsumiki Bar..."
		python3 main.py || {
			log_error "❌ Failed to start Tsumiki Bar"
			exit 1
		}
	fi

	deactivate
}

install_packages() {

	# Fun ASCII stays untouched 👍

	echo -e "\e[1;34m 📦 Installing the pre-requisites, may take a while....\e[0m\n"

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

	if command -v paru &>/dev/null; then
		aur_helper="paru"
	elif command -v yay &>/dev/null; then
		aur_helper="yay"
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
	log_error "❌ Usage: $0 [OPTION]..."
	log_info "ℹ️  Execute one or more operations in sequence."
	log_success "✅ Available options:"
	log_success "  ▶️  -start         Start the bar"
	log_success "  🔄  -d             Enable detached mode (run in background)"
	log_success "  �  -f             Force reinstall Python packages during setup"
	log_success "  �🛑  -stop          Stop running instances"
	log_success "  ⬆️  -update        Update from git"
	log_success "  📦  -install       Install system packages"
	log_success "  🐍  -setup         Setup virtual environment and Python dependencies"
	log_success "    -restart       Kill existing instances and start the bar"
	log_warning "⚡ Examples:"
	log_info "  $0 -start                    # ▶️ Just start the bar"
	log_info "  $0 -d -start                 # ▶️ Detached start"
	log_info "  $0 -f -setup                 # 🔄 Force reinstall Python packages"
	log_info "  $0 -stop                     # 🛑 Stop running instances"
	log_info "  $0 -update -start            # ⬆️ Update then start"
	log_info "  $0 -install -setup -start    # 📦 Full setup and start"
	log_info "  $0 -restart                  # 🔁 Restart the bar"
}

kill_existing() {
	log_warning "🛑 Stopping existing Tsumiki instances..."
	pkill -x tsumiki || true
	while pgrep -x "tsumiki" >/dev/null; do
		sleep 0.1
	done
	log_success "✅ Existing instances stopped."
}

check_prerequisites

for arg in "$@"; do
	case "$arg" in
	-start)
		SHOULD_START=true
		;;
	-d)
		log_warning "Detached mode enabled"
		DETACHED_MODE=true
		;;
	-f)
		log_warning "Force reinstall mode enabled"
		FORCE_REINSTALL=true
		;;
	-stop)
		SHOULD_STOP=true
		;;
	-update)
		SHOULD_UPDATE=true
		;;
	-install)
		SHOULD_INSTALL=true
		;;
	-setup)
		SHOULD_SETUP=true
		;;
	-restart)
		SHOULD_STOP=true
		SHOULD_START=true
		;;
	*)
		log_error "Unknown command: $arg"
		usage >&2
		exit 1
		;;
	esac
done

if [ "$SHOULD_STOP" = true ]; then
	log_info "=== 🛑 Stopping Tsumiki ==="
	kill_existing
fi

if [ "$SHOULD_UPDATE" = true ]; then
	log_info "=== ⬆️  Updating from Git ==="
	cd "$INSTALL_DIR" && git fetch --all && git reset --hard origin/$(git rev-parse --abbrev-ref HEAD)
	log_success "✅ Update completed."

	if ! git diff --quiet HEAD@{1} HEAD -- requirements.txt; then
    echo "📌 requirements.txt changed in the last update. Please update the packages"
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
