#!/usr/bin/env python3
"""
export_json.py

Reads the correlated_trends.csv and exports a trimmed JSON
file with just the keyword and score for dashboard or downstream use.
"""

import pandas as pd
import os
import json

input_csv = "D:/MAGIC/outputs/trends/correlated_trends.csv"
output_json = "D:/MAGIC/outputs/trends/correlated_trends.json"

if not os.path.exists(input_csv):
    print(f"❌ Input file not found: {input_csv}")
    exit(1)

df = pd.read_csv(input_csv)

# Keep only relevant fields
export_data = df[["keyword", "score"]].to_dict(orient="records")

with open(output_json, "w", encoding="utf-8") as f:
    json.dump(export_data, f, ensure_ascii=False, indent=2)

print(f"✅ Correlated trends exported to {output_json}")
