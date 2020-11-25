# mccli

This is a small program and library that makes it much easier to manage minecraft servers on linux (and probably other) OSes. It provides some easy to use commands that allows you to for example, upgrade the server binary, create a new server or change the server port etc. just with one command. It also makes it easy to attach to the server console from the command line.

## Install

Before installing, make sure the dependencies are installed.

```bash
# Ubuntu/Debian:
sudo apt install python3-libtmux python3-dbus python3-requests

# Arch:
sudo pacman -S python-libtmux python-dbus python-requests
```

Then just follow these steps for a standard installation:

```bash
sudo useradd minecraft
sudo mkdir /home/minecraft && sudo chown minecraft:minecraft /home/minecraft
sudo mkdir /opt/mccli && sudo chown minecraft:minecraft /opt/mccli
sudo -u minecraft git clone https://github.com/alvesvaren/mccli.git /opt/mccli
cd /opt/mccli
sudo ./install.sh
```

## Update

```bash
cd /opt/mccli
sudo ./update.sh
```

> **Note:** If upgrading from 0.0.14 or earlier, run `sudo systemctl disable /etc/systemd/system/minecraft-server@.service` and `sudo rm /usr/bin/mccli` before upgrading

> **Another note:** If upgrading from between 0.1.6 and 0.1.9, you might need to run `sudo -u minecraft git reset --hard origin/master` and then re-run the script `./update.sh`

## Usage

### Basic usage

```bash
mccli create servername
mccli enable --now servername
mccli console servername
```

### All available commands

| Command + arguments                                         | Description                                                                                | Example                                   |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ----------------------------------------- |
| `mccli create [name] [--provider {vanilla,papermc,spigot}]` | Creates a new server                                                                       | `mccli create example --provider vanilla` |
| `mccli update <name> [--provider {vanilla,papermc,spigot}]` | Change the server jar version                                                              | `mccli update example --provider papermc` |
| `mccli status <name>`                                       | Shows the current (systemd) status for the specified server                                | `mccli status example`                    |
| `mccli start <name>`                                        | Starts the specified server using systemd                                                  | `mccli start example`                     |
| `mccli stop <name>`                                         | Stops the specified server using systemd                                                   | `mccli stop example`                      |
| `mccli enable [--now] <name>`                               | Enable automatic starting of the server (on reboot). If called with `--now`, also start it | `mccli enable --now example`              |
| `mccli disable [--now] <name>`                              | Disable automatic starting of the server. If called with `--now`, also stop it             | `mccli disable --now example`             |
| `mccli restart <name>`                                      | Restart the server                                                                         | `mccli restart example`                   |
| `mccli attach <name>`                                       | Attach to the server console. To detach, Press **_Ctrl+b_ followed by _d_**                | `mccli attach example`                    |
| `mccli run <name> <command>`                                | Send the specified command to the server (using tmux send-keys)                            | `mccli run example say Hello everyone!`   |
| `mccli list`                                                | List all running servers (that has an active tmux session) and their version               | `mccli list`                              |
| `mccli modify [--file] <name> <key> <value>`                | Modify the _server.properties_ file (if no other was specified).                           | `mccli modify example server-port 25566`  |
| `mccli`                                                     | Shows the version and usage of mccli                                                       | `mccli`                                   |

> **Note:** You can run any command with the argument _-h_ to show the usage for that specific command

## Develop

> This is sort of broken right now but it should work after you've installed mccli at least once using the "Install" instructions

1. Clone the repository wherever you'd like
2. `cd mccli`
3. ```bash
   git checkout dev
   python -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```
4. Make sure the mccli binary is correct (`whereis mccli` should return something that's in this repository)

## Project status

### Planned features:

-   [x] Code to interface with server files
    -   [x] Vanilla support
    -   [x] Paper support
    -   [x] Waterfall support
-   [x] Code to manage virtual console sessions (for example tmux)
-   [x] Systemd service (template) to start minecraft servers
-   [x] Code to manage systemd service
-   [ ] Backup system (both automatic and manual)

### Other features that I might add in the future

-   [ ] Web interface
-   [ ] Spigot/Buildtools support
-   [ ] Bungeecord support
-   [ ] SSH server that just handles mccli
    -   [ ] Client that can communicate using said ssh server
-   [ ] REST api for use with some sort of client
-   [ ] Command scheduling
-   [ ] FTP server
-   [ ] Access policies to manage user access to different servers
-   [ ] Automatic port forwarding using UPnP
-   [ ] YML file support when using modify command
-   [ ] Plugin manager
-   [ ] Colors when running commands
-   [ ] CLI autocompletion
