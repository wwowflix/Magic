import sys, sqlite3, json
db = sys.argv[1]
out = {"ok": False, "tables": [], "counts": {}, "last_ts": None}
try:
    con = sqlite3.connect(db); cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'"); out["tables"] = [r[0] for r in cur.fetchall()]
    if "google_trends" in out["tables"]:
        try:
            cur.execute("SELECT COUNT(*) FROM google_trends"); out["counts"]["google_trends"] = cur.fetchone()[0]
        except Exception as e:
            out["counts"]["google_trends_err"] = str(e)
        for col in ("ts","fetched_at","timestamp","datetime","date","time","created_at"):
            try:
                cur.execute(f"SELECT {col} FROM google_trends ORDER BY ROWID DESC LIMIT 1")
                r = cur.fetchone()
                if r and r[0] is not None:
                    out["last_ts"] = {"column": col, "value": str(r[0])}; break
            except Exception:
                pass
    out["ok"] = True
except Exception as e:
    out["error"] = str(e)
print(json.dumps(out))
