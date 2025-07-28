#!/bin/bash
# shellcheck source=/dev/null

set -e          # Exit immediately if a command exits with a non-zero status
set -u          # Treat unset variables as an error
set -o pipefail # Prevent errors in a pipeline from being masked

if ! grep -q "arch" /etc/os-release; then
	echo "This script is designed to run on Arch Linux."
	exit 1
fi

# Get the absolute path of the script's directory
SCRIPT_PATH=$(readlink -f "$0")
INSTALL_DIR=$(dirname "$SCRIPT_PATH")

copy_config_files() {
	# Navigate to the $INSTALL_DIR directory
	cd "$INSTALL_DIR" || {
		echo -e "\033[31mDirectory $INSTALL_DIR does not exist.\033[0m\n"
		exit 1
	}

	# Copy config.json from example if it doesn't exist
	if [ ! -f config.json ]; then
		if [ -f example/config.json ]; then
			echo -e "\033[33m  config.json not found. Copying from example...\033[0m\n"
			cp example/config.json config.json
			echo -e "\033[32m  config.json copied successfully.\033[0m\n"
		else
			echo -e "\033[31m  example/config.json not found. Cannot create default config.\033[0m\n"
			exit 1
		fi
	fi

	# Copy theme.json from example if it doesn't exist
	if [ ! -f theme.json ]; then
		if [ -f example/theme.json ]; then
			echo -e "\033[33m  theme.json not found. Copying from example...\033[0m\n"
			cp example/theme.json theme.json
			echo -e "\033[32m  theme.json copied successfully.\033[0m\n"
		else
			echo -e "\033[31m  example/theme.json not found. Cannot create default theme.\033[0m\n"
			exit 1
		fi
	fi
}

setup_venv() {
	# Navigate to the $INSTALL_DIR directory
	cd "$INSTALL_DIR" || {
		echo -e "\033[31mDirectory $INSTALL_DIR does not exist.\033[0m\n"
		exit 1
	}

	# Check if the virtual environment exists, if not, create it
	if [ ! -d .venv ]; then
		echo -e "\033[32m  venv does not exist. Creating venv...\033[0m\n"
		if ! python3 -m venv .venv; then
			printf "\033[31m  Failed to create virtual environment. Exiting...\033[0m\n" >&2
			exit 1
		fi

		printf "\033[32m  Virtual environment created successfully.\033[0m\n"
	else
		printf "\033[33m  Virtual environment already exists.\033[0m\n"
	fi

	# Activate virtual environment
	source .venv/bin/activate

	if ! source .venv/bin/activate; then
		printf "\033[31m  Failed to activate venv. Exiting...\033[0m\n" >&2
		exit 1
	fi


	# Install Python dependencies
		printf "\033[32m  Installing python dependencies, brace yourself.\033[0m\n"
	pip install -r requirements.txt

	if ! pip install -r requirements.txt; then
		printf "\033[31mFailed to install packages from requirements.txt. Exiting...\033[0m\n" >&2
		deactivate
		exit 1
	fi

		printf "\033[32m  Python dependencies installed successfully.\033[0m\n"
	deactivate
}

start_bar() {
	# Navigate to the $INSTALL_DIR directory
	cd "$INSTALL_DIR" || {
		echo -e "\033[31mDirectory $INSTALL_DIR does not exist.\033[0m\n"
		exit 1
	}

	# Ensure config files exist
	copy_config_files

	VERSION=$(git describe --tags --abbrev=0)

	# Check if the virtual environment exists, if not, create it
	if [ ! -d .venv ]; then
		echo -e "\033[32m  venv does not exist. Creating venv...\033[0m\n"
		python3 -m venv .venv

		if [ $? -ne 0 ]; then
			echo -e "\033[31m  Failed to create virtual environment. Exiting...\033[0m\n"
			exit 1
		fi

		source .venv/bin/activate

		if [ $? -ne 0 ]; then
			echo -e "\033[31m  Failed to activate venv. Exiting...\033[0m\n"
			exit 1
		fi

		echo -e "\033[32m  Installing python dependencies, brace yourself.\033[0m\n"
		pip install -r requirements.txt

		if [ $? -ne 0 ]; then
			echo -e "\033[31mFailed to install packages from requirements.txt. Exiting...\033[0m\n"
			exit 1
		fi
		echo -e "\033[32m  All done, starting bar.\033[0m\n"
	else
		echo -e "\033[32m  Using existing venv.\033[0m\n"
		source .venv/bin/activate
	fi

	cat <<EOF


████████╗███████╗██╗   ██╗███╗   ███╗██╗██╗  ██╗██╗
╚══██╔══╝██╔════╝██║   ██║████╗ ████║██║██║ ██╔╝██║
   ██║   ███████╗██║   ██║██╔████╔██║██║█████╔╝ ██║
   ██║   ╚════██║██║   ██║██║╚██╔╝██║██║██╔═██╗ ██║
   ██║   ███████║╚██████╔╝██║ ╚═╝ ██║██║██║  ██╗██║
   ╚═╝   ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═╝╚═╝

version:	$VERSION


EOF
	echo -e "\e[32mUsing python:\e[0m \e[34m$(which python)\e[0m\n"
	python3 main.py
	deactivate
}

