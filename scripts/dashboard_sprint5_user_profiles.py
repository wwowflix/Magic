import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import json
import streamlit_authenticator as stauth

st.set_page_config(layout="wide")
st.title("🌟 Zephyr Trend Dashboard with User Profiles")

# --- Authentication Setup ---
names = ["Admin", "User1"]
usernames = ["admin", "user1"]
passwords = ["password123", "password456"]  # Use hashed passwords in production

hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "zephyr_dashboard", "abcdef", cookie_expiry_days=1)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.sidebar.write(f"Welcome, {name}!")
    
    # Load or create user settings
    settings_file = f"user_settings_{username}.json"
    
    try:
        with open(settings_file, "r") as f:
            user_settings = json.load(f)
    except FileNotFoundError:
        user_settings = {
            "platforms": ["google_trends", "youtube_autocomplete"],
            "start_date": (datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d"),
            "end_date": datetime.today().strftime("%Y-%m-%d"),
            "keyword_filter": ""
        }

    # Sidebar filters with saved defaults
    platforms = ["google_trends", "youtube_autocomplete", "reddit", "tiktok", "amazon"]
    selected_platforms = st.sidebar.multiselect(
        "Select platforms:",
        platforms,
        default=user_settings.get("platforms", platforms)
    )
    
    start_date = st.sidebar.date_input(
        "Start date",
        datetime.strptime(user_settings.get("start_date"), "%Y-%m-%d")
    )
    
    end_date = st.sidebar.date_input(
        "End date",
        datetime.strptime(user_settings.get("end_date"), "%Y-%m-%d")
    )
    
    keyword_filter = st.sidebar.text_input(
        "Keyword filter (substring):",
        value=user_settings.get("keyword_filter", "")
    )
    
    # Save updated settings
    if st.sidebar.button("Save Settings"):
        user_settings = {
            "platforms": selected_platforms,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "keyword_filter": keyword_filter
        }
        with open(settings_file, "w") as f:
            json.dump(user_settings, f)
        st.sidebar.success("Settings saved!")
    
    # Load data and display as usual
    conn = sqlite3.connect(r"D:\MAGIC\outputs\zephyr_trends.db")
    
    if start_date > end_date:
        st.sidebar.error("Start date must be before end date.")
    
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
    
    st.dataframe(df)
    conn.close()
    
elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")
