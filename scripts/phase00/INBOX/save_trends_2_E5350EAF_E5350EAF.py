"""
save_trends.py 🔽
Part of Zephyr – Phase 2, Module G (G.2.44)

✅ Purpose:
Save cleaned or raw trend data to CSV format with a timestamped filename.
Supports any platform (Reddit, Google Trends, TikTok, etc.)

🧠 Inputs:
- List[Dict] or pandas.DataFrame of trend items
- Platform/source name (e.g. 'reddit', 'google', 'tiktok')

📤 Output:
- File saved under outputs/{platform}_trends_YYYYMMDD_HHMMSS.csv
"""

import os
import csv
import pandas as pd
from datetime import datetime

OUTPUT_DIR = "outputs"


def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def save_trends(data, source_name="unknown"):
    """
    Save trend data to timestamped CSV in outputs/ folder.

    Args:
        data (List[Dict] | pd.DataFrame): Trend data to save
        source_name (str): Optional tag for filename (e.g., 'reddit', 'google')
    """
    ensure_output_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{source_name}_trends_{timestamp}.csv"
    filepath = os.path.join(OUTPUT_DIR, filename)

    try:
        if isinstance(data, pd.DataFrame):
            data.to_csv(filepath, index=False, encoding="utf-8-sig")
        elif isinstance(data, list) and isinstance(data[0], dict):
            with open(filepath, mode="w", newline="", encoding="utf-8-sig") as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        else:
            raise ValueError(
                "Unsupported data format. Must be list[dict] or DataFrame."
            )
        print(f"✅ Trends saved to {filepath}")
    except Exception as e:
        print(f"❌ Error saving trends: {e}")
