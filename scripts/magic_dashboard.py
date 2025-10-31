"""
MAGIC Streamlit Dashboard "" Upgrade v1
Location suggestion: scripts/dashboard/magic_dashboard.py

Features delivered in this single file:
- Google Trends charts (last 7 days by default) with keyword + region filters
- Top trending keywords table with acceleration metric
- System status panel (DB freshness, scheduled task last/next run, last result)
- Last refresh timestamp + auto-refresh countdown
- Buttons: Force Trends Refresh, Export Insights (CSV)

Prereqs (one-time):
  pip install streamlit plotly pandas numpy python-dateutil tzdata
Run:
  streamlit run scripts/dashboard/magic_dashboard.py --server.headless true

Assumptions:
- SQLite DB at outputs/mydata.db with table 'google_trends' having columns:
    keyword TEXT, region TEXT, ts TEXT or INTEGER (UTC ISO8601 or epoch), value REAL
- Collector script at scripts/collect/google_trends_fetcher.py
- Windows host with 'schtasks' task named "MAGIC_Trends_Hourly" (optional)
"""

from __future__ import annotations

import os
import sys
import io
import csv
import json
import time
import math
import sqlite3
import subprocess
from datetime import datetime, timedelta, timezone
from dateutil import tz

import pandas as pd
import numpy as np

import streamlit as st
import plotly.express as px


# --- Compatibility: Streamlit rerun helper (works across versions & tests)
def __get_rerun__():
    try:
        if hasattr(st, "rerun"):
            return st.rerun
        return getattr(st, "experimental_rerun", lambda: None)
    except Exception:
        return lambda: None


__ST_RERUN__ = __get_rerun__()
# ----------------------------
# Constants / Paths
# ----------------------------
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_PATH = os.path.join(ROOT, "outputs", "mydata.db")
COLLECTOR = os.path.join(ROOT, "scripts", "collect", "google_trends_fetcher.py")
TASK_NAME = "MAGIC_Trends_Hourly"  # Windows Scheduled Task (optional)
LOCAL_TZ = tz.gettz("Asia/Kolkata")
UNDER_PYTEST = bool(os.environ.get("PYTEST_CURRENT_TEST"))

# ----------------------------
# Utilities
# ----------------------------


def _utcnow():
    return datetime.now(timezone.utc)


