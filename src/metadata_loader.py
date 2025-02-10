import os
import json
import sys

def load_metadata(tags_json_path):
    if not os.path.exists(tags_json_path):
        print(f"❌ Metadata file not found at {tags_json_path}")
        sys.exit(1)
    
    with open(tags_json_path, "r", encoding="utf-8") as json_file:
        try:
            tags_data = json.load(json_file)
            return tags_data.get("Metadata", {})
        except json.JSONDecodeError as e:
            print(f"❌ JSON Load Error: {e}")
            sys.exit(1)
