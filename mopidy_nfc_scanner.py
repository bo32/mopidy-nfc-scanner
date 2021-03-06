import RPi.GPIO as GPIO

import lib.pn532.pn532 as nfc
from lib.pn532.uart import *

import time
TIME_FREQUENCY=2 # seconds

class MopidyNfcScanner:

    def __init__(self, handler):
        self.pn532 = PN532_UART(debug=False, reset=20)

        ic, ver, rev, support = self.pn532.get_firmware_version()
        print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

        # Configure PN532 to communicate with NTAG215 cards
        self.pn532.SAM_configuration()

        self.handler = handler

    def start_scanning(self):
        while True:
            # Check if a card is available to read
            uid = self.pn532.read_passive_target(timeout=0.5)
            # print('.', end="")
            # Try again if no card is available.
            if uid is not None:
                print('Found card with UID:', [hex(i) for i in uid])
                try:
                    self.read_value()
                except RuntimeError as e:
                    print('Exception occured when scanning NFC tag. Please try again.')
                    print(e.strerror)

                print('waiting for {} seconds before next scan...'.format(TIME_FREQUENCY))
                
                time.sleep(TIME_FREQUENCY)  

    def read_value(self):
        result = ''
        end_of_nfc_value = False # We loop until we reach the end of NFC value (00)
        # Here we start reading NFC value from 6, as the beginning is not related to the stored value
        for i in range(6, 135):
            try:
                for x in self.pn532.ntag2xx_read_block(i):
                    if x == 0x00:
                        end_of_nfc_value = True
                        break
                    result = result + ('%02X' % x) + ' '
            except nfc.PN532Error as e:
                print(e.errmsg)
                break  
            if end_of_nfc_value is True:
                break
        print('Encoded result: {}'.format(result))
        raw_result = bytes.fromhex(result).decode("latin-1")
        print('Decoded result: {}'.format(raw_result))
        self.process_value(raw_result)

    def process_value(self, decoded_value):
        if len(decoded_value) == 3 and decoded_value.isnumeric():
            self.handler.play_value(decoded_value)
        else:
            print('Wrong value scanned. Value must be a number of 3 digits. Please try again.')

