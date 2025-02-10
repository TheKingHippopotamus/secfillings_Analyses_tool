import sqlite3

def save_data_to_db(data, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executemany("""
    INSERT INTO xbrl_data (company_id, report_type, fiscal_year, tag, regulatory_name, clean_value,
    start_date, end_date, instant, category, sub_category, type, risk_level, usage)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, data)
    conn.commit()
    conn.close()
