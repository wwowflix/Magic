# -*- coding: utf-8 -*-
import streamlit as st
import sqlite3
import pandas as pd
import altair as alt

st.set_page_config(page_title="Magic Dashboard", layout="wide")

if "theme" not in st.session_state:
    st.session_state["theme"] = "light"

theme_choice = st.sidebar.radio(
    "Select Theme:",
    ("Light", "Dark"),
    index=0 if st.session_state["theme"] == "light" else 1,
)

if theme_choice != st.session_state["theme"]:
    st.session_state["theme"] = theme_choice
    st.rerun()

if st.session_state["theme"] == "dark":
    st.markdown(
        """
        <style>
            body { background-color: #111111; color: #FFFFFF; }
            .stDataFrame { background-color: #222222; color: #FFFFFF; }
        </style>
        """,
        unsafe_allow_html=True,
    )

DB_PATH = r"D:\MAGIC\outputs\mydata.db"

try:
    conn = sqlite3.connect(DB_PATH)
except Exception as e:
    st.error(f"Could not connect to DB:\n{e}")
    st.stop()

st.sidebar.header("Filters")

platforms = st.sidebar.multiselect(
    "Select Platforms:",
    ["google_trends", "reddit_scrape", "youtube_scrape"],
    default=["google_trends", "reddit_scrape", "youtube_scrape"],
)

keyword_filter = st.sidebar.text_input("Keyword filter (substring):", "")

tables = {
    "google_trends": None,
    "reddit_scrape": None,
    "youtube_scrape": None,
}

for platform in tables.keys():
    if platform in platforms:
        try:
            df = pd.read_sql(f"SELECT * FROM {platform}", conn)
            if keyword_filter and "keyword" in df.columns:
                df = df[df["keyword"].str.contains(keyword_filter, case=False, na=False)]
            tables[platform] = df
        except Exception as e:
            st.warning(f"Could not read table {platform}: {e}")

for name, df in tables.items():
    if df is not None:
        st.header(f"{name} Data")
        st.write(df)

        if "keyword" in df.columns:
            chart = (
                alt.Chart(df)
                .mark_bar()
                .encode(
                    x=alt.X("keyword:N", sort="-y"),
                    y="count():Q",
                )
                .properties(width=700, height=300)
            )
            st.altair_chart(chart, use_container_width=True)

conn.close()
