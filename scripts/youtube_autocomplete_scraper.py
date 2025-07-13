import requests
import pandas as pd
from datetime import datetime, timezone
from cost_manager import track_cost
import json
import sys
import os

def scrape_youtube_autocomplete(keyword):
    url = f"https://suggestqueries.google.com/complete/search?client=youtube&ds=yt&q={keyword}&hl=en"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    resp = requests.get(url, headers=headers)

    text = resp.text.strip()

    prefix = "window.google.ac.h("
    suffix = ")"

    if text.startswith(prefix):
        json_str = text[len(prefix):-len(suffix)]
        json_str = json_str.strip()
        try:
            json_data = json.loads(json_str)
        except json.JSONDecodeError as e:
            print("JSON decode error:", e)
            print("Raw json string:")
            print(json_str)
            return None

        suggestions = []
        for sug in json_data[1]:
            suggestions.append({
                "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "keyword": sug[0],
                "platform": "youtube_autocomplete",
                "metric": 1
            })

        if suggestions:
            df = pd.DataFrame(suggestions)
            return df
        else:
            print("No suggestions found.")
            return None
    else:
        print("No recognizable JSONP format found.")
        print("Raw text:")
        print(text)
        return None

if __name__ == "__main__":
    kw = sys.argv[1] if len(sys.argv) > 1 else "ai"

    output_dir = r"D:\MAGIC\outputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = f"youtube_autocomplete_output_{kw}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.csv"
    output_path = os.path.join(output_dir, output_file)

    df = scrape_youtube_autocomplete(kw)

    if df is not None and not df.empty:
        df.to_csv(output_path, index=False)
        track_cost("youtube_autocomplete", 0.01)
        print(f"YouTube autocomplete data saved to {output_path}")
    else:
        print(f"No data found for keyword: {kw}")
