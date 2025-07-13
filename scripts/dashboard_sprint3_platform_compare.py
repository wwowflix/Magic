import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("🌟 Zephyr Trend Dashboard - Platform Comparison")

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
SELECT keyword, platform, SUM(metric) as total_metric FROM trends
WHERE platform IN ({','.join(['?']*len(selected_platforms))})
AND date BETWEEN ? AND ?
GROUP BY keyword, platform
"""
params = selected_platforms + [start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")]

df = pd.read_sql_query(query, conn, params=params)

if keyword_filter:
    df = df[df['keyword'].str.contains(keyword_filter, case=False, na=False)]

if df.empty:
    st.warning("No data found for the selected filters.")
    st.stop()

# Pivot data for plotting
pivot_df = df.pivot(index='keyword', columns='platform', values='total_metric').fillna(0)

# Filter to top N keywords by total metric sum across platforms
top_n = 20
pivot_df['total'] = pivot_df.sum(axis=1)
top_keywords = pivot_df.sort_values('total', ascending=False).head(top_n).drop(columns='total')

# Plot grouped bar chart
fig = px.bar(top_keywords, barmode='group', title="Top Keywords by Platform",
             labels={"value": "Total Metric", "keyword": "Keyword", "platform": "Platform"})
st.plotly_chart(fig, use_container_width=True)

conn.close()
