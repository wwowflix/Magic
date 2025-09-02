import os
import pandas as pd

# CONFIG
TARGET_FOLDER = "outputs/data"
LOG_FILE = "outputs/logs/data_quality_issues_log.txt"

# Collect issues
issues = []

for root, _, files in os.walk(TARGET_FOLDER):
    for file in files:
        if file.endswith(".csv"):
            path = os.path.join(root, file)
            try:
                df = pd.read_csv(path)
                if df.isnull().values.any():
                    null_rows = df[df.isnull().any(axis=1)]
                    issues.append(f"🧪 {file}: {len(null_rows)} rows with nulls")
            except Exception as e:
                issues.append(f"⚠️ {file}: Failed to load – {e}")

# Write report
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
with open(LOG_FILE, "w", encoding="utf-8") as f:
    if not issues:
        f.write("✅ All data files are clean.\n")
    else:
        f.write("❌ Data Quality Issues Found:\n")
        for issue in issues:
            f.write(issue + "\n")

print(f"🔍 Scan complete. Issues: {len(issues)}")
print(f"📄 Report saved to: {LOG_FILE}")