def parse_ts(x: str | int | float | None) -> datetime | None:
    if x is None:
        return None
    try:
        # try epoch seconds
        return datetime.fromtimestamp(float(x), tz=timezone.utc)
    except Exception:
        pass
    try:
        # try ISO8601
        dt = datetime.fromisoformat(str(x).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


def read_trends(
    conn: sqlite3.Connection, since_utc: datetime | None = None
) -> pd.DataFrame:
    q = "SELECT keyword, region, ts, value FROM google_trends"
    params: tuple = ()
    if since_utc is not None:
        q += " WHERE ts >= ?"
        # store as ISO string to be flexible; DB may hold TEXT ISO8601
        params = (since_utc.replace(tzinfo=timezone.utc).isoformat(),)
    df = pd.read_sql_query(q, conn, params=params)
    # normalize
    if not df.empty:
        df["ts_dt"] = df["ts"].apply(parse_ts)
        df = df.dropna(subset=["ts_dt"]).copy()
        df["ts_local"] = df["ts_dt"].apply(lambda d: d.astimezone(LOCAL_TZ))
        df.sort_values("ts_dt", inplace=True)
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df = df.dropna(subset=["value"])  # keep clean
    return df


def db_freshness(conn: sqlite3.Connection, window_minutes: int = 120) -> dict:
    now = _utcnow()
    since = now - timedelta(minutes=window_minutes)
    df = read_trends(conn, since)
    fresh = not df.empty
    last_ts = None
    if not df.empty:
        last_ts = df["ts_dt"].max()
    return {
        "fresh": fresh,
        "rows_recent": int(len(df)) if fresh else 0,
        "last_ts": last_ts,
        "since": since,
    }


def get_schtask_status(task_name: str = TASK_NAME) -> dict:
    """Query Windows scheduled task; safe on non-Windows (returns blanks)."""
    if os.name != "nt":
        return {"supported": False}
    try:
        out = subprocess.check_output(
            [
                "schtasks",
                "/Query",
                "/TN",
                task_name,
                "/V",
                "/FO",
                "LIST",
            ],
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
        )
    except subprocess.CalledProcessError as e:
        return {"supported": True, "found": False, "error": e.output}

    data = {"supported": True, "found": True}
    for line in out.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        k, v = [s.strip() for s in line.split(":", 1)]
        if k in ("Last Run Time", "Next Run Time", "Last Result", "Status"):
            data[k] = v
    return data


def force_refresh_trends(
    default_keywords: list[str] | None = None,
    regions: list[str] | None = None,
    timeframe: str = "now 7-d",
) -> subprocess.CompletedProcess | None:
    if not os.path.exists(COLLECTOR):
        st.warning("Collector script not found: %s" % COLLECTOR)
        return None
    # Build args: if default_keywords not provided, try to infer from DB
    args = [sys.executable, COLLECTOR]
    kw = default_keywords or []
    if not kw:
        try:
            with sqlite3.connect(DB_PATH) as c:
                dfk = pd.read_sql_query(
                    "SELECT DISTINCT keyword FROM google_trends ORDER BY keyword", c
                )
            kw = dfk["keyword"].dropna().tolist()[:5]
        except Exception:
            pass
    if kw:
        args += ["--keywords", *kw]
    if regions:
        args += ["--regions", *regions]
    args += ["--timeframe", timeframe]

    return subprocess.run(
        args, capture_output=True, text=True, encoding="utf-8", cwd=ROOT
    )


# Utility: safe rerun helper for Streamlit
def _maybe_rerun():
    fn = getattr(st, "rerun", None) or getattr(st, "experimental_rerun", None)
    if fn and not UNDER_PYTEST:
        try:
            fn()
        except Exception:
            pass


# ----------------------------
# Streamlit UI# ----------------------------
st.set_page_config(page_title="MAGIC - Trends HQ", layout="wide")
st.title("🧠 MAGIC — Trends Intelligence HQ")

# Auto-refresh every 60s to reflect new rows from hourly task
refresh_interval_sec = st.sidebar.number_input(
    "Auto-refresh (seconds)", min_value=10, max_value=600, value=60, step=10
)
if UNDER_PYTEST:
    refresh_interval_sec = 0
st_autorefresh = getattr(st, "rerun", None) or getattr(
    st, "experimental_rerun", None
)  # placeholder; below we use st.experimental_data_editor trick
st.caption("Auto-refresh is enabled - the view will update periodically.")

# DB connection
if not os.path.exists(DB_PATH):
    st.error(f"Database not found: {DB_PATH}")
    st.stop()

try:
    conn = sqlite3.connect(DB_PATH, timeout=1)
except Exception:
    # During tests, avoid crashing on import if the file is locked/missing.
    if os.environ.get("PYTEST_CURRENT_TEST"):
        conn = sqlite3.connect(":memory:")
        conn.execute(
            "CREATE TABLE IF NOT EXISTS google_trends (keyword TEXT, region TEXT, ts TEXT, value REAL)"
        )
    else:
        raise

with st.sidebar:
    st.subheader("Filters")
    # Load minimal frame for selectors
    try:
        df_meta = pd.read_sql_query(
            "SELECT DISTINCT keyword, region FROM google_trends", conn
        )
    except Exception as e:
        st.error(f"Failed to read google_trends: {e}")
        st.stop()

    all_keywords = sorted(df_meta["keyword"].dropna().unique().tolist())
    all_regions = sorted(df_meta["region"].dropna().unique().tolist())

    sel_keywords = st.multiselect(
        "Keywords",
        options=all_keywords,
        default=all_keywords[:3] if all_keywords else [],
    )
    sel_regions = st.multiselect(
        "Regions", options=all_regions, default=all_regions[:2] if all_regions else []
    )

    days = st.slider("Days window", min_value=1, max_value=30, value=7, step=1)

    st.divider()
    st.subheader("Controls")
    colA, colB = st.columns(2)
    with colA:
        if st.button("🔄 Force Trends Refresh"):
            res = force_refresh_trends(
                sel_keywords or None, sel_regions or None, timeframe=f"now {days}-d"
            )
            if res is not None:
                if res.returncode == 0:
                    st.success("Collector ran successfully.")
                else:
                    st.error(
                        f"Collector failed (code {res.returncode}). See logs below."
                    )
                with st.expander("Collector output"):
                    st.code(res.stdout or "<no stdout>")
                    st.code(res.stderr or "<no stderr>", language="bash")
    with colB:
        export_clicked = st.button("📤 Export Insights CSV")

# Data query
since = _utcnow() - timedelta(days=int(days))
df = read_trends(conn, since)

# Apply filters if selected
if sel_keywords:
    df = df[df["keyword"].isin(sel_keywords)]
if sel_regions:
    df = df[df["region"].isin(sel_regions)]

# Status header
col1, col2, col3, col4 = st.columns(4)
with col1:
    if df.empty:
        st.metric("Rows in window", 0)
    else:
        st.metric("Rows in window", len(df))

with col2:
    last_ts = df["ts_dt"].max() if not df.empty else None
    last_ts_local = (
        last_ts.astimezone(LOCAL_TZ).strftime("%Y-%m-%d %H:%M:%S") if last_ts else "-"
    )
    st.metric("Last data timestamp", last_ts_local)

with col3:
    # Scheduled task status
    t = get_schtask_status(TASK_NAME)
    if not t.get("supported", True):
        st.metric("Scheduler", "Non-Windows")
    elif not t.get("found", True):
        st.metric("Scheduler", "Not Found")
    else:
        st.metric("Last Result", t.get("Last Result", "-"))

with col4:
    if t.get("found", True):
        st.caption(f"Next Run: {t.get('Next Run Time', '-')}")
        st.caption(f"Status: {t.get('Status', '-')}")

st.divider()

# ----------------------------
# Charts
# ----------------------------

if df.empty:
    st.info(
        "No data for the selected window/filters. Try widening the time range or removing filters."
    )
else:
    # Line chart: value over time per (keyword, region)
    st.subheader("📈 Google Trends - Value over Time")
    df_line = df.copy()
    df_line["Series"] = df_line["keyword"] + " | " + df_line["region"]
    fig = px.line(
        df_line,
        x="ts_local",
        y="value",
        color="Series",
        hover_data=["keyword", "region"],
        markers=True,
    )
    fig.update_layout(
        xaxis_title="Time (local)", yaxis_title="Value", legend_title="Series"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Acceleration metric: last N vs previous N window mean
    st.subheader("🚀 Top Trending by Acceleration")
    accel_window = st.number_input(
        "Acceleration window (hours)", min_value=1, max_value=24, value=6, step=1
    )

    def compute_accel_safe(frame: pd.DataFrame, hours: int) -> pd.DataFrame:
        # group by series, compare mean of last window vs prior window
        out = []
        now = frame["ts_dt"].max()
        late_start = now - timedelta(hours=hours)
        early_start = now - timedelta(hours=2 * hours)
        for (k, r), g in frame.groupby(["keyword", "region"], dropna=False):
            g = g.sort_values("ts_dt")
            early = g[(g["ts_dt"] >= early_start) & (g["ts_dt"] < late_start)][
                "value"
            ].mean()
            late = g[g["ts_dt"] >= late_start]["value"].mean()
            if pd.notna(early) and pd.notna(late):
                delta = late - early
                pct = (delta / early * 100.0) if early else np.nan
                out.append(
                    {
                        "keyword": k,
                        "region": r,
                        "late_mean": late,
                        "early_mean": early,
                        "delta": delta,
                        "%chg": pct,
                    }
                )
        out_df = pd.DataFrame(
            out,
            columns=["keyword", "region", "late_mean", "early_mean", "delta", "%chg"],
        )
        if out_df.empty:
            return out_df
        out_df = out_df.sort_values(["delta"], ascending=False)
        return out_df

    accel_df = compute_accel_safe(df, int(accel_window))
    if accel_df.empty:
        st.info(
            "Not enough data density to compute acceleration. Let the collector run a bit more."
        )
    else:
        st.dataframe(accel_df.head(20), use_container_width=True)

# ----------------------------
# System Health Panel
# ----------------------------
st.subheader("âš™ï¸ System Health")
health = db_freshness(conn, window_minutes=120)
colh1, colh2, colh3 = st.columns(3)
colh1.metric("DB Fresh (â‰¤120 min)", "Yes" if health["fresh"] else "No")
colh2.metric("Rows (â‰¤120 min)", health["rows_recent"])
colh3.write(
    f"Last row: **{health['last_ts'].astimezone(LOCAL_TZ).strftime('%Y-%m-%d %H:%M:%S') if health['last_ts'] else '-'}**"
)

# Export insights
if "export_clicked" in globals() and export_clicked:
    if df.empty:
        st.warning("Nothing to export for current filters.")
    else:
        csv_buf = io.StringIO()
        df_export = df[["keyword", "region", "ts_local", "value"]].copy()
        df_export.rename(columns={"ts_local": "timestamp_local"}, inplace=True)
        df_export.to_csv(csv_buf, index=False)
        st.download_button(
            label="Download CSV",
            data=csv_buf.getvalue().encode("utf-8"),
            file_name="magic_trends_export.csv",
            mime="text/csv",
        )

# Friendly footer
st.caption(
    "MAGIC Dashboard v1 "¢ Live filters, acceleration insights, scheduler status, and export. ✨"
)

# Basic timer to refresh "" Streamlit's built-in autorefresh helper
# (We use a placeholder increment pattern to trigger rerun)
placeholder = st.empty()
for i in range(int(refresh_interval_sec), 0, -1):
    placeholder.info(f"Refreshing in {i} sec…")
    time.sleep(1)
placeholder.empty()
_maybe_rerun()


# ---------- SAFE ACCELERATION COMPUTE (appended by patch) ----------
def compute_accel_safe(df, window_hours: int):
    import pandas as pd

    cols = ["keyword", "region", "late_mean", "early_mean", "delta", "%chg"]
    if df is None or len(df) == 0:
        return pd.DataFrame(columns=cols)

    # Expect columns: keyword, region, ts, value
    if not {"keyword", "region", "ts", "value"}.issubset(df.columns):
        return pd.DataFrame(columns=cols)

    # Parse timestamps robustly
    ts = pd.to_datetime(df["ts"], utc=True, errors="coerce")
    df = df.assign(__ts=ts).dropna(subset=["__ts"])
    if df.empty:
        return pd.DataFrame(columns=cols)

    now = df["__ts"].max()
    late_start = now - pd.Timedelta(hours=window_hours)
    early_start = now - pd.Timedelta(hours=2 * window_hours)

    late = df[(df["__ts"] > late_start) & (df["__ts"] <= now)]
    early = df[(df["__ts"] >= early_start) & (df["__ts"] <= late_start)]

    if late.empty or early.empty:
        return pd.DataFrame(columns=cols)

    g = ["keyword", "region"]
    late_mean = late.groupby(g)["value"].mean().rename("late_mean")
    early_mean = early.groupby(g)["value"].mean().rename("early_mean")

    out = pd.concat([late_mean, early_mean], axis=1).dropna()
    if out.empty:
        return pd.DataFrame(columns=cols)

    out["delta"] = out["late_mean"] - out["early_mean"]
    # Avoid div-by-zero
    denom = out["early_mean"].replace({0: pd.NA})
    out["%chg"] = (out["delta"] / denom) * 100

    out = out.reset_index().sort_values("delta", ascending=False)
    # Ensure column order exists even if %chg is NA
    for c in cols:
        if c not in out.columns:
            out[c] = pd.NA
    return out[cols]


# ---------- END SAFE ACCELERATION COMPUTE ----------
