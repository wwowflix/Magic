import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import json

st.set_page_config(layout="wide")
st.title("🌟 Zephyr Trend Dashboard with Authentication")

# Sample users - replace with your secure hash storage
names = ["Admin User", "Test User"]
usernames = ["admin", "testuser"]
passwords = ["adminpass", "testpass"]

hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
                                    "zephyr_dashboard", "abcdef", cookie_expiry_days=1)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.sidebar.write(f"Welcome, {name}!")

    # Connect to DB and show dashboard content here
    conn = sqlite3.connect(r"D:\MAGIC\outputs\zephyr_trends.db")

    # Your dashboard code...

    conn.close()
elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")
