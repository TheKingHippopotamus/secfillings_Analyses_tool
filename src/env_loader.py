import os
from dotenv import load_dotenv
import logging
import time


# 🔹 Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

start_time = time.time()


def load_environment_variables():
    try:
        load_dotenv()
        return {
            "file_path": os.getenv("FILE_PATH"),
            "tags_json_path": os.getenv("TAGS_JSON_PATH"),
            "db_path": os.getenv("DB_PATH"),
            "all_tags_csv_path": os.getenv("ALL_TAGS_CSV_PATH"),
            "csv_output_dir": os.getenv("CSV_OUTPUT_DIR"),
            "missing_tags_csv_path": os.getenv("MISSING_TAGS_CSV_PATH"),
        }
    except Exception as e:
        logger.exception(f"Error loading environment variables: {e}")
        raise
    

end_time = time.time()
logger.info(f"🔹 Total execution time of env_loader: {end_time - start_time} seconds")





