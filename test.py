import pandas as pd

# 🔹 Paths to CSV files
csv_final_path = "/Users/elmaliahmac/Documents/HippoDashBoard/py/xbrl_final_data.csv"
csv_textual_path = "/Users/elmaliahmac/Documents/HippoDashBoard/py/xbrl_textual_data.csv"
csv_output_path = "/Users/elmaliahmac/Documents/HippoDashBoard/py/xbrl_unknown_tags.csv"

# 🔹 Load CSV files
df_final = pd.read_csv(csv_final_path, usecols=["Tag", "RegulatoryTerm"])
df_textual = pd.read_csv(csv_textual_path, usecols=["Tag", "RegulatoryTerm"])

# 🔹 Combine both files
df_combined = pd.concat([df_final, df_textual]).drop_duplicates()

# 🔹 Filter only rows where RegulatoryTerm is "Unknown"
df_unknown = df_combined[df_combined["RegulatoryTerm"] == "Unknown"]

# 🔹 Save to a new CSV file
df_unknown.to_csv(csv_output_path, index=False)

print(f"✅ Unknown regulatory terms extracted and saved to: {csv_output_path}")



