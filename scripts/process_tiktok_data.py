# -*- coding: utf-8 -*-
import pandas as pd

df = pd.read_csv('outputs/tiktok_scrape.csv')
df['title'] = df['title'].fillna('No Title')
df = df[df['url'].notna() & (df['url'] != '')]

print(f"Total valid videos with URL: {len(df)}")

df.to_csv('outputs/tiktok_scrape_clean.csv', index=False)

