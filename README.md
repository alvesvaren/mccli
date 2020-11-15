# mccli

This is a collection of some python modules/scripts that makes it easier for you to manager minecraft servers on linux (and probably other) OSes.

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

## Basic usage

```bash
mccli create servername
mccli enable --now servername
mccli console servername
```

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
    -   [ ] Spigot/Buildtools support
    -   [ ] Waterfall support
    -   [ ] Sponge support
    -   [ ] Bungeecord support
-   [x] Code to manage virtual console sessions (for example tmux)
-   [x] Systemd service (template) to start minecraft servers
-   [x] Code to manage systemd service
-   [ ] Backup system (both automatic and manual)
-   [ ] Plugin manager
-   [ ] CLI autocompletion
-   [ ] Colors when running commands
-   [ ] Support for comments when using config_parser.py

### Other features that I might add in the future

-   [ ] Web interface
-   [ ] SSH server that just handles mccli
    -   [ ] Client that can communicate using said ssh server
-   [ ] REST api for use with some sort of client
-   [ ] Command scheduling
-   [ ] FTP server
-   [ ] Access policies to manage user access to different servers
-   [ ] Automatic port forwarding using UPnP
-   [ ] YML file support when using modify command
