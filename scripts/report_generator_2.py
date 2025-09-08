# -*- coding: utf-8 -*-
import pandas as pd
from fpdf import FPDF
import streamlit as st

st.title("?? PDF Report Generator")

try:
    df = pd.read_csv("outputs/google_trends.csv")
except FileNotFoundError:
    st.error("CSV not found!")
    st.stop()

st.dataframe(df.head())

if st.button("Generate PDF Report"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Trend Report", ln=True, align="C")

    for i, row in df.head(10).iterrows():
        pdf.cell(200, 10, txt=f"{row['date']} - {row['keyword']} - {row['value']}", ln=True)

    pdf.output("trend_report.pdf")
    st.success("[OK] PDF saved: trend_report.pdf")
