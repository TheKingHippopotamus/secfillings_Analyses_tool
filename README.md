# **SEC Filings Analysis Tool**

## **📌 Overview**
This tool extracts and processes financial data from **SEC XBRL filings**. It utilizes **Arelle** to parse the XBRL files, stores extracted data in a SQLite database, and saves structured information in CSV format.

---
## **🛠 Features**
✔ **Automated Parsing** – Extract key financial data from SEC filings.
✔ **Database Storage** – Save extracted data into a structured SQLite database.
✔ **CSV Export** – Generate organized CSV reports for further analysis.
✔ **HTML Data Cleaning** – Remove unnecessary HTML from financial text.
✔ **Tag Mapping** – Uses a structured JSON file for metadata reference.

---
## **📥 Installation**
### **1️⃣ Clone the Repository**
```sh
 git clone https://github.com/TheKingHippopotamus/secfillings_Analyses_tool.git
 cd secfillings_Analyses_tool
```
### **2️⃣ Install Dependencies**
Make sure Python is installed, then install the required libraries:
```sh
pip install pandas beautifulsoup4 arelle
```

---
## **📂 File Structure**
```
secfillings_Analyses_tool/
│── app.py                 # Main script
│── structured_tags.json    # Metadata for XBRL tags
│── all_xbrl_tags.csv       # List of extracted XBRL tags
│── tags.json               # Additional tag mapping
│── test.py                 # Test script
│── README.md               # Project documentation
```

---
## **🚀 Usage**
Run the main script to process an XBRL file:
```sh
python app.py
```

The script will:
1. Parse the XBRL file.
2. Extract metadata (Ticker, Report Type, Fiscal Year).
3. Store data in `xbrl_data.db` (SQLite).
4. Save results to a structured CSV file.

---
## **⚙ Configuration**
Update `app.py` to point to the correct **XBRL file path** before running:
```python
file_path = "/path/to/your/SEC_filing.txt"
db_path = "/path/to/xbrl_data.db"
tags_json_path = "/path/to/structured_tags.json"
```

---
## **📝 Data Fields**
The extracted data includes:
- **CompanyID** (Ticker or CIK)
- **ReportType** (10-K, 10-Q, etc.)
- **FiscalYear** (Year of report)
- **Tag** (XBRL tag name)
- **RegulatoryName** (Mapped from JSON metadata)
- **CleanValue** (Processed value)
- **StartDate / EndDate / Instant** (Context period)
- **Category / SubCategory** (Financial classification)
- **RiskLevel** (Risk rating)

---
## **🛠 Database Schema (SQLite)**
```sql
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
```

---
## **📊 Example Output**
Example of extracted financial data:
```
CompanyID, ReportType, FiscalYear, Tag, RegulatoryName, CleanValue, StartDate, EndDate, Instant, Category
AAPL, 10-K, 2024, Revenue, Net Sales, 394.3B, 2024-01-01, 2024-12-31, NULL, Financials
```

---
## **📌 Notes**
- Ensure that the **XBRL file path** is correctly set.
- The script assumes an **XBRL file format** as used by the SEC.
- Some fields may require additional processing for better analysis.

---
## **📩 Contributing**
Feel free to submit pull requests or open issues to improve the tool!

---
## **📜 License**
MIT License © TheKingHippopotamus

