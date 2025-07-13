import streamlit as st
import pandas as pd
import sqlite3
import subprocess
from datetime import datetime, timedelta
from typing import List

SCRAPER_SCRIPT_PATH = r"D:\MAGIC\scripts\run_scrapers.bat"  # <-- Adjust as needed

@st.cache_data(show_spinner=False)
def query_trends(platforms: List[str], start_date: str, end_date: str, keyword_filter: str) -> pd.DataFrame:
    conn = sqlite3.connect(r"D:\MAGIC\outputs\zephyr_trends.db")
    try:
        query = f"""
        SELECT date, keyword, platform, metric FROM trends
        WHERE platform IN ({','.join(['?']*len(platforms))})
        AND date BETWEEN ? AND ?
        """
        params = platforms + [start_date, end_date]
        df = pd.read_sql_query(query, conn, params=params)

        if keyword_filter:
            df = df[df['keyword'].str.contains(keyword_filter, case=False, na=False)]
        return df
    finally:
        conn.close()

st.set_page_config(layout="wide")
st.title("🌟 Zephyr Trend Dashboard (Sprint 5: Auto Refresh)")

all_platforms = ["google_trends", "youtube_autocomplete", "reddit", "tiktok", "amazon"]
selected_platforms = st.sidebar.multiselect("Select platforms:", all_platforms, default=["google_trends", "youtube_autocomplete"])

today = datetime.today().date()
start_date = st.sidebar.date_input("Start date", today - timedelta(days=30))
end_date = st.sidebar.date_input("End date", today)
if start_date > end_date:
    st.sidebar.error("Start date must be before end date.")

keyword_filter = st.sidebar.text_input("Keyword filter (substring):", "")

# Auto Refresh button
if st.sidebar.button("🔄 Run Scrapers & Refresh Data"):
    with st.spinner("Running scrapers... this may take a moment."):
        # Run your scraper batch or python script (adjust as needed)
        result = subprocess.run([SCRAPER_SCRIPT_PATH], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            st.success("Scrapers finished successfully! Reloading data...")
            st.experimental_rerun()
        else:
            st.error(f"Scraper run failed:\n{result.stderr}")

# Query and display data
df = query_trends(selected_platforms, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), keyword_filter)

if df.empty:
    st.warning("No data found for the selected filters.")
else:
    st.dataframe(df)
