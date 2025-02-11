import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime 
import logging
import sys
import time 


start_time = time.time()





# 🔹 Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

# 🔹 Load environment variables
load_dotenv()
MISSING_TAGS_CSV_PATH = os.getenv("MISSING_TAGS_CSV_PATH")


# 🔹 Check if the CSV file exists
if not os.path.exists(MISSING_TAGS_CSV_PATH):
    logger.info(f"🔹 Creating new CSV file at: {MISSING_TAGS_CSV_PATH}")
    pd.DataFrame(columns=["Tag", "Value", "Timestamp"]).to_csv(MISSING_TAGS_CSV_PATH, index=False)

def save_missing_tags(tag, value):
    """Save tags with missing or unknown values to a persistent CSV file."""
    try:
        missing_value_indicators = {"Unknown", "N/A", "NULL", "", None}
        
        # Check if the value is missing or unknown
        if value in missing_value_indicators:
            new_entry = pd.DataFrame([[tag, value, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]], columns=["Tag", "Value", "Timestamp"])
            
            # If the file exists, append data without overwriting
            if os.path.exists(MISSING_TAGS_CSV_PATH):
                existing_data = pd.read_csv(MISSING_TAGS_CSV_PATH)
                updated_data = pd.concat([existing_data, new_entry], ignore_index=True).drop_duplicates()
            else:
                updated_data = new_entry
            
            # Save the updated data
            updated_data.to_csv(MISSING_TAGS_CSV_PATH, index=False)

    except Exception as e:
        logger.exception(f"Error saving missing tags: {e}")
        logger.info(f"🔹 Tag '{tag}' with missing value saved to: {MISSING_TAGS_CSV_PATH}")



end_time = time.time()
logger.info(f"🔹 Total execution time of missing tags logger: {end_time - start_time} seconds")

    