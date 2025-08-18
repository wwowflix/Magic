# -*- coding: utf-8 -*-
import praw
from vault_manager import load_secret

client_id = load_secret("REDDIT_CLIENT_ID")
client_secret = load_secret("REDDIT_CLIENT_SECRET")
user_agent = load_secret("REDDIT_USER_AGENT")

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

print("🔎 Reddit read_only:", reddit.read_only)

for submission in reddit.subreddit("python").hot(limit=3):
    print(f"✅ {submission.title} | Score: {submission.score}")
