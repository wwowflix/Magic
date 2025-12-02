import os, sqlite3, pandas as pd
import streamlit as st
from datetime import datetime, timedelta

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB = os.path.join(ROOT, "outputs", "mydata.db")

st.set_page_config(page_title="MAGIC - Ops", layout="wide", page_icon="ðŸª„")
st.title("ðŸª„ MAGIC - Autonomous Ops Dashboard")

if not os.path.exists(DB):
    st.error(f"DB not found: {DB}")
    st.stop()

# Sidebar controls
days = st.sidebar.slider("Trends window (days)", 1, 30, 7)
since = (datetime.utcnow() - timedelta(days=days)).isoformat()


def read_sql(sql, params=None):
    with sqlite3.connect(DB) as con:
        return pd.read_sql_query(sql, con, params=params or ())


# --- Section: Source of Truth (magic_status) ---
st.subheader("âš™ï¸ System Source of Truth")

try:
    ms = read_sql(
        "SELECT component, metric, status, details, observed_at FROM magic_status ORDER BY component, metric"
    )
    if ms.empty:
        st.info("No rows in magic_status yet. Run: tools\\refresh_sot.ps1")
    else:
        # KPIs
        ok = (ms.status == "ok").sum()
        warn = (ms.status == "warn").sum()
        err = (ms.status == "error").sum()
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("OK", ok)
        c2.metric("WARN", warn)
        c3.metric("ERROR", err)
        c4.metric("Components", ms["component"].nunique())

        st.dataframe(ms, use_container_width=True, height=300)
except Exception as e:
    st.error(f"Failed to read magic_status: {e}")

st.divider()

# --- Section: Trends (google_trends) ---
st.subheader("ðŸ“ˆ Trends (google_trends)")

try:
    df = read_sql(
        "SELECT keyword, region, ts, value FROM google_trends WHERE ts >= ?",
        params=(since,),
    )
    if df.empty:
        st.info("No google_trends rows in window. (Collector may be pending.)")
    else:
        # Timestamp parse
        def _p(x):
            try:
                return pd.to_datetime(x, utc=True)
            except:
                return pd.NaT

        df["ts_dt"] = df["ts"].apply(_p)
        df = df.dropna(subset=["ts_dt"]).sort_values("ts_dt")
        df["series"] = df["keyword"] + " | " + df["region"]

        # Small aggregation to keep chart readable
        # (sum by ts & series; if duplicates exist)
        pivot = df.pivot_table(
            index="ts_dt", columns="series", values="value", aggfunc="sum"
        ).sort_index()
        st.line_chart(pivot)

        with st.expander("Recent rows"):
            st.dataframe(df.tail(50), use_container_width=True, height=260)
except Exception as e:
    st.error(f"Failed to read google_trends: {e}")

st.caption("DB: " + DB)
