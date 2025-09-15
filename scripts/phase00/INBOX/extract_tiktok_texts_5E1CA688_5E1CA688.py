# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

# Read saved HTML
with open("outputs/page_source.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# Grab all text from data-e2e tags
elements = soup.find_all(attrs={"data-e2e": True})

found = False
for el in elements:
    text = el.get_text(strip=True)
    if text:
        print("OK FOUND:", text)
        found = True

if not found:
    print("?? No data-e2e texts found.")

# Extra: Grab all text in <span> tags as a backup
print("\\n=== Checking <span> tags ===")
spans = soup.find_all("span")
for span in spans:
    text = span.get_text(strip=True)
    if text:
        print("SPAN:", text)
