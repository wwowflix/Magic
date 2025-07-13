import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(layout="wide")
st.title("🌟 Zephyr Trend Dashboard - Anomaly Detection Alerts")

conn = sqlite3.connect(r"D:\MAGIC\outputs\zephyr_trends.db")

# Sidebar filters
platforms = ["google_trends", "youtube_autocomplete", "reddit", "tiktok", "amazon"]
selected_platforms = st.sidebar.multiselect("Select platforms:", platforms, default=platforms)

today = datetime.today().date()
start_date = st.sidebar.date_input("Start date", today - timedelta(days=30))
end_date = st.sidebar.date_input("End date", today)

if start_date > end_date:
    st.sidebar.error("Start date must be before end date.")

keyword_filter = st.sidebar.text_input("Keyword filter (substring):")

query = f"""
SELECT date, keyword, platform, metric FROM trends
WHERE platform IN ({','.join(['?']*len(selected_platforms))})
AND date BETWEEN ? AND ?
"""
params = selected_platforms + [start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")]

df = pd.read_sql_query(query, conn, params=params)

if keyword_filter:
    df = df[df['keyword'].str.contains(keyword_filter, case=False, na=False)]

if df.empty:
    st.warning("No data found for the selected filters.")
    st.stop()

# Compute daily sums per keyword
daily_sums = df.groupby(['date', 'keyword'])['metric'].sum().reset_index()

# Pivot to time series format
pivot_df = daily_sums.pivot(index='date', columns='keyword', values='metric').fillna(0)

# Convert index to datetime
pivot_df.index = pd.to_datetime(pivot_df.index)

# Calculate z-score to detect anomalies per keyword
z_scores = (pivot_df - pivot_df.mean()) / pivot_df.std()

# Detect spikes where z-score > threshold (e.g., 3)
threshold = 3
anomalies = (z_scores > threshold)

# Show anomalies
st.subheader("Anomaly Alerts (z-score > 3)")
for keyword in anomalies.columns:
    dates = anomalies.index[anomalies[keyword]].strftime('%Y-%m-%d').tolist()
    if dates:
        st.markdown(f"**{keyword}**: Spike detected on dates: {', '.join(dates)}")

# Optionally show charts of anomalous keywords
selected_keywords = st.multiselect("Select keywords to view time series:", pivot_df.columns.tolist())

for kw in selected_keywords:
    st.line_chart(pivot_df[kw])

conn.close()
