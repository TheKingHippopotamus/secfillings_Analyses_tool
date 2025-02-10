# **SEC Filings Analysis Tool**

## **📌 Overview**
The **SEC Filings Analysis Tool** is an automated system for extracting and analyzing **XBRL filings** from the **U.S. Securities and Exchange Commission (SEC)**. This tool leverages **Arelle** for XBRL parsing, stores structured financial data in a **SQLite database**, and exports results to **CSV format** for further analysis.

---
## **🛠 Features**
✔ **Automated Parsing** – Extracts key financial data from SEC filings.
✔ **Database Storage** – Saves extracted data into a structured SQLite database.
✔ **CSV Export** – Generates structured CSV reports for easy data analysis.
✔ **Advanced Logging** – Uses a professional logging system.
✔ **Data Cleaning** – Removes unnecessary HTML and transforms raw XBRL data.
✔ **Tag Mapping** – Uses structured JSON files for metadata reference.
✔ **Flexible Ticker Extraction** – Extracts ticker from multiple sources (XBRL, database, etc.).

---
## **📥 Installation**
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/TheKingHippopotamus/secfillings_Analyses_tool.git
cd secfillings_Analyses_tool
```
### **2️⃣ Install Dependencies**
Ensure Python is installed, then run:
```sh
pip install -r requirements.txt
```

---
## **📂 File Structure**
```
secfillings_Analyses_tool/
│── src/
│   ├── main.py                 # Main script
│   ├── process_xbrl.py         # XBRL data extraction logic
│   ├── ticker_lookup.py        # Fetch ticker from XBRL or DB
│   ├── metadata_loader.py      # Loads metadata from JSON
│   ├── database.py             # Handles SQLite database operations
│   ├── env_loader.py           # Loads environment variables
│   ├── logger_config.py        # Logger configuration
│   ├── file_utils.py           # File handling utilities
│── data/
│   ├── awaiting_secFiles/      # Unprocessed SEC XBRL files
│   ├── database/xbrl_data.db   # SQLite database file
│   ├── csvDatabase/            # Generated CSV reports
│   ├── helpers/json/           # Metadata JSON files
│── logs/
│   ├── app.log                 # Application log file
│── README.md                   # Project documentation
```

---
## **🚀 Usage**
### **Run the SEC Filings Processor**
```sh
python src/main.py
```

### **How It Works:**
1️⃣ Parses an XBRL file.
2️⃣ Extracts metadata (**Ticker, Report Type, Fiscal Year**).
3️⃣ Stores structured financial data in `xbrl_data.db` (SQLite).
4️⃣ Generates CSV reports in `data/csvDatabase/`.
5️⃣ Logs processing details in `logs/app.log`.

---
## **⚙ Configuration**
Update your **`.env` file** (or `env_loader.py`) with the correct paths:
```sh
FILE_PATH=/absolute/path/to/your/SEC_filing.txt
DB_PATH=/absolute/path/to/xbrl_data.db
TAGS_JSON_PATH=/absolute/path/to/structured_tags.json
CSV_OUTPUT_DIR=/absolute/path/to/csvDatabase/
MISSING_TAGS_CSV_PATH=/absolute/path/to/missing_xbrl_tags.csv
```

---
## **📝 Data Fields**
### **Extracted Information**
- **CompanyID** (*Ticker or CIK*)
- **ReportType** (*10-K, 10-Q, etc.*)
- **FiscalYear** (*Report Year*)
- **Tag** (*XBRL Tag Name*)
- **RegulatoryName** (*Mapped from JSON metadata*)
- **CleanValue** (*Processed Financial Value*)
- **StartDate / EndDate / Instant** (*Context Period*)
- **Category / SubCategory** (*Financial Classification*)
- **RiskLevel** (*Risk Rating*)

### **📊 Example CSV Output**
```
CompanyID, ReportType, FiscalYear, Tag, RegulatoryName, CleanValue, StartDate, EndDate, Instant, Category
AAPL, 10-K, 2024, Revenue, Net Sales, 394.3B, 2024-01-01, 2024-12-31, NULL, Financials
```

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
## **📊 Logging System**
✔ **Logs are saved to `logs/app.log`** for easy debugging.
✔ **Logging levels:** `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
✔ **Example log entry:**
```
2025-02-09 10:30:15 - INFO - ticker_lookup.py - fetch_ticker_from_db - Fetched ticker from DB: AAPL
```

