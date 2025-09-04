import csv
from datetime import datetime
from googleapiclient.discovery import build

API_KEY = "AIzaSyAFhk0N5grMqInsZkH4pTJBdyXVJ-n5xs4"
REGION_CODE = "US"


def fetch_youtube_trending(api_key, region_code=REGION_CODE):
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        regionCode=region_code,
        maxResults=10,
    )
    response = request.execute()
    return response


def save_youtube_trends_to_csv(response):
    videos = response.get("items", [])
    if not videos:
        print("No videos found.")
        return

    fieldnames = [
        "video_id",
        "title",
        "channelTitle",
        "viewCount",
        "likeCount",
        "commentCount",
        "thumbnail_url",
        "date",
    ]

    with open(
        "D:/MAGIC/outputs/youtube_scrape.csv", "w", newline="", encoding="utf-8"
    ) as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for video in videos:
            snippet = video["snippet"]
            stats = video.get("statistics", {})
            writer.writerow(
                {
                    "video_id": video["id"],
                    "title": snippet.get("title", ""),
                    "channelTitle": snippet.get("channelTitle", ""),
                    "viewCount": stats.get("viewCount", "0"),
                    "likeCount": stats.get("likeCount", "0"),
                    "commentCount": stats.get("commentCount", "0"),
                    "thumbnail_url": snippet.get("thumbnails", {})
                    .get("high", {})
                    .get("url", ""),
                    "date": snippet.get("publishedAt", datetime.utcnow().isoformat()),
                }
            )

    print(f"✅ Saved {len(videos)} YouTube trending videos to CSV")


if __name__ == "__main__":
    data = fetch_youtube_trending(API_KEY, REGION_CODE)
    save_youtube_trends_to_csv(data)
