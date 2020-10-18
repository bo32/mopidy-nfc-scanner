import sys

if not len(sys.argv) == 2:
    print('One argument only required for this script !')
    exit(1)

mystring=str(sys.argv[1])
print("Going to insert value '{}'...".format(mystring))

"""
This example shows connecting to the PN532 and writing an NTAG215
type RFID tag
"""
import RPi.GPIO as GPIO

import lib.pn532.pn532 as nfc

from lib.pn532.uart import *

# pn532 = PN532_SPI(debug=False, reset=20, cs=4)
# pn532 = PN532_I2C(debug=False, reset=20, req=16)
pn532 = PN532_UART(debug=False, reset=20)

ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

# Configure PN532 to communicate with NTAG215 cards
pn532.SAM_configuration()

print('Waiting for RFID/NFC card to write to!')
while True:
    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=0.5)
    print('.', end="")
    # Try again if no card is available.
    if uid is not None:
        break

print(uid)
print('Found card with UID:', [hex(i) for i in uid])

# Write block #6
block_number = 6


# data = bytes([0x00, 0x01, 0x02, 0x03])
# print(data)
# # data = b'73616c7574206461766964'

# try:
#     print('storing data...')
#     pn532.ntag2xx_write_block(block_number, data)
#     # if pn532.ntag2xx_read_block(block_number) == data:
#     #     print('write block %d successfully' % block_number)
# except nfc.PN532Error as e:
#     print(e.errmsg)

# exit()

encoded = []
for index, letter in enumerate(mystring):
    # print(str(index))
    letter_byte = int('0x' + letter.encode(encoding='utf8').hex(), 16)
    print(letter)
    encoded.append(letter_byte)

    if index % 4 == 3:
        try:
            print('storing data...')
            print(encoded)
            data = bytes(encoded)
            print(data)
            pn532.ntag2xx_write_block(block_number, encoded)
            encoded = []
            block_number = block_number + 1
            # if pn532.ntag2xx_read_block(block_number) == data:
            #     print('write block %d successfully' % block_number)
        except nfc.PN532Error as e:
            print(e.errmsg)
    
if not len(encoded) == 0:
    while len(encoded) < 4:
        encoded.append(0x00)
    data = bytes(encoded)
    pn532.ntag2xx_write_block(block_number, data)


GPIO.cleanup()
