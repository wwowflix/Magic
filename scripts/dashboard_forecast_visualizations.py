import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def load_forecast_data():
    # For demo, load forecast data from a CSV or DB table
    # Replace with your actual forecast data source
    try:
        df = pd.read_csv(r"D:\MAGIC\outputs\forecast_data.csv", parse_dates=["date"])
    except Exception:
        # Dummy forecast data fallback
        dates = pd.date_range(start=datetime.today() - timedelta(days=30), periods=30)
        df = pd.DataFrame({
            "date": dates,
            "forecast": [50 + i*2 for i in range(30)],
            "lower_ci": [45 + i*2 for i in range(30)],
            "upper_ci": [55 + i*2 for i in range(30)],
            "keyword": ["example_keyword"]*30
        })
    return df

st.set_page_config(layout="wide")
st.title("🌟 Zephyr Trend Dashboard (Sprint 6: Forecast Visualizations)")

df_forecast = load_forecast_data()

keywords = df_forecast["keyword"].unique().tolist()
selected_keyword = st.sidebar.selectbox("Select Keyword:", keywords)

df_plot = df_forecast[df_forecast["keyword"] == selected_keyword]

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df_plot["date"], df_plot["forecast"], label="Forecast", color="blue")
ax.fill_between(df_plot["date"], df_plot["lower_ci"], df_plot["upper_ci"], color="blue", alpha=0.2, label="Confidence Interval")
ax.set_title(f"Forecast for '{selected_keyword}'")
ax.set_xlabel("Date")
ax.set_ylabel("Metric")
ax.legend()

st.pyplot(fig)
