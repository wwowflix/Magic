import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from typing import List
import plotly.express as px

PAGE_SIZE = 100  # Number of rows per page

@st.cache_data(show_spinner=False)
def query_trends_paginated(platforms: List[str], start_date: str, end_date: str, keyword_filter: str, offset: int, limit: int) -> pd.DataFrame:
    conn = sqlite3.connect(r"D:\MAGIC\outputs\zephyr_trends.db")
    try:
        query = f"""
        SELECT date, keyword, platform, metric FROM trends
        WHERE platform IN ({','.join(['?']*len(platforms))})
        AND date BETWEEN ? AND ?
        ORDER BY date DESC
        LIMIT ? OFFSET ?
        """
        params = platforms + [start_date, end_date, limit, offset]
        df = pd.read_sql_query(query, conn, params=params)

        if keyword_filter:
            df = df[df['keyword'].str.contains(keyword_filter, case=False, na=False)]
        return df
    finally:
        conn.close()

st.set_page_config(layout="wide")
st.title("🌟 Zephyr Trend Dashboard (Sprint 4: Async Pagination)")

all_platforms = ["google_trends", "youtube_autocomplete", "reddit", "tiktok", "amazon"]
selected_platforms = st.sidebar.multiselect("Select platforms:", all_platforms, default=["google_trends", "youtube_autocomplete"])

today = datetime.today().date()
start_date = st.sidebar.date_input("Start date", today - timedelta(days=30))
end_date = st.sidebar.date_input("End date", today)
if start_date > end_date:
    st.sidebar.error("Start date must be before end date.")

keyword_filter = st.sidebar.text_input("Keyword filter (substring):", "")

# Pagination controls
page_num = st.sidebar.number_input("Page number", min_value=1, value=1, step=1)
offset = (page_num - 1) * PAGE_SIZE

df = query_trends_paginated(selected_platforms, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), keyword_filter, offset, PAGE_SIZE)

if df.empty:
    st.warning("No data found on this page with current filters.")
else:
    st.write(f"Showing page {page_num} (rows {offset + 1} to {offset + len(df)})")
    st.dataframe(df)

    # Simple bar chart for keywords on this page
    top_keywords = df['keyword'].value_counts().head(10)
    st.bar_chart(top_keywords)

