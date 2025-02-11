from env_loader import load_environment_variables
from metadata_loader import load_metadata
from file_utils import ensure_directory_exists, clean_filename
from process_xbrl import load_xbrl_file, extract_metadata, process_xbrl_data
from database import save_data_to_db
from ticker_lookup import fetch_ticker_from_db, save_ticker_to_db
import pandas as pd
import os
import logging
import time


# 🔹 Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

start_time = time.time()






def main():
    try:
        env_vars = load_environment_variables()
        metadata = load_metadata(env_vars["tags_json_path"])
        model_xbrl = load_xbrl_file(env_vars["file_path"])

        # חיפוש הטיקר
        company_id, report_type, fiscal_year = extract_metadata(model_xbrl, metadata)
        
        if company_id == "Unknown":
            company_id = fetch_ticker_from_db()  # ניסיון להשיג טיקר מהדאטה בייס
        
        save_ticker_to_db(company_id)  # שמירת הטיקר בבסיס הנתונים
        
        # יצירת נתיב לקובץ
        filename = f"{clean_filename(company_id)}_{clean_filename(report_type)}_{clean_filename(fiscal_year)}.csv"
        csv_dir = env_vars["csv_output_dir"]
        ensure_directory_exists(csv_dir)
        csv_output_path = os.path.join(csv_dir, filename)
        
        logger.info(f"✅ CSV will be saved as: {csv_output_path}")

        # עיבוד הנתונים
        all_data, _ = process_xbrl_data(model_xbrl, company_id, report_type, fiscal_year, metadata)

        # שמירת נתונים
        df_all = pd.DataFrame(all_data, columns=[
            "CompanyID", "ReportType", "FiscalYear", "Tag", "RegulatoryName", "CleanValue",
            "StartDate", "EndDate", "Instant", "Category", "SubCategory", "Type", "RiskLevel", "Usage"
        ])
        df_all.to_csv(csv_output_path, index=False)
        save_data_to_db(all_data, env_vars["db_path"])

        logger.info(f"✅ Data for {company_id} ({report_type} {fiscal_year}) saved.")

        end_time = time.time()
        logger.info(f"🔹 Total execution time of main: {end_time - start_time} seconds")

    except Exception as e:
        logger.exception(f"Error in main: {e}")
        raise


end_time = time.time()
logger.info(f"🔹 Total execution time of main: {end_time - start_time} seconds")


if __name__ == "__main__":
    main()
