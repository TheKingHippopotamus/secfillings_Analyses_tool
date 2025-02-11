from arelle import Cntlr
import logging
import time


# 🔹 Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

start_time = time.time()




def load_xbrl_file(file_path):
    try:
        cntlr = Cntlr.Cntlr()
        return cntlr.modelManager.load(file_path)
    except Exception as e:
        logger.exception(f"Error loading XBRL file: {e}")
        raise

def extract_metadata(model_xbrl, metadata):
    try:
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

        return company_id, report_type, fiscal_year
    except Exception as e:
        logger.exception(f"Error extracting metadata: {e}")
        raise

def process_xbrl_data(model_xbrl, company_id, report_type, fiscal_year, metadata):
    try:
        all_data = []

        for fact in model_xbrl.facts:
            tag = fact.concept.qname.localName if fact.concept else fact.qname.localName
            value = fact.value if fact.value else "N/A"
            meta = metadata.get(tag, {})

            all_data.append((
                company_id, report_type, fiscal_year, tag,
                meta.get("RegulatoryName", "Unknown"),
                value, "NULL", "NULL", "NULL",
                meta.get("Category", "Unknown"),
                meta.get("SubCategory", "Unknown"),
                meta.get("Type", "Unknown"),
                meta.get("RiskLevel", "Unknown"),
                ", ".join(meta.get("Usage", ["Unknown"]))
            ))

        return all_data, set()
        
    except Exception as e:
        logger.exception(f"Error processing XBRL data: {e}")
        raise




end_time = time.time()
logger.info(f"🔹 Total execution time of process_xbrl_data: {end_time - start_time} seconds")




