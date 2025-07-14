import streamlit as st
import pandas as pd
import os

st.title("🔥 Multi-Platform Dashboard")

file_paths = {
    "Google Trends": "outputs/google_trends_output.csv",
    "Reddit": "outputs/reddit_scrape.csv",
    "YouTube": "outputs/youtube_scrape.csv",
    "TikTok": None
}

for platform, file in file_paths.items():
    if platform == "TikTok":
        import sqlite3
        conn = sqlite3.connect(r"D:/MAGIC/outputs/zephyr_trends.db")
        df = pd.read_sql_query(
            "SELECT * FROM trends WHERE platform = 'tiktok'",
            conn
        )
        conn.close()
        st.write("✅ Loaded TikTok data from SQLite!")
        st.dataframe(df)
    elif file and os.path.exists(file):
        df = pd.read_csv(file)
        st.write(f"✅ Loaded {platform} data from {file}")
        st.dataframe(df)
    else:
        st.write(f"⚠️ File not found for {platform}")
