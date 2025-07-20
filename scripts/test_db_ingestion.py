import sqlite3
import pandas as pd

def test_insert_data():
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE trends (platform TEXT, title TEXT)
    """)
    data = pd.DataFrame({"platform": ["tiktok"], "title": ["Test Title"]})
    data.to_sql("trends", conn, if_exists="append", index=False)

    result = conn.execute("SELECT COUNT(*) FROM trends").fetchone()[0]
    assert result == 1
    conn.close()

