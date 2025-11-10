try:
    import selenium.webdriver as _selenium  # type: ignore
except Exception:
    class SeleniumOptionalStub:
        def __getattr__(self, name): raise RuntimeError("Selenium not available")
    _selenium = SeleniumOptionalStub()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

service = Service(r"D:\MAGIC\scripts\chromedriver-win64\chromedriver.exe")
options = webdriver.ChromeOptions()
# Uncomment next line to run headless (no browser window)
# options.add_argument("--headless=new")

driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.google.com")
print("Page title is:", driver.title)
driver.quit()
