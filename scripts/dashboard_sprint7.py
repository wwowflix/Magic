import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from io import BytesIO
import base64

# -------------------------
# Simple in-memory user auth (demo only)
# Replace with real auth in production
USERS = {"admin": "password123", "user": "pass"}

def login():
    st.sidebar.subheader("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if USERS.get(username) == password:
            st.session_state["user"] = username
            st.sidebar.success(f"Logged in as {username}")
        else:
            st.sidebar.error("Invalid credentials")
    return st.session_state.get("user", None)

def logout():
    if st.sidebar.button("Logout"):
        st.session_state.pop("user", None)
        st.experimental_rerun()

def query_trends(platforms, start_date, end_date, keyword_filter):
    conn = sqlite3.connect(r"D:\MAGIC\outputs\zephyr_trends.db")
    try:
        query = f"""
        SELECT date, keyword, platform, metric FROM trends
        WHERE platform IN ({','.join(['?']*len(platforms))})
        AND date BETWEEN ? AND ?
        """
        params = platforms + [start_date, end_date]
        df = pd.read_sql_query(query, conn, params=params)
        if keyword_filter:
            df = df[df["keyword"].str.contains(keyword_filter, case=False, na=False)]
        return df
    finally:
        conn.close()

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Trends")
        # writer.save() removed to fix AttributeError
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):
    val = to_excel(df)
    b64 = base64.b64encode(val).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="trends_report.xlsx">Download Excel Report</a>'
    return href

def get_csv_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="trends_report.csv">Download CSV Report</a>'
    return href

# Streamlit app starts here
st.set_page_config(layout="wide")
st.title("🌟 Zephyr Trend Dashboard (Sprint 7: Reports & Auth)")

user = login()

if user:
    logout()

    all_platforms = ["google_trends", "youtube_autocomplete", "reddit", "tiktok", "amazon"]
    selected_platforms = st.sidebar.multiselect("Select platforms:", all_platforms, default=["google_trends", "youtube_autocomplete"])

    today = datetime.today().date()
    start_date = st.sidebar.date_input("Start date", today - timedelta(days=30))
    end_date = st.sidebar.date_input("End date", today)
    if start_date > end_date:
        st.sidebar.error("Start date must be before end date.")

    keyword_filter = st.sidebar.text_input("Keyword filter (substring):", "")

    df = query_trends(selected_platforms, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), keyword_filter)

    if df.empty:
        st.warning("No data found for the selected filters.")
    else:
        st.dataframe(df)

        st.markdown(get_csv_download_link(df), unsafe_allow_html=True)
        st.markdown(get_table_download_link(df), unsafe_allow_html=True)

    st.markdown("---")
    st.header("Custom Domain Setup")
    st.info("To deploy your dashboard with a custom domain and SSL, configure your hosting provider and DNS settings accordingly. This is outside Streamlit code scope.")

    st.markdown("---")
    st.header("Embed Dashboard")
    st.info("You can embed this dashboard into other websites via iframe or Streamlit sharing links.")

else:
    st.info("Please log in to access the dashboard features.")
