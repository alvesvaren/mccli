# mccli (really WIP)

This is a collection of some python modules/scripts that makes it easier for you to manager minecraft servers on linux (and probably other) OSes.

## Install

Before installing, make sure the dependencies are installed.
Ubuntu/debian: `sudo apt install python3-libtmux python3-dbus python3-requests`
Arch: `sudo pacman -S python-libtmux python-dbus python-requests`

```bash
sudo useradd minecraft
sudo mkdir /opt/mccli && sudo chown minecraft:minecraft /opt/mccli
sudo -u minecraft git clone https://github.com/alvesvaren/mccli.git /opt/mccli
cd /opt/mccli
sudo ./install.sh
```

## Update

```bash
cd /opt/mccli
sudo -u minecraft git pull
sudo ./install.sh
```

## Basic usage

```bash
mccli create servername
mccli enable --now servername # doesn't really work right now, but this is how it's meant to be used, replace with 'sudo systemctl enabe --now minecraft-server@servername.service'
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
