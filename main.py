import logging 

from mopidy_nfc_scanner import MopidyNfcScanner
from mopidy_http_service import MopidyHttpService
import logger

def main():
    LOGGER = logger.get_logger(__name__)
    
    httpService = MopidyHttpService('http://localhost:6680/mopidy/rpc')
    #FIXME handle scanning errors !!!
    nfcScanner = MopidyNfcScanner(handler=httpService)

    LOGGER.info('Starting NFC scanning...')
    nfcScanner.start_scanning()

    LOGGER.info('NFC scanning stopped.')

if __name__ == '__main__':
    main()

