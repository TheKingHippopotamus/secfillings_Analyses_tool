from arelle import Cntlr

def load_xbrl_file(file_path):
    cntlr = Cntlr.Cntlr()
    return cntlr.modelManager.load(file_path)

def extract_metadata(model_xbrl, metadata):
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

def process_xbrl_data(model_xbrl, company_id, report_type, fiscal_year, metadata):
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
