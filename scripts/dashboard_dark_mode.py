import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from typing import List

# Define light and dark themes as dicts (for reference, not applied directly here)
LIGHT_THEME = {
    "primaryColor": "#1f77b4",
    "backgroundColor": "#ffffff",
    "secondaryBackgroundColor": "#f0f2f6",
    "textColor": "#000000",
    "font": "sans serif"
}

DARK_THEME = {
    "primaryColor": "#1f77b4",
    "backgroundColor": "#0e1117",
    "secondaryBackgroundColor": "#262730",
    "textColor": "#fafafa",
    "font": "sans serif"
}

def apply_theme(theme_name):
    st.session_state["theme"] = theme_name
    # Removed st.experimental_rerun() due to compatibility
    st.info("Please refresh the browser page to apply theme changes.")

if "theme" not in st.session_state:
    st.session_state["theme"] = "light"

st.set_page_config(
    page_title="🌟 Zephyr Trend Dashboard (Dark Mode)",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.title("Settings")
theme_choice = st.sidebar.radio("Select Theme:", ("Light", "Dark"), index=0 if st.session_state["theme"]=="light" else 1)

if (theme_choice == "Light" and st.session_state["theme"] == "dark") or \
   (theme_choice == "Dark" and st.session_state["theme"] == "light"):
    st.sidebar.warning("Theme change requires dashboard refresh.")
    if st.sidebar.button("Confirm Theme Change"):
        apply_theme(theme_choice.lower())

st.title(f"🌟 Zephyr Trend Dashboard (Theme: {st.session_state['theme'].capitalize()})")

# Connect to DB and load data
conn = sqlite3.connect(r"D:\MAGIC\outputs\zephyr_trends.db")

selected_platforms = st.sidebar.multiselect(
    "Select platforms:", ["google_trends", "youtube_autocomplete", "reddit", "tiktok", "amazon"],
    default=["google_trends", "youtube_autocomplete"]
)

today = datetime.today().date()
start_date = st.sidebar.date_input("Start date", today - timedelta(days=30))
end_date = st.sidebar.date_input("End date", today)

if start_date > end_date:
    st.sidebar.error("Start date must be before end date.")

keyword_filter = st.sidebar.text_input("Keyword filter (substring):", "")

query = f"""
SELECT date, keyword, platform, metric FROM trends
WHERE platform IN ({','.join(['?']*len(selected_platforms))})
AND date BETWEEN ? AND ?
"""

params = selected_platforms + [start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")]
df = pd.read_sql_query(query, conn, params=params)

if keyword_filter:
    df = df[df['keyword'].str.contains(keyword_filter, case=False, na=False)]

conn.close()

if df.empty:
    st.warning("No data found for the selected filters.")
else:
    st.dataframe(df)
