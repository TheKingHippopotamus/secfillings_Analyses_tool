import os
import json
import sys
import logging
import time


# 🔹 Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

start_time = time.time()




def load_metadata(tags_json_path):
    try:
        if not os.path.exists(tags_json_path):
            print(f"❌ Metadata file not found at {tags_json_path}")
            sys.exit(1)
    except Exception as e:
        logger.exception(f"Error loading metadata: {e}")
        raise
    
    with open(tags_json_path, "r", encoding="utf-8") as json_file:
        try:
            tags_data = json.load(json_file)
            return tags_data.get("Metadata", {})
        except json.JSONDecodeError as e:
            print(f"❌ JSON Load Error: {e}")
            sys.exit(1)


end_time = time.time()
logger.info(f"🔹 Total execution time of load_metadata: {end_time - start_time} seconds")



