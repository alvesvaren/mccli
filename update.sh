echo "Pulling from git repo..."
sudo -u minecraft git pull --ff-only
echo
echo "Running install script..."
sudo ./install.sh
echo "Updated mccli!"

