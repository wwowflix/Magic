import tiktok_scraper
if __name__ == "__main__":
        print("✅ Reddit scraping complete. Data saved to outputs/reddit_scrape.csv.")
import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, help='Choose trend source: google, reddit, etc.')
    parser.add_argument('--subreddits', type=str, help='Comma-separated subreddits for reddit scraping')
    parser.add_argument('--keywords', type=str, help='Comma-separated list of keywords for Google Trends scraping')
    args = parser.parse_args()

    keywords = ['AI tools']
    if args.keywords:
        keywords = [k.strip() for k in args.keywords.split(',')]

    if args.source == "google":
        scrape_google_trends(keywords)

    elif args.source == "tiktok":
        tiktok_scraper.scrape_tiktok()

    elif args.source == "youtube":
        youtube_scraper.scrape_youtube()

    elif args.source == "reddit":
        subreddits = [s.strip() for s in args.subreddits.split(",")]
        client_id = "OBhDPCPwu_CJkw813LQwng"
        client_secret = "zjl6-I2sU9i3cNOBRx76tnpLCyPCBg"
        user_agent = "MAGICZephyrScraper/0.1 by u/AffectionateRoom6084"

        df = scrape_reddit(subreddits, client_id, client_secret, user_agent)

        # --- STANDARDIZE COLUMNS ---
        standard_cols = ['date', 'keyword', 'metric', 'platform', 'author']
        for col in standard_cols:
            if col not in df.columns:
                df[col] = 'N/A'
        df = df[standard_cols]
        # --- END STANDARDIZE ---

        df.to_csv("outputs/reddit_scrape.csv", index=False, encoding="utf-8-sig")
        print("✅ Reddit scraping complete. Data saved to outputs/reddit_scrape.csv.")
