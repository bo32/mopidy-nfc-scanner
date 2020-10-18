import requests
import json
        
MOPIDY_BROWSE_LIBRARY = 'core.library.browse'

MOPIDY_TRACKLIST_CLEAR = 'core.tracklist.clear'
MOPIDY_TRACKLIST_ADD = 'core.tracklist.add'
MOPIDY_TRACKLIST_SHUFFLE = 'core.tracklist.shuffle'

MOPIDY_PLAYBACK_PLAY = 'core.playback.play'
MOPIDY_PLAYBACK_STATE = 'core.playback.get_state'
MOPIDY_PLAYBACK_STOP = 'core.playback.stop'

RPC_JSON_BASE = {'jsonrpc': '2.0', 'id': '1'}

class MopidyHttpService:

    def __init__(self, host):
        self.host = host

    def play_value(self, value: str):
        print(value)
        try:
            value_type = int(value[0])
            value_index = int(value[1:])
        except ValueError:
            print('Cannot convert integer value')
            exit(1)

        if value_type == 1:
            self.play_folder_index(value_index)
        elif value_type == 2:
            self.play_youtube_playlist_index(value_index)
        elif value_type == 9:
            self.play_station_index(value_index)
        else:
            print('Cannot process {}'.format(str(value_type)))


    def get_folder_uri_from_index(self, index):
        # with open('mopidy_folders.json') as json_file:
        #     data = json.load(json_file)
        #     for folder in data['items']:
        #         print(folder)
        #         if folder['index'] == index:
        #             return folder['uri']
        # return None
        return self.get_uri_from_index_and_file(index, 'mopidy_folders.json')

    def get_uri_from_index_and_file(self, index, file):
        with open(file) as json_file:
            data = json.load(json_file)
            for folder in data['items']:
                print(folder)
                if folder['index'] == index:
                    return folder['uri']
        return None

    def get_youtube_playlist_uri_from_index(self, index):
        return self.get_uri_from_index_and_file(index, 'mopidy_youtube_playlists.json')
        # with open('mopidy_youtube_playlists.json') as json_file:
        #     data = json.load(json_file)
        #     for folder in data['items']:
        #         print(folder)
        #         if folder['index'] == index:
        #             return folder['uri']
        # return None

    def get_station_uri_from_index(self, index):
        return self.get_uri_from_index_and_file(index, 'mopidy_stations.json')
        # with open('mopidy_stations.json') as json_file:
        #     data = json.load(json_file)
        #     for folder in data['items']:
        #         print(folder)
        #         if folder['index'] == index:
        #             return folder['uri']
        # return None

    def play_station_index(self, index: int):
        uri = self.get_station_uri_from_index(index)
        print('Retrieved URI: {}'.format(uri))
        self.stop_and_clear()
        self.add_uri_to_tracklist(uri)
        self.play()

    def play_folder_index(self, index: int):
        uri = self.get_folder_uri_from_index(index)
        print('Retrieved URI: {}'.format(uri))
        self.play_folder_uri(uri)

    def play_youtube_playlist_index(self, index: int):
        uri = self.get_youtube_playlist_uri_from_index(index)
        print('Retrieved URI: {}'.format(uri))
        self.play_youtube_playlist(uri)

    def stop_and_clear(self):
        requests.post(self.host, json={'jsonrpc': '2.0', 'id': '1', 'method': MOPIDY_PLAYBACK_STOP})
        requests.post(self.host, json={'jsonrpc': '2.0', 'id': '1', 'method': MOPIDY_TRACKLIST_CLEAR})

    def add_uri_to_tracklist(self, uri):
        requests.post(self.host, json={'jsonrpc': '2.0', 'id': '1', 'method': MOPIDY_TRACKLIST_ADD , 'params': {'uris': [uri]}})

    def play_youtube_playlist(self, uri):
        self.stop_and_clear()
        self.add_uri_to_tracklist(uri)
        self.play()
        self.shuffle()

    def play(self):
        requests.post(self.host, json={'jsonrpc': '2.0', 'id': '1', 'method': MOPIDY_PLAYBACK_PLAY})
    
    def shuffle(self):
        requests.post(self.host, json={'jsonrpc': '2.0', 'id': '1', 'method': MOPIDY_TRACKLIST_SHUFFLE})

    

    def play_folder_uri(self, uri: str):
        print('Sending folder content to player...')
        # body = RPC_JSON_BASE['method'] = MOPIDY_BROWSE_LIBRARY
        response = requests.post(self.host, json={'jsonrpc': '2.0', 'id': '1', 'method': MOPIDY_BROWSE_LIBRARY, 'params': {'uri': uri}})
        payload = response.json()

        tracks = json.loads(json.dumps(payload))['result']

        self.stop_and_clear()
        for track in tracks:
            uri = str(track['uri'])
            print('Adding {}...'.format(uri))
            self.add_uri_to_tracklist(uri)
        self.play()
        
    def is_playing(self):
        response = requests.post(self.host, json={'jsonrpc': '2.0', 'id': '1', 'method': MOPIDY_PLAYBACK_STATE})
        payload = response.json()
        return json.loads(json.dumps(payload))['result'] == 'playing'
