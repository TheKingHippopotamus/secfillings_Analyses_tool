from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging
import json 
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.env_loader import load_environment_variables
from src.file_utils import ensure_directory_exists
from src.logger_config import logger

# Load environment variables
load_dotenv()

# Get path and validate
path_for_save_txt_links = os.getenv("PATH_FOR_SAVE_TXT_LINKS")
if path_for_save_txt_links is None:
    raise ValueError("PATH_FOR_SAVE_TXT_LINKS environment variable is not set")

# Ensure directory exists
ensure_directory_exists(os.path.dirname(path_for_save_txt_links))

print(f"Environment path: {path_for_save_txt_links}")

# Configure Selenium Headless Mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run without opening a browser
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")

# Set a real User-Agent to avoid bot detection
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

start_time = time.time()

# Create WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open SEC website
url10K = "https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK=&type=10-K&owner=include&count=100&action=getcurrent"
driver.get(url10K)
logger.info(f"🔹 Opened SEC website: {url10K}")
url10Q = "https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK=&type=10-Q&owner=include&count=100&action=getcurrent"
driver.get(url10Q)
logger.info(f"🔹 Opened SEC website: {url10Q}")
url8K = "https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK=&type=8-K&owner=include&count=100&action=getcurrent"
driver.get(url8K)
logger.info(f"🔹 Opened SEC website: {url8K}")





# Wait for the page to load properly
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
except Exception as e:
    logger.error(f"❌ Page did not load properly: {e}")
    driver.quit()
    exit()



# Extract only .txt links using XPath
rows = driver.find_elements(By.XPATH, "//tr")

extracted_data = []
download_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for row in rows:
    try:
        report_type = row.find_element(By.XPATH, ".//td[1]").text.strip()
        report_date = row.find_element(By.XPATH, ".//td[2]").text.strip()
        text_link_elem = row.find_element(By.XPATH, ".//td/a[contains(@href, '.txt')]")
        text_link = text_link_elem.get_attribute("href")
        extracted_data.append({
            "Report Type": report_type,
            "Download Date": download_date,
            "Link": text_link
        })
    except Exception:
        continue
    
logger.info(f"🔹 Found {len(extracted_data)} .txt links")

# Load existing data to prevent overwriting
if os.path.exists(path_for_save_txt_links):
    with open(path_for_save_txt_links, "r") as f:
        try:
            existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = []
else:
    existing_data = []

# Merge new and existing data, ensuring no duplicates
all_data = {entry["Link"]: entry for entry in existing_data + extracted_data}.values()

# Save data to JSON file
with open(path_for_save_txt_links, "w") as f:
    json.dump(list(all_data), f, indent=4)
    logger.info(f"🔹 Saved JSON data with {len(all_data)} records")

# Close browser
driver.quit()
logger.info(f"🔹 Closed browser")
end_time = time.time()
logger.info(f"🔹 Total execution time: {end_time - start_time} seconds")
