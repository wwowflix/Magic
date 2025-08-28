# -*- coding: utf-8 -*-
import sqlite3

conn = sqlite3.connect("zephyr_trends.db")
cur = conn.cursor()

tables = ["google_trends", "reddit", "youtube", "tiktok"]
for table in tables:
    cur.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {table} (
            date TEXT,
            keyword TEXT,
            metric TEXT,
            platform TEXT,
            author TEXT
        )
    """
    )
    print(f"OK Created table {table}")

conn.commit()
conn.close()
