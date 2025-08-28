# -*- coding: utf-8 -*-
import csv
import logging


def scrape_google_trends():
    return [{"term": "AI tools", "region": "US", "score": 93}]


if __name__ == "__main__":
    logging.basicConfig(filename="logs/google_trends.log", level=logging.INFO)
    trends = scrape_google_trends()
    with open("outputs/google_trends.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=trends[0].keys())
        writer.writeheader()
        writer.writerows(trends)
    logging.info(f"Saved {len(trends)} trends")
