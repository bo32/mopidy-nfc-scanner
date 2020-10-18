from mopidy_nfc_scanner import MopidyNfcScanner
from mopidy_http_service import MopidyHttpService

# httpService = MopidyHttpService('http://filip.local:6680/mopidy/rpc')
httpService = MopidyHttpService('http://localhost:6680/mopidy/rpc')
#FIXME handle scanning errors !!!
nfcScanner = MopidyNfcScanner(handler=httpService)
nfcScanner.start_scanning()

