import sqlite3
import pandas as pd

def test_tiktok_query_returns_data():
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE trends (platform TEXT, title TEXT)
    """)
    conn.execute("""
        INSERT INTO trends (platform, title) VALUES ('tiktok', 'Test Video')
    """)
    df = pd.read_sql_query(
        "SELECT * FROM trends WHERE platform = 'tiktok'",
        conn
    )
    assert not df.empty
    conn.close()
