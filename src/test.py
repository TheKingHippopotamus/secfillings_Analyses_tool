import sqlite3
import os   
import logging
import time


# 🔹 Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)    

start_time = time.time()    

db_path = 'database.sqlite'  # ודא שהנתיב נכון

# בדוק אם הקובץ קיים    
if not os.path.exists(db_path):
    print(f"Database file does not exist: {db_path}")

# נסה להתחבר למסד הנתונים
try:
    conn = sqlite3.connect(db_path)
    print("Connected to the database successfully.")
except sqlite3.OperationalError as e:
    print(f"An error occurred: {e}")


end_time = time.time()
logger.info(f"🔹 Total execution time of test: {end_time - start_time} seconds")

