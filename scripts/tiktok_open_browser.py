# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import os

def open_foryou_for_5_minutes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        page.goto("https://www.tiktok.com/foryou")

        print("OK Browser is open on TikTok For You page.")
        print("? Waiting for 5 minutes...")

        page.wait_for_timeout(300000)  # 5 minutes = 300,000 ms

        print("OK Done. Closing browser.")
        browser.close()

if __name__ == "__main__":
    open_foryou_for_5_minutes()

