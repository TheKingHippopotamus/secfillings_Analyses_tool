import os
import json
import sqlite3
import pandas as pd
import re
from bs4 import BeautifulSoup
from arelle import Cntlr

# 🔹 Initialize Arelle
cntlr = Cntlr.Cntlr()

# 🔹 File Path (יש להזין קובץ XBRL/SEC נכון)
file_path = "/Users/elmaliahmac/Documents/HippoDashBoard/py/0001300514-25-000040.txt"
tags_json_path = "/Users/elmaliahmac/Documents/HippoDashBoard/py/structured_tags.json"
db_path = "/Users/elmaliahmac/Documents/HippoDashBoard/py/xbrl_data.db"
all_tags_csv_path = "/Users/elmaliahmac/Documents/HippoDashBoard/py/all_xbrl_tags.csv"

# 🔹 Load XBRL File
model_xbrl = cntlr.modelManager.load(file_path)

# 🔹 שליפת נתוני חברה (Ticker, CIK, דוח ושנה)
ticker = None
name = None
report_type = None
fiscal_year = None

for fact in model_xbrl.facts:
    tag = fact.concept.qname.localName if fact.concept else fact.qname.localName
    value = fact.value.strip() if fact.value else None

    if tag == "TradingSymbol":  # שליפת Ticker
        name = value
        ticker = value
    elif tag == "DocumentType":  # סוג הדוח (10-K, 10-Q, וכו')
        report_type = value
    elif tag == "DocumentFiscalYearFocus":  # שנת הדוח
        fiscal_year = value
    elif tag == "DocumentPeriodEndDate" and not fiscal_year:  # חלופה אם אין DocumentFiscalYearFocus
        fiscal_year = value[:4]  # שולפים רק את השנה (YYYY-MM-DD → YYYY)

# 🔹 שימוש ב-CIK אם אין Ticker
company_id = ticker if ticker else name if name else "Unknown" 

# 🔹 טיפול במקרה שאין נתונים
if not report_type:
    report_type = "Unknown_Report"
if not fiscal_year:
    fiscal_year = "Unknown_Year"

# 🔹 קובץ CSV ייחודי לכל חברה ודוח
csv_output_path = f"/Users/elmaliahmac/Documents/HippoDashBoard/py/{company_id}_{report_type}_{fiscal_year}.csv"

# 🔹 התחברות למסד הנתונים (ללא מחיקה)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 🔹 יצירת טבלת נתונים עם מזהה חברה ודוח (אם לא קיימת)
cursor.execute("""
CREATE TABLE IF NOT EXISTS xbrl_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id TEXT,
    report_type TEXT,
    fiscal_year TEXT,
    tag TEXT,
    regulatory_name TEXT,
    clean_value TEXT,
    start_date TEXT,
    end_date TEXT,
    instant TEXT,
    category TEXT,
    sub_category TEXT,
    type TEXT,
    risk_level TEXT,
    usage TEXT
);
""")

# 🔹 טעינת מטא-דאטה
with open(tags_json_path, "r", encoding="utf-8") as json_file:
    tags_data = json.load(json_file)

# 🔹 ניקוי HTML מהנתונים
def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    
    for table in soup.find_all("table"):
        table.decompose()
    
    for tag in soup.find_all(["style", "script", "meta", "link"]):
        tag.decompose()
    
    text = soup.get_text(separator="\n")
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    text = re.sub(r'\t+', ' ', text)
    text = re.sub(r' {2,}', ' ', text)
    text = text.strip()

    return text

# 🔹 אחסון נתונים
all_data = []
all_tags = set()

# 🔹 עיבוד הנתונים מהדוח
for fact in model_xbrl.facts:
    tag = fact.concept.qname.localName if fact.concept else fact.qname.localName
    value = fact.value if fact.value else "N/A"
    all_tags.add(tag)

    if "ixTransformValueError" in value:
        value = value.replace("ixTransformValueError", "").strip()

    meta = tags_data.get("Metadata", {}).get(tag, {})

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
    
    clean_value = clean_html(value)
    
    all_data.append((
        company_id,
        report_type,
        fiscal_year,
        tag,
        regulatory_name,
        clean_value,
        start_date,
        end_date,
        instant,
        category,
        sub_category,
        data_type,
        risk_level,
        usage
    ))

# 🔹 שמירת נתונים לקובץ CSV

df_all = pd.DataFrame(all_data, columns=[
    "CompanyID", "ReportType", "FiscalYear", "Tag", "RegulatoryName", "CleanValue",
    "StartDate", "EndDate", "Instant", "Category", "SubCategory", "Type", "RiskLevel", "Usage"
])
df_all.to_csv(csv_output_path, index=False)

# 🔹 שמירת רשימת כל התגים
if os.path.exists(all_tags_csv_path):
    df_existing_tags = pd.read_csv(all_tags_csv_path)
    all_tags.update(df_existing_tags["Tag"].tolist())

df_tags = pd.DataFrame(sorted(all_tags), columns=["Tag"])
df_tags.to_csv(all_tags_csv_path, index=False)

# 🔹 שמירת נתונים למסד נתונים
cursor.executemany("""
INSERT INTO xbrl_data (company_id, report_type, fiscal_year, tag, regulatory_name, clean_value, start_date, end_date, instant, category, sub_category, type, risk_level, usage)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
""", all_data)

conn.commit()
conn.close()

print(f"✅ Data for {company_id} ({report_type} {fiscal_year}) saved to database.")
print(f"✅ Extracted data saved to: {csv_output_path}")
print(f"✅ All tags saved to: {all_tags_csv_path}")
