# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright


def login_and_save_cookies():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.tiktok.com/foryou")

        print("-> PLEASE LOG IN NOW (you have ~5 minutes)...")
        page.wait_for_timeout(300000)  # 5 minutes

        context.storage_state(path="tiktok_state.json")
        print("OK TikTok session cookies saved to tiktok_state.json.")

        browser.close()


if __name__ == "__main__":
    login_and_save_cookies()
