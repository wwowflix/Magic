# -*- coding: utf-8 -*-
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Interactive Plotly Line Chart
def show_interactive_chart(csv_file):
    print("-> Running Interactive Plotly Chart...")
    df = pd.read_csv(csv_file)
    fig = px.line(df, x="date", y="value", title="Trend Over Time", hover_data=["keyword"])
    fig.show()

# Keyword Trend Over Time
def keyword_trend_over_time(csv_file, keyword):
    print("-> Running Keyword Trend Over Time...")
    df = pd.read_csv(csv_file)
    df_filtered = df[df["keyword"] == keyword]
    fig = px.line(df_filtered, x="date", y="value", title=f"Trend for {keyword}")
    fig.show()

# Platform Comparison Chart
def platform_comparison_chart():
    print("-> Running Platform Comparison Chart...")
    df = pd.DataFrame({
        "Platform": ["Google", "TikTok", "YouTube"],
        "Score": [80, 65, 50]
    })
    fig = px.bar(df, x="Platform", y="Score", color="Platform", title="Platform Comparison")
    fig.show()

# Word Cloud / Heatmap
def create_word_cloud(csv_file):
    print("-> Running Word Cloud...")
    df = pd.read_csv(csv_file)
    text = " ".join(df["keyword"].astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    # Replace with your CSV file path if different
    csv_file = "outputs/google_trends.csv"

    # Run all visualizations
    show_interactive_chart(csv_file)
    keyword_trend_over_time(csv_file, "ai tools")
    platform_comparison_chart()
    create_word_cloud(csv_file)



