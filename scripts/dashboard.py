import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("🌟 Zephyr Trend Dashboard with Async Pagination")

# Connect to SQLite DB
conn = sqlite3.connect(r"D:\MAGIC\outputs\zephyr_trends.db")

# Sidebar filters
all_platforms = ["google_trends", "youtube_autocomplete", "reddit", "tiktok", "amazon"]
selected_platforms = st.sidebar.multiselect(
    "Select platforms to display:",
    all_platforms,
    default=["google_trends", "youtube_autocomplete"]
)

today = datetime.today().date()
start_date = st.sidebar.date_input("Start date", today - timedelta(days=30))
end_date = st.sidebar.date_input("End date", today)

if start_date > end_date:
    st.sidebar.error("Start date must be before end date.")

keyword_filter = st.sidebar.text_input("Keyword filter (substring):")

# Pagination controls
page_size = 50
page_num = st.sidebar.number_input("Page number", min_value=1, value=1, step=1)

# Calculate offset
offset = (page_num - 1) * page_size

# SQL query with LIMIT and OFFSET for pagination
query = f"""
SELECT date, keyword, platform, metric FROM trends
WHERE platform IN ({','.join(['?']*len(selected_platforms))})
AND date BETWEEN ? AND ?
"""

params = selected_platforms + [start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")]

df = pd.read_sql_query(query + " LIMIT ? OFFSET ?", conn, params=params + [page_size, offset])

if keyword_filter:
    df = df[df["keyword"].str.contains(keyword_filter, case=False, na=False)]

if df.empty:
    st.warning("No data found for the selected filters and page.")
else:
    st.dataframe(df)

    # Simple summary metrics
    st.write(f"Showing page {page_num} with up to {page_size} records per page.")

conn.close()
