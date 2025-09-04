# -*- coding: utf-8 -*-
import sqlite3

conn = sqlite3.connect("zephyr_trends.db")
cur = conn.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cur.fetchall()
print("Tables in zephyr_trends.db:")
for t in tables:
    print("-", t[0])

conn.close()
