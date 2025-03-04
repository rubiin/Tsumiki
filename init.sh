#!/bin/bash
# shellcheck source=/dev/null

set -e  # Exit immediately if a command exits with a non-zero status
set -u  # Treat unset variables as an error
set -o pipefail  # Prevent errors in a pipeline from being masked


INSTALL_DIR=`dirname -- "$0"`

start_bar() {
	# Navigate to the $HOME/bar directory
	cd "$INSTALL_DIR" || {
		echo -e "\033[31mDirectory $INSTALL_DIR does not exist.\033[0m\n"
		exit 1
	}
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


 __ __  __ __  ___      ___  ____   ____  ____     ___  _
|  |  ||  |  ||   \    /  _]|    \ /    ||    \   /  _]| |
|  |  ||  |  ||    \  /  [_ |  o  )  o  ||  _  | /  [_ | |
|  _  ||  ~  ||  D  ||    _]|   _/|     ||  |  ||    _]| |___
|  |  ||___, ||     ||   [_ |  |  |  _  ||  |  ||   [_ |     |
|  |  ||     ||     ||     ||  |  |  |  ||  |  ||     ||     |
|__|__||____/ |_____||_____||__|  |__|__||__|__||_____||_____|

$VERSION

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
	sudo pacman -S --noconfirm --needed pipewire playerctl dart-sass networkmanager power-profiles-daemon brightnessctl pkgconf wf-recorder kitty python pacman-contrib gtk3 cairo gtk-layer-shell libgirepository gobject-introspection gobject-introspection-runtime python-pip python-gobject python-psutil python-cairo python-dbus python-loguru python-setproctitle


	if command -v yay &> /dev/null; then
		aur_helper="yay"
	elif command -v paru &> /dev/null; then
		aur_helper="paru"
	else
		echo -e "\033[33myay or paru not found. Install the aur packages \033[36mgray-git \033[36mpython-fabric \033[33mwith the aur helper installed.\033[0m\n"
		exit 1
	fi


    if command -v paru &> /dev/null; then
		aur_helper="paru"
	else
		aur_helper="yay"
	fi

	# Install packages using yay (AUR helper)
	$aur_helper -S --noconfirm --needed gray-git python-fabric gnome-bluetooth-3.0 python-rlottie-python fabric-cli-git slurp
}

# Check the argument passed to the script and call the appropriate function
case "$1" in
-start)
	start_bar # Call the start_bar function
	;;
-update)
	git pull origin master # Placeholder for the update functionality
	;;
-install)
	install_packages # Call the install_packages function
	;;
*)
	echo -e "\033[31mUnknown command. Use \033[32m'-start'\033[33m, \033[32m'-update'\033[33m, \033[32m'-install'\033[31m.\033[0m\n"
	exit 1
	;;
esac
