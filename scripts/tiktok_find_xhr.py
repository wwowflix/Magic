import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# <<< IMPORTANT >>>
# Change this to your chromedriver.exe path if different!
CHROMEDRIVER_PATH = r"D:\MAGIC\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

# ✅ NEW → set capability for performance logs
options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

driver = webdriver.Chrome(
    service=Service(CHROMEDRIVER_PATH),
    options=options
)

driver.get("https://www.tiktok.com/tag/trending")

for i in range(10):
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(2)

logs = driver.get_log("performance")

found_urls = []

for entry in logs:
    try:
        message = json.loads(entry["message"])
        message_data = message["message"]

        if (
            message_data["method"] == "Network.requestWillBeSent"
            and "request" in message_data["params"]
        ):
            request = message_data["params"]["request"]
            url = request["url"]

            if "api" in url:
                found_urls.append(url)
    except Exception:
        continue

unique_urls = list(set(found_urls))
for url in unique_urls:
    print(url)

driver.quit()
