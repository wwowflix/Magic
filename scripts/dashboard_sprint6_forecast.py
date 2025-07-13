import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🌟 Zephyr Trend Dashboard - Forecast Visualizations")

conn = sqlite3.connect(r"D:\MAGIC\outputs\zephyr_trends.db")

platforms = ["google_trends", "youtube_autocomplete", "reddit", "tiktok", "amazon"]
selected_platforms = st.sidebar.multiselect("Select platforms:", platforms, default=platforms)

today = datetime.today().date()
start_date = st.sidebar.date_input("Start date", today - timedelta(days=60))
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

# Select a keyword for forecast visualization
keywords = df['keyword'].unique()
selected_keyword = st.selectbox("Select keyword for forecast visualization:", keywords)

keyword_df = df[df['keyword'] == selected_keyword].copy()
keyword_df['date'] = pd.to_datetime(keyword_df['date'])
keyword_df.set_index('date', inplace=True)

# Load forecast data for selected_keyword
# Here assume forecast data stored as CSV files named forecast_<keyword>.csv in forecasts folder
try:
    forecast_path = f"D:\\MAGIC\\forecasts\\forecast_{selected_keyword}.csv"
    forecast_df = pd.read_csv(forecast_path, parse_dates=['date'])
    forecast_df.set_index('date', inplace=True)
except FileNotFoundError:
    st.warning(f"No forecast data found for keyword: {selected_keyword}")
    forecast_df = None

# Plot actual and forecast
fig, ax = plt.subplots(figsize=(10,5))
ax.plot(keyword_df.index, keyword_df['metric'], label='Actual', color='blue')

if forecast_df is not None:
    ax.plot(forecast_df.index, forecast_df['forecast'], label='Forecast', color='orange')
    ax.fill_between(forecast_df.index,
                    forecast_df['lower_ci'],
                    forecast_df['upper_ci'],
                    color='orange', alpha=0.3, label='Confidence Interval')

ax.set_title(f"Trend and Forecast for '{selected_keyword}'")
ax.set_xlabel("Date")
ax.set_ylabel("Metric")
ax.legend()
st.pyplot(fig)

conn.close()
