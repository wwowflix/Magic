# -*- coding: utf-8 -*-
import csv, logging
def scrape_youtube_trends():
    return [{'video_id': 'xyz123', 'title': 'AI makes music', 'views': 123456}]
if __name__ == '__main__':
    logging.basicConfig(filename='logs/youtube.log', level=logging.INFO)
    trends = scrape_youtube_trends()
    with open('outputs/youtube_scrape.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=trends[0].keys())
        writer.writeheader()
        writer.writerows(trends)
    logging.info(f"Saved {len(trends)} YouTube trends")