install_packages() {

	echo "								  "
	echo "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"
	echo "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"
	echo "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"
	echo "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"
	echo "⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣷⣤⣙⢻⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀"
	echo "⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀"
	echo "⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀"
	echo "⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⡿⠛⠛⠿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀"
	echo "⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀"
	echo "⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⠿⣆⠀⠀⠀⠀"
	echo "⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀"
	echo "⠀⢀⣾⣿⣿⠿⠟⠛⠋⠉⠉⠀⠀⠀⠀⠀⠀⠉⠉⠙⠛⠻⠿⣿⣿⣷⡀⠀"
	echo "⣠⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⣄"
	echo "								  "

	# Notify user about the installation process
	echo -e "\e[1;34mInstalling the pre-requisites, may take a while....\e[0m\n"

	# Install packages using pacman
	pacman_deps=(
		pipewire
		playerctl
		dart-sass
		networkmanager
		brightnessctl
		power-profiles-daemon
		pkgconf
		wf-recorder
		kitty
		libnotify
		python
		pacman-contrib
		gtk3
		cairo
		gtk-layer-shell
		libgirepository
		gobject-introspection
		gobject-introspection-runtime
		python-pip
		python-gobject
		python-psutil
		python-cairo
		python-loguru
		python-requests
		python-setproctitle
		cliphist
		noto-fonts-emoji
		satty
	)

		aur_deps=(
		gray-git
		python-fabric-git
		gnome-bluetooth-3.0
		python-rlottie-python
		python-pytomlpp
		python-pyjson5
		python-ijson
		slurp
		imagemagick
		tesseract
		tesseract-data-eng
		ttf-jetbrains-mono-nerd
		grimblast-git
	)


	sudo pacman -S --noconfirm --needed "${pacman_deps[@]}"  || true

	if command -v yay &>/dev/null; then
		aur_helper="yay"
	elif command -v paru &>/dev/null; then
		aur_helper="paru"
	else
		echo -e "\033[33myay or paru not found. Install the aur packages \033[36mgray-git \033[36mpython-fabric \033[33mwith the aur helper installed.\033[0m\n"
		exit 1
	fi

	if command -v paru &>/dev/null; then
		aur_helper="paru"
	else
		aur_helper="yay"
	fi

	# Install packages using yay (AUR helper)

	$aur_helper -S --noconfirm --needed "${aur_deps[@]}"  || true

}

# Function to display usage information
usage() {
	printf "\033[31mUsage: %s [OPTION]...\033[0m\n" "$0"
	printf "Execute one or more operations in sequence.\n\n"
	printf "\033[32mAvailable options:\033[0m\n"
	printf "\033[32m  -start\033[0m         Start the bar\n"
	printf "\033[32m  -update\033[0m        Update from git\n"
	printf "\033[32m  -install\033[0m       Install system packages only\n"
	printf "\033[32m  -setup\033[0m         Setup virtual environment and Python dependencies only\n"
	printf "\033[32m  -install-setup\033[0m Install packages and setup virtual environment\n"
	printf "\033[32m  -restart\033[0m       Kill existing instances and start the bar\n"
	printf "\n\033[33mExamples:\033[0m\n"
	printf "  %s -start                    # Just start the bar\n" "$0"
	printf "  %s -update -start            # Update and then start\n" "$0"
	printf "  %s -install -setup -start    # Full setup and start\n" "$0"
	printf "  %s -restart                  # Restart the bar\n" "$0"
}

# Function to kill existing instances
kill_existing() {
	echo -e "\033[33m  Stopping existing Tsumiki instances...\033[0m"
	pkill tsumiki || true
	# Wait for the process to terminate completely
	while pgrep -x "tsumiki" >/dev/null; do
		sleep 0.1
	done
	echo -e "\033[32m  Existing instances stopped.\033[0m\n"
}

# Check if no arguments provided
if [ $# -eq 0 ]; then
  usage >&2
  exit 1
fi

# Process each argument in sequence
for arg in "$@"; do
	case "$arg" in
	-start)
		echo -e "\033[34m=== Starting Bar ===\033[0m"
		start_bar
		;;
	-update)
		echo -e "\033[34m=== Updating from Git ===\033[0m"
		cd $INSTALL_DIR && git pull
		echo -e "\033[32m  Update completed.\033[0m\n"
		;;
	-install)
		echo -e "\033[34m=== Installing System Packages ===\033[0m"
		install_packages
		;;
	-setup)
		echo -e "\033[34m=== Setting up Virtual Environment ===\033[0m"
		setup_venv
		;;
	-install-setup)
		echo -e "\033[34m=== Installing Packages and Setting up Environment ===\033[0m"
		install_packages
		setup_venv
		;;
	-restart)
		echo -e "\033[34m=== Restarting Bar ===\033[0m"
		kill_existing
		start_bar
		;;
	*)
		printf "\033[31mUnknown command: %s\033[0m\n" "$arg" >&2
		usage >&2
		exit 1
		;;
	esac
done
