#!/usr/bin/env python3
"""
autocomplete_scraper.py

This script fetches YouTube autocomplete suggestions from Google's suggestion API
for a list of base keywords and saves them in Zephyr-compatible format.
"""

import requests
import pandas as pd
from datetime import datetime
import os

# ✅ Define keywords to search for autocomplete suggestions
keywords = ["ai", "chatgpt", "elon", "future", "python", "machine learning"]

# ✅ Store results in a list of dicts
results = []
print("🔍 Fetching YouTube autocomplete suggestions...")

for base_keyword in keywords:
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q={base_keyword}"
    try:
        response = requests.get(url)
        suggestions = response.json()[1]
        for suggestion in suggestions:
            results.append({
                "date": datetime.utcnow().isoformat(),
                "keyword": suggestion,
                "platform": "YouTube",
                "metric": 1,
                "author": ""
            })
    except Exception as e:
        print(f"❌ Failed to fetch suggestions for '{base_keyword}': {e}")

# ✅ Convert to DataFrame
if results:
    df = pd.DataFrame(results)
    output_path = "D:/MAGIC/outputs/youtube_autocomplete.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Saved {len(results)} autocomplete suggestions to {output_path}")
else:
    print("⚠️ No suggestions fetched.")
