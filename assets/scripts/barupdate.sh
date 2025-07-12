#!/bin/bash

INSTALL_DIR=$(dirname -- "$0")

# Navigate to the $HOME/bar directory
cd "$INSTALL_DIR" || {
		echo -e "\033[31mDirectory $INSTALL_DIR does not exist.\033[0m\n"
		exit 1
}

# Fetch updates from the remote
git fetch

# Check if there are any changes
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})

if [ "$LOCAL" != "$REMOTE" ]; then
    # If they differ, there are updates
    notify-send "Bar Update" "New updates are available. Pull changes to update the bar."
fi
