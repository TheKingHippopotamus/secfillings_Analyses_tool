import os
import time
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get path for JSON file
path_for_save_txt_links = os.getenv("PATH_FOR_SAVE_TXT_LINKS")
if path_for_save_txt_links is None:
    raise ValueError("PATH_FOR_SAVE_TXT_LINKS environment variable is not set")

print(f"Watching for changes in: {path_for_save_txt_links}")

# Function to read and print JSON file
def print_json_file():
    try:
        with open(path_for_save_txt_links, "r") as f:
            data = json.load(f)
            print(json.dumps(data, indent=4))
    except (json.JSONDecodeError, FileNotFoundError):
        print("No valid JSON file found or file is empty.")

# Monitor file changes
last_modified = None
while True:
    if os.path.exists(path_for_save_txt_links):
        current_modified = os.path.getmtime(path_for_save_txt_links)
        if last_modified is None or current_modified > last_modified:
            print("🔹 JSON file updated. Printing contents:")
            print_json_file()
            last_modified = current_modified
    time.sleep(2)  # Check every 2 seconds
