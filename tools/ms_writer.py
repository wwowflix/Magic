import sys, json, sqlite3
db, js = sys.argv[1], sys.argv[2]
rows = json.load(open(js, "r", encoding="utf-8-sig"))
con = sqlite3.connect(db); cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS magic_status(
  component   TEXT NOT NULL,
  metric      TEXT NOT NULL,
  status      TEXT NOT NULL,
  details     TEXT,
  observed_at TEXT NOT NULL,
  PRIMARY KEY(component, metric)
)""")
for r in rows:
    cur.execute("""INSERT INTO magic_status(component,metric,status,details,observed_at)
                   VALUES(?,?,?,?,?)
                   ON CONFLICT(component,metric)
                   DO UPDATE SET status=excluded.status,
                                 details=excluded.details,
                                 observed_at=excluded.observed_at""",
                (r["component"], r["metric"], r["status"], r.get("details",""), r["observed_at"]))
con.commit(); con.close()
print("magic_status updated:", len(rows))
