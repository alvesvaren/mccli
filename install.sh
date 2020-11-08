#!/bin/bash

ERROR_STR="\e[31m\e[1mError:\e[0m"
SUCCESS_STR="\e[32m\e[1mSuccess:\e[0m"
WARN_STR="\e[33m\e[1mWarn:\e[0m"
INFO_STR="\e[34m\e[1mInfo:\e[0m"
DIM_QUOTE="\e[2m'\e[22m"
confirm() {
    read -p "$1 [Y/n] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        return true
    fi
    return false
}

sudo -v
echo -e "\e[1mInstallation script for MCCLI"
echo

echo -e "$INFO_STR Checking of minecraft user exists"
getent passwd minecraft > /dev/null
if [ $? -ne 0 ]
then
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
if [ $? -ne 0 ]
then
    echo -e "$ERROR_STR ./sudoers.conf is invalid!"
    echo -e "$WARN_STR Aborting. Check output"
    exit 1
fi
echo -e "$SUCCESS_STR Validity check passed!"
echo

echo -e "$INFO_STR Adding sudoers file to sudoers.d"
sudo cp ./sudoers.conf /etc/sudoers.d/10-mccli.conf
echo

echo -e "$INFO_STR Installing mccli with pip (editable mode)"
sudo pip3 install -e .
echo

echo -e "$INFO_STR Linking service template with systemd"
sudo systemctl reenable $PWD/minecraft-server@.service
echo

echo -e "$INFO_STR Adding alias file to profile.d"
sudo cp ./profile.sh /etc/profile.d/10-mccli.sh
echo -e "$INFO_STR Sourcing alias file in current shell"
echo

echo -e "$WARN_STR If you have any other shells open, you need to restart it or source the alias file to use the ${DIM_QUOTE}mccli$DIM_QUOTE command"
source /etc/profile.d/10-mccli.sh
echo -e "$WARN_STR Make sure to add yourself to the ${DIM_QUOTE}minecraft$DIM_QUOTE group to be able to use mccli without entering sudo password"
echo
echo -e "$INFO_STR Most likely you are able to add yourself to the minecraft group by typing: ${DIM_QUOTE}sudo usermod -aG minecraft $USER$DIM_QUOTE"
echo
echo -e "$SUCCESS_STR MCCLI successfully installed!"
