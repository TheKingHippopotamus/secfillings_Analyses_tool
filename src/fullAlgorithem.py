import os
import re
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import sqlite3
import pandas as pd
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from arelle import Cntlr
from collector.missing_tags_logger import save_missing_tags


# 🔹 1. טעינת משתני סביבה
def load_environment_variables():
    load_dotenv()
    return {
        "file_path": os.getenv("FILE_PATH"),
        "tags_json_path": os.getenv("TAGS_JSON_PATH"),
        "db_path": os.getenv("DB_PATH"),
        "all_tags_csv_path": os.getenv("ALL_TAGS_CSV_PATH"),
        "csv_output_dir": os.getenv("CSV_OUTPUT_DIR"),  # אין צורך להוסיף "companiesCsv" ידנית
    }


# 🔹 2. פונקציה לניקוי שמות קבצים
def clean_filename(name):
    """Clean filename and replace slashes with underscores"""
    # Replace slashes with underscores to avoid creating subdirectories
    name = name.replace('/', '_').replace('\\', '_')
    return re.sub(r'[^A-Za-z0-9_-]', '_', name).strip('_')


# 🔹 3. טעינת קובץ XBRL
def load_xbrl_file(file_path):
    cntlr = Cntlr.Cntlr()
    return cntlr.modelManager.load(file_path)

def fetch_ticker_from_db():
    """שליפת Ticker מבסיס הנתונים אם נמצא בעבר"""
    conn = sqlite3.connect(os.getenv("DB_PATH"))
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT company_id FROM xbrl_data WHERE company_id != 'Unknown' LIMIT 1")
    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]
    return "Unknown"


def save_ticker_to_db(ticker):
    """שומר את ה-Ticker למסד הנתונים אם עדיין לא קיים"""
    conn = sqlite3.connect(os.getenv("DB_PATH"))
    cursor = conn.cursor()

    # בדיקה אם הטיקר כבר קיים
    cursor.execute("SELECT company_id FROM xbrl_data WHERE company_id = ?", (ticker,))
    existing = cursor.fetchone()

    if not existing and ticker != "Unknown":
        cursor.execute("INSERT INTO xbrl_data (company_id) VALUES (?)", (ticker,))
        conn.commit()
        print(f"✅ Ticker '{ticker}' saved to database.")

    conn.close()
    
def save_data_to_csv(df, output_path):
    try:
        df.to_csv(output_path, index=False)
        print(f"✅ CSV file saved: {output_path}")
    except Exception as e:
        print(f"❌ Error saving CSV: {e}")
        sys.exit(1)

def process_xbrl_data(model_xbrl, company_id, report_type, fiscal_year, metadata):
    all_data = []
    all_tags = set()

    for fact in model_xbrl.facts:
        tag = fact.concept.qname.localName if fact.concept else fact.qname.localName
        value = fact.value if fact.value else "N/A"
        all_tags.add(tag)

        meta = metadata.get(tag, {})

        regulatory_name = meta.get("RegulatoryName", "Unknown")
        category = meta.get("Category", "Unknown")
        sub_category = meta.get("SubCategory", "Unknown")
        data_type = meta.get("Type", "Unknown")
        risk_level = meta.get("RiskLevel", "Unknown")
        usage = ", ".join(meta.get("Usage", ["Unknown"]))

        context = fact.context
        start_date = str(context.startDatetime if context.isStartEndPeriod else "NULL")
        end_date = str(context.endDatetime if context.isStartEndPeriod else "NULL")
        instant = str(context.instantDatetime if context.isInstantPeriod else "NULL")

        clean_value = value

        all_data.append((
            company_id, report_type, fiscal_year, tag, regulatory_name, clean_value,
            start_date, end_date, instant, category, sub_category, data_type, risk_level, usage
        ))

    return all_data, all_tags




def ensure_directory_exists(directory):
    try:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Directory ensured: {directory}")
    except Exception as e:
        print(f"❌ Error creating directory {directory}: {e}")
        sys.exit(1)


def process_xbrl_data(model_xbrl, company_id, report_type, fiscal_year, metadata):
    all_data = []
    all_tags = set()

    for fact in model_xbrl.facts:
        tag = fact.concept.qname.localName if fact.concept else fact.qname.localName
        value = fact.value if fact.value else "N/A"
        all_tags.add(tag)

        meta = metadata.get(tag, {})

        regulatory_name = meta.get("RegulatoryName", "Unknown")
        category = meta.get("Category", "Unknown")
        sub_category = meta.get("SubCategory", "Unknown")
        data_type = meta.get("Type", "Unknown")
        risk_level = meta.get("RiskLevel", "Unknown")
        usage = ", ".join(meta.get("Usage", ["Unknown"]))

        context = fact.context
        start_date = str(context.startDatetime if context.isStartEndPeriod else "NULL")
        end_date = str(context.endDatetime if context.isStartEndPeriod else "NULL")
        instant = str(context.instantDatetime if context.isInstantPeriod else "NULL")

        clean_value = value

        all_data.append((
            company_id, report_type, fiscal_year, tag, regulatory_name, clean_value,
            start_date, end_date, instant, category, sub_category, data_type, risk_level, usage
        ))

    return all_data, all_tags



