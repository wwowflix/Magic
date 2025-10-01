import os
from dotenv import load_dotenv

load_dotenv(r"D:\MAGIC\.env")

keys = [
    "OPENAI_API_KEY",
    "NOTION_TOKEN",
    "NOTION_DATABASE_ID",
    "REDDIT_CLIENT_ID",
    "REDDIT_CLIENT_SECRET",
    "CODECOV_TOKEN",
    "GITHUB_TOKEN",
]

for key in keys:
    val = os.getenv(key)
    if val:
        print(f"{key}: OK ✅")
    else:
        print(f"{key}: MISSING ❌")
