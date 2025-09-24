#!/usr/bin/env python3
"""
correlation_engine.py

Compares YouTube filtered trends and Reddit scraped trends to find overlapping keywords.
Outputs a CSV with matched entries.
"""

import pandas as pd
import os

# â�"… File paths
yt_file = "D:/MAGIC/outputs/youtube_filtered.csv"
reddit_file = "D:/MAGIC/outputs/reddit_scrape.csv"
output_file = "D:/MAGIC/outputs/trends/correlated_trends.csv"

# â�"… Check files exist
if not os.path.exists(yt_file) or not os.path.exists(reddit_file):
    print("â��' One or more input files are missing.")
    exit(1)

# â�"… Load both datasets
yt_df = pd.read_csv(yt_file)
reddit_df = pd.read_csv(reddit_file)

# â�"… Normalize keywords for comparison
yt_keywords = set(yt_df["keyword"].str.lower().str.strip())
reddit_keywords = set(reddit_df["title"].str.lower().str.strip())

# â�"… Find overlaps
matched_keywords = yt_keywords.intersection(reddit_keywords)

# â�"… Filter original YouTube rows
correlated_df = yt_df[yt_df["keyword"].str.lower().isin(matched_keywords)]

# â�"… Save output
os.makedirs(os.path.dirname(output_file), exist_ok=True)
correlated_df.to_csv(output_file, index=False)

print(f"â�"… Correlated trends saved to {output_file}")
