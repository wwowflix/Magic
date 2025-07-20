""" 
insert_to_db.py 🔽
Part of Zephyr – Phase 2, Module G (G.2.45)

✅ Purpose:
Insert cleaned trend data into SQLite DB for dashboard access.

🧠 Inputs:
- List[Dict] or pandas.DataFrame of trend items
- Table name (e.g., "reddit_scrape", "google_trends")

📤 Output:
- SQLite DB updated at outputs/mydata.db
"""

import os
import sqlite3
import pandas as pd

DB_PATH = "outputs/mydata.db"

def insert_to_db(data, table_name="trend_data"):
    """Insert trend data into SQLite database."""
    try:
        if isinstance(data, list):
            data = pd.DataFrame(data)

        if data.empty:
            raise ValueError("Data is empty, nothing to insert.")

        os.makedirs("outputs", exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        data.to_sql(table_name, conn, if_exists="append", index=False)
        conn.close()
        print(f"✅ Inserted {len(data)} records into table '{table_name}' in {DB_PATH}")
    except Exception as e:
        print(f"❌ Failed to insert data into DB: {e}")
