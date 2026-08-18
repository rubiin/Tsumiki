# IPC (Inter-Process Communication) Support

Tsumiki supports IPC via D-Bus, allowing external programs and scripts to interact with and control the application at runtime. This is implemented through Fabric's built-in D-Bus integration.

## How It Works

Fabric registers D-Bus actions using the `@Application.action()` decorator. These actions can be invoked from external programs using:

1. **tsumiki.sh** - The main Tsumiki CLI wrapper
2. **fabric-cli** - The official Fabric CLI tool
3. **D-Bus directly** - Using tools like `dbus-send` or `gdbus`

### D-Bus Details

- **Interface**: `org.Fabric.fabric`
- **Object Path**: `/org/Fabric/fabric`

## Available Actions

### toggle_window

Toggle the visibility of a Tsumiki window.

**Arguments:**
- `name` (string): Window name to toggle

### list_windows

List all available windows and their visibility status.

### reload_config

Reload Tsumiki configuration.

### execute_command

Execute a shell command and return the output.

**Arguments:**
- `command` (string): Shell command to execute

### open_inspector

Open the GTK inspector for debugging.

## Using tsumiki.sh

The recommended way to use IPC is through `tsumiki.sh`:

```bash
# List windows
./tsumiki.sh -ipc list-windows

# Toggle a window
./tsumiki.sh -ipc toggle launcher

# Reload configuration
./tsumiki.sh -ipc reload-config

# Execute a command
./tsumiki.sh -ipc execute "echo hello"

# Open GTK inspector
./tsumiki.sh -ipc inspector

# Show IPC help
./tsumiki.sh -ipc help
```

### Short aliases

```bash
./tsumiki.sh -ipc lw                  # list-windows
./tsumiki.sh -ipc toggle launcher     # toggle window
./tsumiki.sh -ipc exec "echo hello"   # execute command
./tsumiki.sh -ipc inspector           # open GTK inspector
./tsumiki.sh -ipc actions             # list-actions
```

## Using fabric-cli

### Installation

```bash
# From AUR (Arch Linux)
yay -S fabric-cli-git

# Or build from source
git clone https://github.com/Fabric-Development/fabric-cli
cd fabric-cli
meson setup --buildtype=release --prefix=/usr build
sudo meson install -C build
```

### Basic Commands

```bash
# List all running Fabric instances
fabric-cli list-all

# List windows in default instance
fabric-cli list-windows

# List available actions
fabric-cli list-actions

# Toggle a window
fabric-cli invoke-action toggle_window launcher

# Execute a command
fabric-cli execute "echo hello"

# Reload configuration
fabric-cli invoke-action reload_config
```

### JSON Output

All commands support the `--json` flag for machine-readable output:

```bash
fabric-cli list-windows --json
```

## Using D-Bus Directly

### With gdbus (GLib)

```bash
# List windows
gdbus call --session \
    --dest org.Fabric.fabric \
    --object-path /org/Fabric/fabric \
    --method org.freedesktop.DBus.Properties.Get \
    org.Fabric.fabric Windows

# Toggle window
gdbus call --session \
    --dest org.Fabric.fabric \
    --object-path /org/Fabric/fabric \
    --method org.Fabric.fabric.InvokeAction \
    toggle_window \
    "['launcher']"
```

### With dbus-send

```bash
# List windows
dbus-send --session --type=method_call \
    --dest=org.Fabric.fabric \
    /org/Fabric/fabric \
    org.freedesktop.DBus.Properties.Get \
    string:"org.Fabric.fabric" \
    string:"Windows"
```

## Examples

### Toggle Launcher from Script

```bash
#!/bin/bash
# toggle-launcher.sh

./tsumiki.sh -ipc toggle launcher
```

### Reload Config on File Change

```bash
#!/bin/bash
# watch-config.sh

CONFIG_FILE="$HOME/.config/tsumiki/config.toml"

while true; do
    inotifywait -q -e modify "$CONFIG_FILE"
    sleep 1  # Debounce
    echo "Config changed, reloading..."
    ./tsumiki.sh -ipc reload-config
done
```

## Extending IPC

To add new IPC actions to Tsumiki, add a new `@Application.action()` decorator in `main.py`:

```python
@Application.action()
def my_custom_action(arg1: str, arg2: int = 0):
    """Custom action description."""
    # Your logic here
    return "result"
```

Then invoke it via tsumiki.sh:

```bash
./tsumiki.sh -ipc invoke my_custom_action "hello" "42"
```

Or via fabric-cli:

```bash
fabric-cli invoke-action my_custom_action "hello" "42"
```

## Security Considerations

- D-Bus actions are only accessible to the local user by default
- No authentication is required for local connections
- The `execute_command` action can run arbitrary commands - use with caution
- Consider restricting access in shared environments

## Troubleshooting

### "couldn't find a running Fabric instance"

Ensure Tsumiki is running:
```bash
pgrep -f tsumiki
```

### "command not found: fabric-cli"

Install fabric-cli (see Installation section above).

### Permission Denied

Ensure you're running as the same user who started Tsumiki.

### No Output

Check if Tsumiki has any windows open:
```bash
./tsumiki.sh -ipc list-windows
```

## Further Reading

- [Fabric Documentation](https://wiki.ffpy.org/)
- [fabric-cli Repository](https://github.com/Fabric-Development/fabric-cli)
- [Fabric IPC Documentation](https://wiki.ffpy.org/api/services/hyprland/)
