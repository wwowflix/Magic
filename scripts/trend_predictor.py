import pandas as pd
import numpy as np
import plotly.express as px

# Simulate daily search volumes
np.random.seed(42)
dates = pd.date_range(start="2024-01-01", periods=60)
values = np.random.poisson(lam=500, size=60)

# Add a sudden spike
values[30] += 1000

df = pd.DataFrame({
    "date": dates,
    "search_volume": values
})

# Simple anomaly detection: flag values > mean + 2*std
threshold = df["search_volume"].mean() + 2 * df["search_volume"].std()
df["anomaly"] = df["search_volume"] > threshold

fig = px.line(df, x="date", y="search_volume", title="Trend with Anomaly Detection")
fig.add_scatter(
    x=df.loc[df["anomaly"], "date"],
    y=df.loc[df["anomaly"], "search_volume"],
    mode="markers",
    marker=dict(color="red", size=10),
    name="Anomaly"
)

fig.show()
