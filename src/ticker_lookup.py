import os
import sqlite3
from logger_config import logger 
import logging
import time


# 🔹 Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

start_time = time.time()

def fetch_ticker_from_db():
    
    db_path = os.getenv("DB_PATH")
    if not db_path:
        logger.error("DB_PATH is not set in environment variables")
        raise ValueError("DB_PATH is not set")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT DISTINCT company_id FROM xbrl_data WHERE company_id != 'Unknown' LIMIT 1")
        row = cursor.fetchone()
        ticker = row[0] if row else "Unknown"
        logger.info(f"Fetched ticker from DB: {ticker}")
        return ticker
    except Exception as e:
        logger.exception("Failed to fetch ticker from DB")
    finally:
        conn.close()

def save_ticker_to_db(ticker):
    """שומר את ה-Ticker למסד הנתונים אם עדיין לא קיים"""
    db_path = os.getenv("DB_PATH")
    if not db_path:
        logger.error("DB_PATH is not set in environment variables")
        raise ValueError("DB_PATH is not set")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT company_id FROM xbrl_data WHERE company_id = ?", (ticker,))
        existing = cursor.fetchone()

        if not existing and ticker != "Unknown":
            cursor.execute("INSERT INTO xbrl_data (company_id) VALUES (?)", (ticker,))
            conn.commit()
            logger.info(f"✅ Ticker '{ticker}' saved to database.")
    except Exception as e:
        logger.exception(f"Error saving ticker '{ticker}' to DB")
    finally:
        conn.close()
        

end_time = time.time()
logger.info(f"🔹 Total execution time of save_ticker_to_db: {end_time - start_time} seconds")

