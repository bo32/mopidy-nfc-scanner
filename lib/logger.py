from pathlib import Path

import logging

def get_logger(name, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    log_folder_path = Path('./log')
    if not log_folder_path.is_dir():
        log_folder_path.mkdir(parents=True)        

    ch = logging.FileHandler(str(log_folder_path / 'nfc_scanner.log'))
    ch.setLevel(level)

    formatter = logging.Formatter('[%(asctime)s][%(levelname).4s][%(name)s] %(message)s')
    ch.setFormatter(formatter)
    
    logger.addHandler(ch)
    return logger