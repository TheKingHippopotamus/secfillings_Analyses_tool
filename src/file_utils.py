import os
import re
import logging
import time

# 🔹 Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

start_time = time.time()

def ensure_directory_exists(directory):
    try:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"🔹 Directory ensured: {directory}")
    except Exception as e:
        logger.exception(f"Error ensuring directory: {e}")
        raise


def clean_filename(name):
    try:
        return re.sub(r'[^A-Za-z0-9_-]', '_', name).strip('_')
    except Exception as e:
        logger.exception(f"Error cleaning filename: {e}")
        raise


end_time = time.time()
logger.info(f"🔹 Total execution time of file_utils: {end_time - start_time} seconds")




