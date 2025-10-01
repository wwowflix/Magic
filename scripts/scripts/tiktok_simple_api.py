# -*- coding: utf-8 -*-
import requests
import csv
from datetime import datetime

# TikTok’s unofficial trending API endpoint
API_URL = "https://www.tiktok.com/api/discover/item/list?aid=1988&app_language=en&count=20&cursor=0&type=5"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://www.tiktok.com/trending?lang=en",
    "Accept": "application/json"
}

def scrape_simple_api():
    resp = requests.get(API_URL, headers=HEADERS, timeout=15)
    data = resp.json().get("body", {}).get("itemListData", [])
    rows = []
    for it in data:
        info = it.get("itemInfos", {})
        rows.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "author": info.get("authorName", ""),
            "title": info.get("text", ""),
            "url": info.get("videoPlayUrl", "")
        })
    return rows

if __name__ == "__main__":
    videos = scrape_simple_api()
    with open("outputs/tiktok_scrape_simple.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["date","author","title","url"])
        writer.writeheader()
        writer.writerows(videos)
    print(f"OK Simple-API scraped -> {len(videos)} rows.")

