# -*- coding: utf-8 -*-
import praw
import sys

try:
    reddit = praw.Reddit(
        client_id="your_real_client_id_here",
        client_secret="your_real_client_secret_here",
        user_agent="MAGICZephyrBot/1.0 by u/yourusername",
    )
    # Minimal API call
    print("?? Reddit read_only:", reddit.read_only)
    for submission in reddit.subreddit("python").hot(limit=1):
        print("[OK] TEST OK:", submission.title, submission.score)

except Exception as e:
    print("? Reddit API Error:", e)
    sys.exit(1)
