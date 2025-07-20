import sqlite3
conn = sqlite3.connect("outputs/mydata.db")

tables_columns = {
    "google_trends": ["term", "region", "score"],
    "reddit": ["subreddit", "title", "score"],
    "youtube": ["video_id", "title", "views"],
    "tiktok": ["hashtag", "desc", "likes"]
}

for table, columns in tables_columns.items():
    try:
        group_by_cols = ", ".join(columns)
        conn.execute(f'''
        DELETE FROM {table}
        WHERE rowid NOT IN (
            SELECT MIN(rowid)
            FROM {table}
            GROUP BY {group_by_cols}
        )
        ''')
        print(f"✅ Deduplicated: {table}")
    except Exception as e:
        print(f"⚠️ Error deduplicating {table}: {e}")

conn.commit()
conn.close()
