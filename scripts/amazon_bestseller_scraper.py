import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from cost_manager import track_cost

def scrape_amazon_bestsellers():
    url = "https://www.amazon.com/Best-Sellers-Books/zgbs/books"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    resp = requests.get(url, headers=headers)

    soup = BeautifulSoup(resp.text, "html.parser")

    # Updated selector to match Amazon's new layout
    items = soup.select("._cDEzb_p13n-sc-css-line-clamp-1_1Fn1y")

    rows = []
    for item in items:
        keyword = item.get_text(strip=True)
        rows.append({
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "keyword": keyword,
            "platform": "amazon_bestsellers",
            "metric": 1
        })

    if rows:
        df = pd.DataFrame(rows)
        df.to_csv("amazon_bestsellers_output.csv", index=False)
        track_cost("amazon_bestsellers", 0.02)
        print("Amazon bestseller data saved.")
    else:
        print("No Amazon bestseller items found.")

if __name__ == "__main__":
    scrape_amazon_bestsellers()
