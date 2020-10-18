WORKING_DIR=~
mkdir -p ${WORKING_DIR}
cd ${WORKING_DIR}

# Apt
wget -q -O - https://apt.mopidy.com/mopidy.gpg | sudo apt-key add -
sudo wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/buster.list
sudo apt install git mopidy python3-pip
sudo apt clean

# Clone Git Repo

# Python
python3 -m pip install -r requirements.txt

# Mopidy plugins
python3 -m pip install Mopidy-Iris Mopidy-Mobile Mopidy-YouTube Mopidy-API-Explorer --user

# Enable Serial
#raspi-config nonint do_serial 1  # disable serial console
raspi-config nonint do_serial 0  # enable serial console

# Enable services
sudo cp nfc_scanner.service /etc/systemd/system/nfc_scanner.service \
    && sudo systemctl enable nfc_scanner.service
sudo cp mopidy.service /etc/systemd/system/mopidy.service \
    && sudo systemctl enable mopidy.service

# Nginx