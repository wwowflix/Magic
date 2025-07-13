from pytrends.request import TrendReq
import pandas as pd
from cost_manager import track_cost

# Universal CSV schema columns:
# date, keyword, platform, metric

def scrape_google_trends(keywords):
    pytrends = TrendReq(hl="en-US", tz=360)
    pytrends.build_payload(keywords, timeframe="now 7-d")

    df = pytrends.interest_over_time()

    if df.empty:
        print("No data retrieved.")
        return

    df.reset_index(inplace=True)

    rows = []
    for _, row in df.iterrows():
        date = row["date"]
        for keyword in keywords:
            value = row[keyword]
            rows.append({
                "date": date,
                "keyword": keyword,
                "platform": "google_trends",
                "metric": value
            })

    output_df = pd.DataFrame(rows)
    output_df.to_csv("google_trends_output.csv", index=False)
    track_cost("google_trends", 0.01)

    print("Google Trends data saved.")

if __name__ == "__main__":
    scrape_google_trends(["AI"])

