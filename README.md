# Mopidy - NFC Scanner

## Installation

```shell
ansible-playbook ansible/playbook_install_project.yml --extra-vars="ansible_become_password=<become-password>" -vvv # FIXME the password should not be set via CLI
ansible-playbook ansible/playbook_setup_bluetooth.yml --extra-vars="device_mac=<bluetooth-decive-MAC-address>" -vvv
```

### Enable Serial port

https://raspberrypi.stackexchange.com/a/47958
https://github.com/codebugtools/codebug_tether/issues/17

## Extra configuration

### Connecting to a Bluetooth audio devices from the RPi

http://mygeeks014.blogspot.com/2017/05/audio-streaming-to-bluetooth-speaker.html

### Static IP address

https://pimylifeup.com/raspberry-pi-static-ip-address/

