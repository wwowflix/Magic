import os, sqlite3, pandas as pd
import streamlit as st
from datetime import datetime, timedelta, timezone
import math

DB = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "outputs", "mydata.db")
)

st.set_page_config(page_title="MAGIC ÃƒÂ¢Ã¢"šÂ¬Ã¢â‚¬Å“ Trends", layout="wide")
st.title("ÃƒÂ°Ã…Â¸Ã‚Â§Ã‚ MAGIC ÃƒÂ¢Ã¢"šÂ¬Ã¢â‚¬Å“ Trends Mini Dashboard")

if not os.path.exists(DB):
    st.error(f"DB not found: {DB}")
    st.stop()

# Controls
days = st.sidebar.slider("Days window", 1, 30, 7)


def _detect_ts_col(con):
    cur = con.cursor()
    cur.execute("PRAGMA table_info(google_trends)")
    cols = cur.fetchall()
    names = [r[1].lower() for r in cols]
    # remember what we saw for debugging
    st.session_state["_gt_cols"] = names
    for cand in [
        "ts",
        "timestamp",
        "datetime",
        "date",
        "time",
        "created_at",
        "fetched_at",
    ]:
        if cand in names:
            return cand
    return None


def _to_utc_datetime(x):
    # Accept epoch (int/float/str) or ISO-like text
    try:
        if isinstance(x, (int, float)) and not (
            isinstance(x, float) and (math.isnan(x) or math.isinf(x))
        ):
            return pd.to_datetime(x, unit="s", utc=True)
        if isinstance(x, str) and x.isdigit():
            return pd.to_datetime(int(x), unit="s", utc=True)
        return pd.to_datetime(x, utc=True, errors="coerce")
    except Exception:
        return pd.NaT


with sqlite3.connect(DB) as con:
    # detect timestamp column
    ts_col = _detect_ts_col(con)
    if not ts_col:
        st.error(
            "`google_trends` has no timestamp-like column. Expected one of: ts, timestamp, datetime, date, time, created_at.\n"
            f"Columns seen: {st.session_state.get('_gt_cols', [])}"
        )
        st.stop()

    # ensure value column exists (common names: value, interest, score)
    cur = con.cursor()
    cur.execute("PRAGMA table_info(google_trends)")
    colnames = [r[1].lower() for r in cur.fetchall()]
    value_col = None
    for cand in ["value", "interest", "score"]:
        if cand in colnames:
            value_col = cand
            break
    if value_col is None:
        st.error(
            "`google_trends` table missing a numeric value column (tried: value, interest, score). "
            f"Columns seen: {colnames}"
        )
        st.stop()

    # keyword/region may vary; fetch superset then project to standard names
    wanted = ["keyword", "region", ts_col, value_col]
    sel = []
    for w in wanted:
        if w == ts_col:
            sel.append(f'"{ts_col}" AS ts_any')
        elif w == value_col:
            sel.append(f'"{value_col}" AS val_any')
        else:
            if w in colnames:
                sel.append(w)
            else:
                # tolerate missing text dims by emitting NULLs
                sel.append(f"NULL AS {w}")
    query = "SELECT " + ", ".join(sel) + " FROM google_trends"
    df = pd.read_sql_query(query, con)

if df.empty:
    st.info("No rows in table.")
    st.stop()

# parse UTC datetime
df["ts_dt"] = df["ts_any"].apply(_to_utc_datetime)
df = df.dropna(subset=["ts_dt"]).copy()
df = df.sort_values("ts_dt")

# filter by days window
cutoff = datetime.now(timezone.utc) - timedelta(days=days)
df = df[df["ts_dt"] >= cutoff]

if df.empty:
    st.info("No rows in selected window.")
    st.stop()

# Filters
kw_options = sorted(df["keyword"].dropna().astype(str).unique().tolist())
rg_options = sorted(df["region"].dropna().astype(str).unique().tolist())
sel_kw = st.sidebar.multiselect(
    "Keywords", kw_options, kw_options[:3] if len(kw_options) >= 3 else kw_options
)
sel_rg = st.sidebar.multiselect(
    "Regions", rg_options, rg_options[:2] if len(rg_options) >= 2 else rg_options
)
if sel_kw:
    df = df[df["keyword"].astype(str).isin(sel_kw)]
if sel_rg:
    df = df[df["region"].astype(str).isin(sel_rg)]

st.caption(
    "Last refresh: **{}Z**".format(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
)

# Series + chart
df["series"] = (
    df["keyword"].fillna("(none)").astype(str)
    + " | "
    + df["region"].fillna("(none)").astype(str)
)
st.line_chart(df.set_index("ts_dt")[["val_any"]].groupby([df["series"]]).sum())

# Tail table
st.dataframe(
    df[["ts_dt", "keyword", "region", "val_any"]].tail(25), use_container_width=True
)
