import streamlit as st
import pandas as pd
import subprocess

st.title("🔄 Dashboard with Auto Refresh")

csv_file = "outputs/google_trends.csv"

# Dummy refresh logic
if st.button("🔁 Refresh Data"):
    st.write("→ Running refresh script...")
    # You can replace this with:
    # subprocess.run(["python", "your_scraper.py"])
    result = subprocess.run(["python", "trends_scraper.py"])
    st.write("✅ Refresh finished!")

# Always show data
try:
    df = pd.read_csv(csv_file)
    st.dataframe(df)
except FileNotFoundError:
    st.warning("CSV file not found. Run the scraper first!")