---
## **📩 Contributing**
Want to improve this tool? Feel free to submit pull requests or open issues!

---
## **📜 License**
MIT License © TheKingHippopotamus






-------------------------------------------------------------------------------                                                     
## **🔹 Arelle Installation & Troubleshooting Guide** 

## **Overview**
Arelle is an open-source XBRL processor that helps parse and analyze XBRL filings. However, installing and running Arelle can sometimes be tricky due to compatibility issues with Python versions and dependencies.

This guide provides a comprehensive overview of:
- Supported Python versions
- Common installation issues
- Fixes for dependency conflicts
- Best practices for setting up Arelle

---

## 📌 Supported Python Versions

Arelle **does not work reliably with Python 3.10+**. The recommended versions are:
- ✅ **Python 3.7 - 3.9** (Fully compatible)
- ⚠️ **Python 3.10+** (Requires manual fixes for certain dependencies)

If you are using Python 3.10 or later and encountering issues, consider downgrading to Python 3.9.

---

## 🔹 Installation Instructions
### ✅ **Standard Installation (Python 3.7 - 3.9)**
```bash
pip install arelle
```
For **Mac/Linux**, you may need to use:
```bash
pip install arelle[web]
```

### ✅ **Alternative Installation with `arelle-release`**
If the default `arelle` package does not work, try using the **release version**:
```bash
pip install arelle-release
```

### ✅ **Installation in a Virtual Environment**
To avoid conflicts, it is recommended to create a virtual environment:
```bash
python3 -m venv arelle_env
source arelle_env/bin/activate  # Mac/Linux
arelle_env\Scripts\activate  # Windows
pip install arelle
```

---

## 🚨 Common Issues & Fixes
### **1. `ModuleNotFoundError: No module named 'arelle'`**
#### ✅ Solution:
- Ensure you are in the correct virtual environment:
  ```bash
  source arelle_env/bin/activate  # Mac/Linux
  arelle_env\Scripts\activate  # Windows
  ```
- Reinstall Arelle:
  ```bash
  pip uninstall arelle
  pip install arelle
  ```

---

### **2. `AttributeError: module 'collections' has no attribute 'MutableMapping'`**
#### ❌ Issue:
- Arelle uses `collections.MutableMapping`, which was removed in Python 3.10.
#### ✅ Solution:
- Downgrade to Python 3.9:
  ```bash
  pyenv install 3.9.18  # Install Python 3.9
  pyenv local 3.9.18    # Set Python 3.9 as the local version
  ```
- Alternatively, manually edit the affected file (`pyparsing_py3.py`):
  ```python
  from collections.abc import MutableMapping
  MutableMapping.register(ParseResults)
  ```

---

### **3. `ImportError: cannot import name 'MutableSet'`**
#### ❌ Issue:
- `collections.MutableSet` was removed in Python 3.10.
#### ✅ Solution:
- Edit `PythonUtil.py` and replace:
  ```python
  from collections import MutableSet
  ```
  **With:**
  ```python
  from collections.abc import MutableSet
  ```

---

### **4. `collections.MutableMapping.register(ParseResults)` Error**
#### ❌ Issue:
- Some Arelle components still use old-style `MutableMapping` calls.
#### ✅ Solution:
- Edit `pyparsing_py3.py` and replace:
  ```python
  collections.MutableMapping.register(ParseResults)
  ```
  **With:**
  ```python
  from collections.abc import MutableMapping
  MutableMapping.register(ParseResults)
  ```

---

## 🔹 Best Practices
1. **Use Python 3.9** for best compatibility.
2. **Always use a virtual environment** to prevent dependency conflicts.
3. **Check dependencies manually** using:
   ```bash
   pip list | grep arelle
   ```
4. **Update dependencies only when necessary**, as updates may break Arelle compatibility.
5. **If using Python 3.10+, manually fix the imports** (`MutableMapping`, `MutableSet`).

---

## 📌 Final Checks
After installation, verify that Arelle is correctly installed:
```bash
python -c "import arelle; print('✅ Arelle installed successfully!')"
```
If this runs without errors, Arelle is correctly installed.

🚀 **Now you’re ready to use Arelle!** 🚀

