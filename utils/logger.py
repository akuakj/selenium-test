import logging
import os
from datetime import datetime

DIR_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_log_dir = f"{DIR_PATH}/logs"
os.makedirs(_log_dir, exist_ok=True)

_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
_log_file = os.path.join(_log_dir, f"test_run_{_timestamp}.log")

_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger



    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(_log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger