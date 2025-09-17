import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from typing import List

DB_PATH = r"D:\MAGIC\outputs\zephyr_trends.db"
USER_PREFS_TABLE = "user_preferences"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS {USER_PREFS_TABLE} (
            username TEXT PRIMARY KEY,
            platforms TEXT,
            start_date TEXT,
            end_date TEXT,
            keyword_filter TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_prefs(username, platforms, start_date, end_date, keyword_filter):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f"""
        INSERT OR REPLACE INTO {USER_PREFS_TABLE} 
        (username, platforms, start_date, end_date, keyword_filter) 
        VALUES (?, ?, ?, ?, ?)
    """, (username, ",".join(platforms), start_date, end_date, keyword_filter))
    conn.commit()
    conn.close()

def load_prefs(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f"SELECT platforms, start_date, end_date, keyword_filter FROM {USER_PREFS_TABLE} WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if row:
        platforms = row[0].split(",") if row[0] else []
        return {
            "platforms": platforms,
            "start_date": datetime.strptime(row[1], "%Y-%m-%d").date() if row[1] else None,
            "end_date": datetime.strptime(row[2], "%Y-%m-%d").date() if row[2] else None,
            "keyword_filter": row[3] or ""
        }
    return None

def query_trends(platforms: List[str], start_date: str, end_date: str, keyword_filter: str) -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
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

# Initialize DB table if missing
init_db()

st.set_page_config(layout="wide")
st.title("🌟 Zephyr Trend Dashboard (User Profiles & Saved Views)")

# User login (demo, no passwords)
username = st.sidebar.text_input("Enter your username:", "")

if username:
    prefs = load_prefs(username)
    today = datetime.today().date()

    platforms_default = prefs["platforms"] if prefs else ["google_trends", "youtube_autocomplete"]
    start_default = prefs["start_date"] if prefs and prefs["start_date"] else today - timedelta(days=30)
    end_default = prefs["end_date"] if prefs and prefs["end_date"] else today
    keyword_default = prefs["keyword_filter"] if prefs else ""

    selected_platforms = st.sidebar.multiselect("Select platforms:", ["google_trends", "youtube_autocomplete", "reddit", "tiktok", "amazon"], default=platforms_default)

    start_date = st.sidebar.date_input("Start date", start_default)
    end_date = st.sidebar.date_input("End date", end_default)
    if start_date > end_date:
        st.sidebar.error("Start date must be before end date.")

    keyword_filter = st.sidebar.text_input("Keyword filter (substring):", keyword_default)

    if st.sidebar.button("💾 Save Preferences"):
        save_prefs(username, selected_platforms, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), keyword_filter)
        st.sidebar.success("Preferences saved!")

    if selected_platforms and start_date <= end_date:
        df = query_trends(selected_platforms, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), keyword_filter)
        if df.empty:
            st.warning("No data found for the selected filters.")
        else:
            st.dataframe(df)
else:
    st.info("Please enter your username to load or save your preferences.")
