#!/bin/bash

ERROR_STR="\e[31m\e[1mError:\e[0m"
SUCCESS_STR="\e[32m\e[1mSuccess:\e[0m"
WARN_STR="\e[33m\e[1mWarn:\e[0m"
INFO_STR="\e[34m\e[1mInfo:\e[0m"
DIM_QUOTE="\e[2m'\e[22m"

options() {
    JQ_OUT=python -
}

sudo -v
if [ $? -ne 0 ]; then
    echo -e "$ERROR_STR Sudo verification failed!"
    exit 1
fi
echo -e "\e[1mInstallation script for MCCLI"
echo

echo -e "$INFO_STR Checking of minecraft user exists"
getent passwd minecraft >/dev/null
if [ $? -ne 0 ]; then
    echo -e "$ERROR_STR You need to add a user called 'minecraft'"
    exit 1
fi
echo -e "$SUCCESS_STR Seems to exist!"
echo

echo -e "$INFO_STR Creating directory /opt/minecraft-servers"
sudo mkdir -p /opt/minecraft-servers
echo -e "$INFO_STR Changing ownership of /opt/minecraft-servers to 'minecraft:minecraft'"
sudo chown minecraft:minecraft /opt/minecraft-servers
echo

echo -e "$INFO_STR Checking validity of sudoers file..."
visudo -scf ./sudoers.conf
if [ $? -ne 0 ]; then
    echo -e "$ERROR_STR ./sudoers.conf is invalid!"
    echo -e "$WARN_STR Aborting. Check output"
    exit 1
fi
echo -e "$SUCCESS_STR Validity check passed!"
echo

echo -e "$INFO_STR Adding sudoers file to sudoers.d"
sudo cp ./sudoers.conf /etc/sudoers.d/10-mccli
echo

echo -e "$INFO_STR Installing mccli with pip"
sudo pip3 install .
echo

echo -e "$INFO_STR Linking service template with systemd"
sudo systemctl enable $PWD/minecraft-server@.service
echo -e "$INFO_STR Reloading daemons"
sudo systemctl daemon-reload
echo

echo -e "$WARN_STR Make sure to add yourself to the ${DIM_QUOTE}minecraft$DIM_QUOTE group to be able to use mccli without entering sudo password"
echo
echo -e "$INFO_STR Most likely you are able to add yourself to the minecraft group by typing: ${DIM_QUOTE}sudo usermod -aG minecraft $USER$DIM_QUOTE"
echo
echo -e "$SUCCESS_STR MCCLI successfully installed!"
