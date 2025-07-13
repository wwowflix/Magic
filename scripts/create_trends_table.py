import sqlite3
import os

# Define DB path
db_path = r"D:\MAGIC\outputs\zephyr_trends.db"

# Ensure outputs folder exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Connect to SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS trends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    keyword TEXT,
    platform TEXT,
    metric REAL
);
""")

conn.commit()
conn.close()

print("✅ Trends table created successfully at:", db_path)
