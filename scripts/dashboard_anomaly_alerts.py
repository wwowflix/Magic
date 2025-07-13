import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from typing import List

def query_trends(platforms: List[str], start_date: str, end_date: str, keyword_filter: str) -> pd.DataFrame:
    conn = sqlite3.connect(r"D:\MAGIC\outputs\zephyr_trends.db")
    try:
        query = f"""
        SELECT date, keyword, platform, metric FROM trends
        WHERE platform IN ({",".join(["?"]*len(platforms))})
        AND date BETWEEN ? AND ?
        """
        params = platforms + [start_date, end_date]
        df = pd.read_sql_query(query, conn, params=params)
        if keyword_filter:
            df = df[df["keyword"].str.contains(keyword_filter, case=False, na=False)]
        return df
    finally:
        conn.close()

def detect_anomalies(df: pd.DataFrame, window: int = 7, threshold: float = 3.0) -> pd.DataFrame:
    # Compute rolling mean and std dev of metric grouped by keyword
    df_sorted = df.sort_values(["keyword", "date"])
    df_sorted["rolling_mean"] = df_sorted.groupby("keyword")["metric"].transform(lambda x: x.rolling(window, 1).mean())
    df_sorted["rolling_std"] = df_sorted.groupby("keyword")["metric"].transform(lambda x: x.rolling(window, 1).std().fillna(0))
    df_sorted["z_score"] = (df_sorted["metric"] - df_sorted["rolling_mean"]) / df_sorted["rolling_std"].replace(0, 1)
    # Flag anomalies where z_score > threshold
    anomalies = df_sorted[(df_sorted["z_score"].abs() > threshold)]
    return anomalies

st.set_page_config(layout="wide")
st.title("🌟 Zephyr Trend Dashboard (Sprint 6: Anomaly Detection Alerts)")

all_platforms = ["google_trends", "youtube_autocomplete", "reddit", "tiktok", "amazon"]
selected_platforms = st.sidebar.multiselect("Select platforms:", all_platforms, default=["google_trends", "youtube_autocomplete"])

today = datetime.today().date()
start_date = st.sidebar.date_input("Start date", today - timedelta(days=60))
end_date = st.sidebar.date_input("End date", today)
if start_date > end_date:
    st.sidebar.error("Start date must be before end date.")

keyword_filter = st.sidebar.text_input("Keyword filter (substring):", "")

df = query_trends(selected_platforms, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), keyword_filter)

if df.empty:
    st.warning("No data found for the selected filters.")
else:
    st.subheader("Trend Data")
    st.dataframe(df)

    anomalies = detect_anomalies(df)

    if anomalies.empty:
        st.success("No anomalies detected in the selected date range and filters.")
    else:
        st.error(f"⚠️ Detected {len(anomalies)} anomalies! Check the table below:")
        st.dataframe(anomalies[["date", "keyword", "platform", "metric", "z_score"]].sort_values(by="z_score", ascending=False))

