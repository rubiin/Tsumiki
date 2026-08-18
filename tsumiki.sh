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
	for cmd in git uv; do
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
	activate)
		source .venv/bin/activate || die "❌ Failed to activate virtual environment."
		;;
	*)
		die "Invalid action for ensure_venv: $action"
		;;
	esac
}

setup_venv() {
	enter_install_dir

	log_info "📦 Syncing Python dependencies with uv..."
	local uv_args=()

	if [ "$FORCE_REINSTALL" = true ]; then
		log_warning "🔄 Force reinstalling packages..."
		uv_args+=(--reinstall)
	fi

	uv sync "${uv_args[@]}" || {
		die "❌ Failed to sync packages with uv (pyproject.toml / uv.lock)."
	}

	log_success "✅ Python dependencies installed successfully."
}

copy_config_files() {
	enter_install_dir
	local file src
	for file in config.toml; do
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
		uv
		pacman-contrib
		gtk3
		cairo
		gtk-layer-shell
		libgirepository
		noto-fonts-emoji
		gobject-introspection
		gobject-introspection-runtime
		libnotify
		libqalculate
		cliphist
		satty
		nvtop
	)

	# Install packages from AUR using yay
	aur_deps=(
		gnome-bluetooth-3.0
		fabric-cli-git
		slurp
		imagemagick
		tesseract
		tesseract-data-eng
		ttf-jetbrains-mono-nerd
		grimblast-git
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
	log_success "  📡  -ipc <cmd>     IPC commands (list-windows, toggle, reload-config, etc.)"
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

IPC_ARGS=()
IPC_MODE=false

for arg in "$@"; do
	case "$arg" in
	-h|--help)
		usage
		exit 0
		;;
	-ipc)
		IPC_MODE=true
		shift
		IPC_ARGS=("$@")
		break
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

