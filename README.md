# Mopidy - NFC Scanner

## Installation

```shell
ansible-playbook ansible/playbook_install_project.yml --extra-vars="library_path=/path/to/music" -vvv -K
ansible-playbook ansible/playbook_setup_bluetooth.yml --extra-vars="device_mac=<bluetooth-decive-MAC-address>" -vvv
```

### Enable Serial port

https://raspberrypi.stackexchange.com/a/47958
https://github.com/codebugtools/codebug_tether/issues/17

## Extra configuration

### Connecting to a Bluetooth audio devices from the RPi

http://mygeeks014.blogspot.com/2017/05/audio-streaming-to-bluetooth-speaker.html

### Play Mopidy over pulseaudio

https://docs.mopidy.com/en/release-2.3/service/#configure-pulseaudio

### Static IP address

https://pimylifeup.com/raspberry-pi-static-ip-address/

