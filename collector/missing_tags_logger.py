import os
import pandas as pd
from dotenv import load_dotenv

# 🔹 Load environment variables
load_dotenv()
MISSING_TAGS_CSV_PATH = os.getenv("MISSING_TAGS_CSV_PATH")

def save_missing_tags(tag, value):
    """Save tags with missing or unknown values to a persistent CSV file."""
    missing_value_indicators = {"Unknown", "N/A", "NULL", "", None}
    
    # Check if the value is missing or unknown
    if value in missing_value_indicators:
        new_entry = pd.DataFrame([[tag, value]], columns=["Tag", "Value"])
        
        # If the file exists, append data without overwriting
        if os.path.exists(MISSING_TAGS_CSV_PATH):
            existing_data = pd.read_csv(MISSING_TAGS_CSV_PATH)
            updated_data = pd.concat([existing_data, new_entry], ignore_index=True).drop_duplicates()
        else:
            updated_data = new_entry
        
        # Save the updated data
        updated_data.to_csv(MISSING_TAGS_CSV_PATH, index=False)

        print(f"🔹 Tag '{tag}' with missing value saved to: {MISSING_TAGS_CSV_PATH}")
