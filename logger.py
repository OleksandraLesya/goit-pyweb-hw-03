# logger.py

import logging

logger = logging.getLogger("shared_logger")
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(threadName)s | %(processName)s | %(message)s')

if not logger.hasHandlers():
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