# 🔹 7. שמירת הנתונים ל-CSV
def save_data_to_csv(df, output_path):
    try:
        df.to_csv(output_path, index=False)
        print(f"✅ CSV file saved: {output_path}")
    except Exception as e:
        print(f"❌ Error saving CSV: {e}")
        sys.exit(1)


# 🔹 8. שמירת הנתונים למסד הנתונים
def save_data_to_db(data, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executemany("""
    INSERT INTO xbrl_data (company_id, report_type, fiscal_year, tag, regulatory_name, clean_value, start_date, end_date, instant, category, sub_category, type, risk_level, usage)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, data)
    conn.commit()
    conn.close()


# 🔹 9. שמירת תגים חסרים
def save_missing_tags_to_csv(model_xbrl):
    for fact in model_xbrl.facts:
        tag = fact.concept.qname.localName if fact.concept else fact.qname.localName
        value = fact.value.strip() if fact.value else "N/A"
        save_missing_tags(tag, value)
# 🔹 פונקציה לטעינת נתוני המטא-דאטה מה-JSON
def load_metadata(tags_json_path):
    """טוען את קובץ ה-JSON שמכיל מידע על המטא-דאטה של התגים"""
    if not os.path.exists(tags_json_path):
        print(f"❌ Error: Metadata file not found at {tags_json_path}")
        sys.exit(1)
    
    with open(tags_json_path, "r", encoding="utf-8") as json_file:
        try:
            tags_data = json.load(json_file)
            return tags_data.get("Metadata", {})  # מחזיר רק את חלק ה-Metadata
        except json.JSONDecodeError as e:
            print(f"❌ JSON Load Error: {e}")
            sys.exit(1)


def extract_metadata(model_xbrl, metadata):
    """Extracts company ID, report type, and fiscal year from the XBRL model."""
    company_id = "Unknown"
    report_type = "Unknown_Report"
    fiscal_year = "Unknown_Year"

    for fact in model_xbrl.facts:
        tag = fact.concept.qname.localName if fact.concept else fact.qname.localName
        value = fact.value.strip() if fact.value else "N/A"

        if tag == "TradingSymbol" and company_id == "Unknown":
            company_id = value
        elif tag == "DocumentType" and report_type == "Unknown_Report":
            report_type = value
        elif tag == "DocumentFiscalYearFocus" and fiscal_year == "Unknown_Year":
            fiscal_year = value[:4] if len(value) >= 4 else value
        elif tag == "DocumentPeriodEndDate" and fiscal_year == "Unknown_Year":
            fiscal_year = value[:4]  # Extract year from date

    return company_id, report_type, fiscal_year


def main():
    env_vars = load_environment_variables()
    metadata = load_metadata(env_vars["tags_json_path"])
    model_xbrl = load_xbrl_file(env_vars["file_path"])

    company_id, report_type, fiscal_year = extract_metadata(model_xbrl, metadata)
    
    # Clean all components of the filename
    safe_company_id = clean_filename(company_id)
    safe_report_type = clean_filename(report_type)
    safe_fiscal_year = clean_filename(fiscal_year)
    
    # Create filename without subdirectories
    filename = f"{safe_company_id}_{safe_report_type}_{safe_fiscal_year}.csv"
    
    csv_dir = env_vars["csv_output_dir"]
    ensure_directory_exists(csv_dir)
    
    # Create full path using os.path.join
    csv_output_path = os.path.join(csv_dir, filename)

    print(f"✅ CSV will be saved as: {csv_output_path}")

    # עיבוד הנתונים כולל מטא-דאטה
    all_data, all_tags = process_xbrl_data(model_xbrl, company_id, report_type, fiscal_year, metadata)

    # שמירת הנתונים לקובץ CSV
    df_all = pd.DataFrame(all_data, columns=[
        "CompanyID", "ReportType", "FiscalYear", "Tag", "RegulatoryName", "CleanValue",
        "StartDate", "EndDate", "Instant", "Category", "SubCategory", "Type", "RiskLevel", "Usage"
    ])
    save_data_to_csv(df_all, csv_output_path)

    # שמירת הנתונים למסד נתונים
    save_data_to_db(all_data, env_vars["db_path"])

    # שמירת תגים חסרים
    save_missing_tags_to_csv(model_xbrl)

    print(f"✅ Data for {company_id} ({report_type} {fiscal_year}) saved to database.")




# 🔹 הפעלת הקובץ הראשי
if __name__ == "__main__":
    main()
