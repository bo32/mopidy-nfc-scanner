# to be scheduled with crontab

from mopidy_http_service import MopidyHttpService
httpService = MopidyHttpService('http://filip.local:6680/mopidy/rpc')

if not httpService.is_playing():
    import os
    os.system('sudo shutdown now')
else:
    print('Mopidy is still playing. Not powering off.')

