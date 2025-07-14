from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def scrape_tiktok():
    print("Scraping TikTok via Selenium...")

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.tiktok.com/trending")

    time.sleep(5)

    # Scroll down to load more videos
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    # Dump entire HTML for debugging
    html = driver.page_source
    dump_path = r"D:\MAGIC\outputs\tiktok_page_dump.html"
    with open(dump_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ HTML dump saved to {dump_path}")

    try:
        elements = driver.find_elements(By.XPATH, "//div[contains(@data-e2e, 'desc')]")

        rows = []
        for elem in elements:
            title = elem.text.strip()
            if title:
                rows.append({
                    "date": pd.Timestamp.today().date(),
                    "keyword": title,
                    "platform": "tiktok",
                    "metric": 0,
                    "author": "unknown"
                })

        if rows:
            df = pd.DataFrame(rows)
            csv_path = r"D:\MAGIC\outputs\tiktok_scrape.csv"
            df.to_csv(csv_path, index=False, encoding="utf-8-sig")
            print(f"✅ TikTok Selenium scraping complete. Data saved to {csv_path}")
            print(df.head())
        else:
            print("⚠️ No trending videos found in Selenium scrape.")

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_tiktok()
