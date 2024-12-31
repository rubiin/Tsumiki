#!/bin/sh

start_bar() {
  # Navigate to the $HOME/bar directory
  cd $HOME/bar || {
    echo "Directory $HOME/bar does not exist."
    exit 1
  }

  # Check if the virtual environment exists, if not, create it
  if [ ! -d .venv ]; then
    echo "venv does not exist. Creating venv..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
      echo "Failed to create virtual environment. Exiting..."
      exit 1
    fi
    # Install required Python packages
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
      echo "Failed to install packages from requirements.txt. Exiting..."
      exit 1
    fi
  fi

  # Activate the virtual environment and run the main Python script
  source .venv/bin/activate
  python3 main.py
  deactivate
}

install_packages() {
  # Display an ASCII art (a small logo) in blue
  echo -e "\e[1;34m
     /\
    /  \
   /    \
  /______\
 /\      /\
/  \    /  \
\   \/\/   /
 \        /
  \______/
\e[0m"

  # Notify user about the installation process
  echo -e "\e[1;34mInstalling the pre-requisites, may take a while....\e[0m"

  # Install packages using pacman
  sudo pacman -S --noconfirm pipewire playerctl dart-sass networkmanager wl-clipboard brightnessctl python pacman-contrib gtk3 cairo gtk-layer-shell libgirepository gobject-introspection gobject-introspection-runtime python-pip python-gobject python-psutil python-cairo python-loguru pkgconf wf-recorder kitty grimblast gnome-bluetooth

  # Install packages using yay (AUR helper)
  yay -S --noconfirm gray-git python-fabric rlottie
}

# Check the argument passed to the script and call the appropriate function
case "$1" in
-start)
  start_bar # Call the start_bar function
  ;;
-update)
  echo "Not implemented yet" # Placeholder for the update functionality
  ;;
-install)
  install_packages # Call the install_packages function
  ;;
*)
  echo "Unknown command. Use '-start', '-update', or '-install'."
  exit 1
  ;;
esac
