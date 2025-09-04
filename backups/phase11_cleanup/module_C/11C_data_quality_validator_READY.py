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
                    issues.append(f"ðŸ§ª {file}: {len(null_rows)} rows with nulls")
            except Exception as e:
                issues.append(f"âš ï¸ {file}: Failed to load â€“ {e}")

# Write report
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
with open(LOG_FILE, "w", encoding="utf-8") as f:
    if not issues:
        f.write("âœ… All data files are clean.\n")
    else:
        f.write("âŒ Data Quality Issues Found:\n")
        for issue in issues:
            f.write(issue + "\n")

print(f"ðŸ” Scan complete. Issues: {len(issues)}")
print(f"ðŸ“„ Report saved to: {LOG_FILE}")
