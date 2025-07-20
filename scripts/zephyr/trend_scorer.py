#!/usr/bin/env python3
"""
trend_scorer.py

This script reads youtube_normalized.csv and assigns a smart score to each trend
based on its source (API vs autocomplete), view count, keyword quality, and recency.
"""

import pandas as pd
import numpy as np
import os

input_csv = "D:/MAGIC/outputs/youtube_normalized.csv"
output_csv = "D:/MAGIC/outputs/youtube_scored.csv"

if not os.path.exists(input_csv):
    print(f"? Input file not found: {input_csv}")
    exit(1)

print("?? Scoring trends from:", input_csv)
df = pd.read_csv(input_csv)

def compute_score(row):
    score = 0

    # ?? Log-scaled view count boost
    try:
        views = int(row['metric'])
        score += min(10, round((np.log1p(views) * 5), 2))
    except:
        pass

    # ?? Source weight: API > Autocomplete
    if pd.notna(row.get('author')) and row['author'] != '':
        score += 10
    else:
        score += 5

    # ? Keyword length bonus
    if len(str(row['keyword']).split()) <= 3:
        score += 3

    # ?? Recency bonus (within 24h)
    try:
        date = pd.to_datetime(row['date'], errors='coerce')
        if pd.notna(date) and date > pd.Timestamp.utcnow() - pd.Timedelta(days=1):
            score += 5
    except:
        pass

    return round(score, 2)

df['score'] = df.apply(compute_score, axis=1)
df = df.sort_values(by='score', ascending=False)
df.to_csv(output_csv, index=False)
print(f"? Scored trends saved to {output_csv}")
