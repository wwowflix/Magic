import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("🌟 Zephyr Trend Dashboard (Sprint 3: Heatmap & Multi-Platform)")

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

# Load data
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

# Prepare data for heatmap: aggregate metric by date and keyword
heatmap_data = df.pivot_table(
    index='date',
    columns='keyword',
    values='metric',
    aggfunc='sum',
    fill_value=0
)

# Convert index to datetime
heatmap_data.index = pd.to_datetime(heatmap_data.index, errors='coerce')

# Sort index (date)
heatmap_data = heatmap_data.sort_index()

# Plotly heatmap
fig = px.imshow(
    heatmap_data.T,
    labels=dict(x="Date", y="Keyword", color="Metric"),
    aspect="auto",
    color_continuous_scale='Viridis'
)
fig.update_xaxes(tickangle=45, tickformat='%Y-%m-%d')
st.plotly_chart(fig, use_container_width=True)

conn.close()
