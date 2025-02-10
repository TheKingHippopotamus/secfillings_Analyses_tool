import sqlite3
import os

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