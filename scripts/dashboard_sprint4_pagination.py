import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("🌟 Zephyr Trend Dashboard - Pagination & Async Simulation")

@st.cache_data(show_spinner=False)
def get_data(platforms, start_date, end_date, keyword_filter, limit, offset):
    conn = sqlite3.connect(r"D:\MAGIC\outputs\zephyr_trends.db")
    try:
        query = f"""
        SELECT date, keyword, platform, metric FROM trends
        WHERE platform IN ({",".join(["?"]*len(platforms))})
        AND date BETWEEN ? AND ?
        LIMIT ? OFFSET ?
        """
        params = platforms + [start_date, end_date, limit, offset]
        df = pd.read_sql_query(query, conn, params=params)
        if keyword_filter:
            df = df[df["keyword"].str.contains(keyword_filter, case=False, na=False)]
        return df
    finally:
        conn.close()

all_platforms = ["google_trends", "youtube_autocomplete", "reddit", "tiktok", "amazon"]
selected_platforms = st.sidebar.multiselect("Select platforms:", all_platforms, default=all_platforms)

today = datetime.today().date()
start_date = st.sidebar.date_input("Start date", today - timedelta(days=30))
end_date = st.sidebar.date_input("End date", today)

if start_date > end_date:
    st.sidebar.error("Start date must be before end date.")

keyword_filter = st.sidebar.text_input("Keyword filter (substring):")

page_size = 50

if "page_num" not in st.session_state:
    st.session_state.page_num = 1

offset = (st.session_state.page_num - 1) * page_size
df = get_data(selected_platforms, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), keyword_filter, page_size, offset)

st.dataframe(df)

col1, col2, col3 = st.columns([1,2,1])

with col1:
    if st.button("Previous") and st.session_state.page_num > 1:
        st.session_state.page_num -= 1

with col3:
    if st.button("Next"):
        st.session_state.page_num += 1
