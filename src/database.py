import sqlite3
import logging
import time
import os



# 🔹 Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

start_time = time.time()

def save_data_to_db(data, db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.executemany("""
        INSERT INTO xbrl_data (company_id, report_type, fiscal_year, tag, regulatory_name, clean_value,
        start_date, end_date, instant, category, sub_category, type, risk_level, usage)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, data)
        conn.commit()
        logger.info(f"🔹 Data saved to database: {db_path}") 
        conn.close()

        end_time = time.time()
        logger.info(f"🔹 Total execution time of save_data_to_db: {end_time - start_time} seconds")

        return data
    except Exception as e:
        logger.exception(f"Error saving data to database: {e}")
        raise   


end_time = time.time()
logger.info(f"🔹 Total execution time of database: {end_time - start_time} seconds")
