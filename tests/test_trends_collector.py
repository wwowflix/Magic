import sqlite3
import types
import pandas as pd

# Import the collector module under test
import importlib
gtf = importlib.import_module("scripts.collect.google_trends_fetcher")

class _StubTrendReq:
    def __init__(self, *a, **kw):
        pass
    def build_payload(self, kws, timeframe="now 7-d", geo=""):
        # remember the single-key list passed in
        self._kw = kws[0]
        self._geo = geo
        self._tf  = timeframe
    def interest_over_time(self):
        # Minimal shape that pytrends would return:
        # a column for the keyword + 'isPartial'
        return pd.DataFrame({
            self._kw: [10, 20],     # pretend interest values
            "isPartial": [False, False]
        })

def test_upsert_trends_inserts_rows(monkeypatch, tmp_db_path):
    # Redirect DB to a temp file, and mock TrendReq → no network
    monkeypatch.setattr(gtf, "DB_PATH", tmp_db_path, raising=False)
    monkeypatch.setattr(gtf, "TrendReq", _StubTrendReq, raising=False)

    # Ensure schema & run insert
    gtf.ensure_db()
    n = gtf.upsert_trends(["chatgpt", "python"], ["US"], "now 7-d")
    assert n == 2  # one row per keyword×region combo in our stub (2×1)

    # Verify rows in the temp DB
    con = sqlite3.connect(tmp_db_path)
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM google_trends")
    cnt = cur.fetchone()[0]
    con.close()
    assert cnt == 2
