import sqlite3

conn = sqlite3.connect('outputs/mydata.db')
cursor = conn.cursor()

for table in ['reddit', 'tiktok']:
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()
    print(f"Columns in {table}: {[col[1] for col in columns]}")

conn.close()
