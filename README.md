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

# Arelle Installation & Troubleshooting Guide

## Overview
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

