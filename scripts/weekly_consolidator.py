#!/usr/bin/env python3
"""
weekly_consolidator.py

Appends current filtered trends to a timestamped CSV file inside
outputs/trends/history/ to keep a weekly archive of high-signal topics.
"""

import pandas as pd
import os
from datetime import datetime

input_csv = "D:/MAGIC/outputs/youtube_filtered.csv"
history_folder = "D:/MAGIC/outputs/trends/history"
timestamp = datetime.utcnow().strftime("%Y-%m-%d")
output_csv = os.path.join(history_folder, f"{timestamp}.csv")

if not os.path.exists(input_csv):
    print(f"❌ Input file not found: {input_csv}")
    exit(1)

if not os.path.exists(history_folder):
    os.makedirs(history_folder)

df = pd.read_csv(input_csv)
df['week'] = timestamp  # tag with current week

df.to_csv(output_csv, index=False)
print(f"✅ Weekly snapshot saved to {output_csv}")