# Handle IPC mode
if [ "$IPC_MODE" = true ]; then
	if [ ${#IPC_ARGS[@]} -eq 0 ]; then
		log_error "IPC requires a command."
		echo ""
		echo "Available IPC commands:"
		echo "  list-windows, lw           List all windows and their visibility"
		echo "  toggle, toggle-window <w>  Toggle window visibility"
		echo "  list-actions, actions      List all available actions"
		echo "  reload-config              Reload Tsumiki configuration"
		echo "  execute, exec <cmd>        Execute a shell command"
		echo "  inspector                  Open the GTK inspector"
		echo "  invoke, action <a> [args]  Invoke an action with arguments"
		echo "  help                       Show this help message"
		exit 1
	fi

	IPC_COMMAND="${IPC_ARGS[0]}"
	IPC_REST_ARGS=(${IPC_ARGS[@]:1})

	# Check if fabric-cli is available
	if ! command -v fabric-cli &>/dev/null; then
		log_error "fabric-cli not found in PATH."
		log_warning "Install it from: https://github.com/Fabric-Development/fabric-cli"
		exit 1
	fi

	# Auto-detect instance name from running instances
	IPC_INSTANCE=$(fabric-cli list-all --json 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    names = data.get('instances-dbus-names', [])
    # Get the first instance name (strip 'org.Fabric.fabric.' prefix)
    for name in names:
        if name.startswith('org.Fabric.fabric.'):
            print(name.replace('org.Fabric.fabric.', ''))
            break
    else:
        print('')
except:
    print('')
" 2>/dev/null)

	if [ -z "$IPC_INSTANCE" ]; then
		log_error "No running Tsumiki instance found."
		log_warning "Please start Tsumiki first: $SCRIPT_NAME -start"
		exit 1
	fi

	case "$IPC_COMMAND" in
	list-windows|lw)
		fabric-cli list-windows "$IPC_INSTANCE" --json
		;;
	toggle|toggle-window)
		if [ ${#IPC_REST_ARGS[@]} -eq 0 ]; then
			log_error "toggle requires a window name."
			echo "Usage: $SCRIPT_NAME -ipc toggle <window-name>"
			exit 1
		fi
		fabric-cli invoke-action "$IPC_INSTANCE" toggle-window "${IPC_REST_ARGS[0]}"
		;;
	list-actions|actions)
		fabric-cli list-actions "$IPC_INSTANCE" --json
		;;
	reload-config)
		log_info "Reloading configuration..."
		fabric-cli invoke-action "$IPC_INSTANCE" reload-config
		log_success "Configuration reloaded."
		;;
	execute|exec)
		if [ ${#IPC_REST_ARGS[@]} -eq 0 ]; then
			log_error "execute requires a command."
			echo "Usage: $SCRIPT_NAME -ipc execute <command>"
			exit 1
		fi
		fabric-cli invoke-action "$IPC_INSTANCE" execute-command "${IPC_REST_ARGS[*]}"
		;;
	invoke|action)
		if [ ${#IPC_REST_ARGS[@]} -eq 0 ]; then
			log_error "invoke requires an action name."
			echo "Usage: $SCRIPT_NAME -ipc invoke <action> [args...]"
			exit 1
		fi
		fabric-cli invoke-action "$IPC_INSTANCE" "${IPC_REST_ARGS[@]}"
		;;
	inspector)
		fabric-cli invoke-action "$IPC_INSTANCE" open-inspector
		;;
	help)
		echo "Tsumiki IPC - Inter-Process Communication"
		echo ""
		echo "Usage: $SCRIPT_NAME -ipc <command> [args...]"
		echo ""
		echo "Commands:"
		echo "  list-windows, lw           List all windows and their visibility"
		echo "  toggle, toggle-window <w>  Toggle window visibility"
		echo "  list-actions, actions      List all available actions"
		echo "  reload-config              Reload Tsumiki configuration"
		echo "  execute, exec <cmd>        Execute a shell command"
		echo "  inspector                  Open the GTK inspector"
		echo "  invoke, action <a> [args]  Invoke an action with arguments"
		echo "  help                       Show this help message"
		;;
	*)
		log_error "Unknown IPC command: $IPC_COMMAND"
		echo "Run '$SCRIPT_NAME -ipc help' for usage information"
		exit 1
		;;
	esac
	exit 0
fi

if [ "$SHOULD_START" = false ] && [ "$SHOULD_STOP" = false ] && [ "$SHOULD_UPDATE" = false ] && [ "$SHOULD_INSTALL" = false ] && [ "$SHOULD_SETUP" = false ]; then
	log_warning "No operation selected."
	usage
	exit 1
fi

if [ "$NEEDS_ENV_CHECK" = true ]; then
	check_arch_distro
	# uv is installed by -install below; only require it upfront otherwise
	if [ "$SHOULD_INSTALL" = false ]; then
		check_prerequisites
	fi
fi

if [ "$SHOULD_STOP" = true ]; then
	log_info "=== 🛑 Stopping Tsumiki ==="
	kill_existing
fi

if [ "$SHOULD_UPDATE" = true ]; then
	log_info "=== ⬆️  Updating from Git ==="
	cd "$INSTALL_DIR" && git fetch --all && git reset --hard origin/$(git rev-parse --abbrev-ref HEAD)
	log_success "✅ Update completed."

	if ! git diff --quiet HEAD@{1} HEAD -- uv.lock; then
		echo "📌 uv.lock changed in the last update. Please update packages."
	fi
fi

if [ "$SHOULD_INSTALL" = true ]; then
	log_info "=== 📦 Installing System Packages ==="
	install_packages
fi

if [ "$SHOULD_SETUP" = true ]; then
	log_info "=== 🐍 Setting up Virtual Environment (uv) ==="
	setup_venv
fi

if [ "$SHOULD_START" = true ]; then
	log_info "=== ▶️ Starting Bar ==="
	start_bar
fi
