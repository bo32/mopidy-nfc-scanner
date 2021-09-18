import json
import sys
from pathlib import Path

from lib import logger

def main():
    LOGGER = logger.get_logger(__name__)

    library_folder_path = sys.argv[1]

    if library_folder_path.endswith('/'):
        library_folder_path = library_folder_path[:-1]

    library_folder = Path(library_folder_path)

    data = {}
    data['music_folder'] = library_folder_path
    data['items'] = []
    for i, folder in enumerate(library_folder.glob('*')):
        data['items'].append({
            'index': i,
            'uri': folder.as_uri().replace(library_folder_path, '[music_folder]')
        })

    target_filepath = 'mopidy_folders.json'
    with open(target_filepath, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
    main()

