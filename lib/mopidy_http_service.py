import requests
import json

from lib import logger
        
MOPIDY_BROWSE_LIBRARY = 'core.library.browse'

MOPIDY_TRACKLIST_CLEAR = 'core.tracklist.clear'
MOPIDY_TRACKLIST_ADD = 'core.tracklist.add'
MOPIDY_TRACKLIST_SHUFFLE = 'core.tracklist.shuffle'

MOPIDY_PLAYBACK_PLAY = 'core.playback.play'
MOPIDY_PLAYBACK_PAUSE = 'core.playback.pause'
MOPIDY_PLAYBACK_RESUME = 'core.playback.resume'
MOPIDY_PLAYBACK_STOP = 'core.playback.stop'
MOPIDY_PLAYBACK_STATE = 'core.playback.get_state'

RPC_JSON_BASE = {'jsonrpc': '2.0', 'id': '1'}

LOGGER = logger.get_logger(__name__)

class MopidyHttpService:

    def __init__(self, host):
        self.host = host
        self.currently_playing = None

    def play_value(self, value: str):
        LOGGER.info(value)
        try:
            value_type = int(value[0])
            value_index = int(value[1:])
        except ValueError:
            LOGGER.warn('Cannot convert integer value')
            return

        if self.currently_playing == value:
            if self.is_playing():
                self.pause()
            elif self.is_paused():
                self.resume()
            return

        if value_type == 1:
            self.play_folder_index(value_index)
        elif value_type == 2:
            self.play_youtube_playlist_index(value_index)
        elif value_type == 9:
            self.play_station_index(value_index)
        else:
            LOGGER.warn('Cannot process {}'.format(str(value_type)))
        
        self.currently_playing = value


    def get_folder_uri_from_index(self, index):
        return self.get_uri_from_index_and_file(index, 'mopidy_folders.json')

    def get_uri_from_index_and_file(self, index, file):
        with open(file) as json_file:
            data = json.load(json_file)
            for folder in data['items']:
                LOGGER.info(folder)
                if folder['index'] == index:
                    return folder['uri']
        return None

    def get_music_folder_value_from_folders_file(self):
        with open('mopidy_folders.json') as json_file:
            data = json.load(json_file)
            return data['music_folder']

    def get_youtube_playlist_uri_from_index(self, index):
        return self.get_uri_from_index_and_file(index, 'mopidy_youtube_playlists.json')

    def get_station_uri_from_index(self, index):
        return self.get_uri_from_index_and_file(index, 'mopidy_stations.json')

    def play_station_index(self, index: int):
        uri = self.get_station_uri_from_index(index)
        LOGGER.info('Retrieved URI: {}'.format(uri))
        self.stop_and_clear()
        self.add_uri_to_tracklist(uri)
        self.play()

    def play_folder_index(self, index: int):
        uri = self.get_folder_uri_from_index(index)
        LOGGER.info('Retrieved URI: {}'.format(uri))
        self.play_folder_uri(uri)

    def play_youtube_playlist_index(self, index: int):
        uri = self.get_youtube_playlist_uri_from_index(index)
        LOGGER.info('Retrieved URI: {}'.format(uri))
        self.play_youtube_playlist(uri)

    def add_uri_to_tracklist(self, uri):
        self.send_modipy_rpc_request(MOPIDY_TRACKLIST_ADD, {'uris': [uri]})

    def play_youtube_playlist(self, uri):
        self.stop_and_clear()
        self.add_uri_to_tracklist(uri)
        self.play()
        self.shuffle()

    def play(self):
        LOGGER.info('PLAY')
        self.send_modipy_rpc_request(MOPIDY_PLAYBACK_PLAY)

    def resume(self):
        LOGGER.info('RESUME')
        self.send_modipy_rpc_request(MOPIDY_PLAYBACK_RESUME)
    
    def pause(self):
        LOGGER.info('PAUSE')
        self.send_modipy_rpc_request(MOPIDY_PLAYBACK_PAUSE)
    
    def shuffle(self):
        LOGGER.info('SHUFFLE')
        self.send_modipy_rpc_request(MOPIDY_TRACKLIST_SHUFFLE)

    def stop(self):
        LOGGER.info('STOP')
        self.send_modipy_rpc_request(MOPIDY_PLAYBACK_STOP)
    
    def clear(self):
        LOGGER.info('CLEAR TRACK LIST')
        self.send_modipy_rpc_request(MOPIDY_TRACKLIST_CLEAR)

    def stop_and_clear(self):
        self.stop()
        self.clear()

    def send_modipy_rpc_request(self, method: str, params=None):
        json = {'jsonrpc': '2.0', 'id': '1', 'method': method}
        if not params is None:
            json['params'] = params
        return requests.post(self.host, json=json)

    def play_folder_uri(self, uri: str):
        LOGGER.info('Sending folder content to player...')
        # response = requests.post(self.host, json={'jsonrpc': '2.0', 'id': '1', 'method': MOPIDY_BROWSE_LIBRARY, 'params': {'uri': uri}})
        response = self.send_modipy_rpc_request(MOPIDY_BROWSE_LIBRARY, {'uri': uri})
        payload = response.json()

        tracks = json.loads(json.dumps(payload))['result']
        if not tracks:
            LOGGER.warn('No tracks retrieved.')
            return

        self.stop_and_clear()
        is_first = True # Used to start playing as soon as the first track is added
        for track in tracks:
            uri = str(track['uri'])

            music_folder_placeholder = '[music_folder]'
            if music_folder_placeholder in uri:
                music_folder_value = self.get_music_folder_value_from_folders_file()
                uri = uri.replace(music_folder_placeholder, music_folder_value)

            LOGGER.info('Adding {}...'.format(uri))
            self.add_uri_to_tracklist(uri)
            if is_first:
                self.play()
                is_first = False
        
    def is_playing(self):
        return self.get_state() == 'playing'

    def is_paused(self):
        return self.get_state() == 'paused'

    def get_state(self):
        # response = requests.post(self.host, json={'jsonrpc': '2.0', 'id': '1', 'method': MOPIDY_PLAYBACK_STATE})
        response = self.send_modipy_rpc_request(MOPIDY_PLAYBACK_STATE)
        payload = response.json()
        return json.loads(json.dumps(payload))['result']

    
