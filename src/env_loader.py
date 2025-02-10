import os
from dotenv import load_dotenv

def load_environment_variables():
    load_dotenv()
    return {
        "file_path": os.getenv("FILE_PATH"),
        "tags_json_path": os.getenv("TAGS_JSON_PATH"),
        "db_path": os.getenv("DB_PATH"),
        "all_tags_csv_path": os.getenv("ALL_TAGS_CSV_PATH"),
        "csv_output_dir": os.getenv("CSV_OUTPUT_DIR"),
    }
