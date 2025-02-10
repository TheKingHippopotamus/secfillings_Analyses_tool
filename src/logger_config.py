import logging
import os

# 🔹 יצירת תיקיית לוגים אם לא קיימת
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# 🔹 נתיב לקובץ הלוגים
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# 🔹 קביעת תצורת הלוגר
logging.basicConfig(
    level=logging.DEBUG,  # ניתן לשנות ל-INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE),  # שמירה לקובץ
        logging.StreamHandler()  # הצגת הודעות במסוף
    ]
)

# 🔹 יצירת משתנה לוגר לשימוש בפרויקטים אחרים
logger = logging.getLogger("sec_filings_logger")
