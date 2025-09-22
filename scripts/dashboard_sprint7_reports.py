import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import io

st.set_page_config(layout="wide")
st.title("🌟 Zephyr Trend Dashboard - Download Reports")

conn = sqlite3.connect(r"D:\MAGIC\outputs\zephyr_trends.db")

platforms = ["google_trends", "youtube_autocomplete", "reddit", "tiktok", "amazon"]
selected_platforms = st.sidebar.multiselect("Select platforms:", platforms, default=platforms)

today = datetime.today().date()
start_date = st.sidebar.date_input("Start date", today - timedelta(days=30))
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

st.dataframe(df)

# Excel download
def to_excel(dataframe):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        dataframe.to_excel(writer, index=False, sheet_name="Trends")
        writer.save()
    processed_data = output.getvalue()
    return processed_data

excel_data = to_excel(df)

st.download_button(
    label="Download data as Excel",
    data=excel_data,
    file_name=f"zephyr_trends_{start_date}_{end_date}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# CSV download
csv_data = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download data as CSV",
    data=csv_data,
    file_name=f"zephyr_trends_{start_date}_{end_date}.csv",
    mime="text/csv"
)

conn.close()
