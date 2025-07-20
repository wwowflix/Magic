import sys
def scrape_google(keywords): print(f"Scraping Google Trends: {keywords}")
def scrape_reddit(): print("Scraping Reddit...")
def scrape_youtube(): print("Scraping YouTube...")

if __name__ == "__main__":
    args = sys.argv
    if "--source" in args:
        src = args[args.index("--source") + 1]
        if src == "google":
            kw = args[args.index("--keywords") + 1]
            scrape_google(kw)
        elif src == "reddit": scrape_reddit()
        elif src == "youtube": scrape_youtube()
        else: print("❌ Unknown source")
