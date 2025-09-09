from secrets import *

from praw import Reddit

print("ðŸ” Logging in to Reddit...")

reddit = Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD,
)

try:
    me = reddit.user.me()
    print(f"âœ… Logged in as: u/{me}")
except Exception as e:
    print(f"âŒ Login failed: {e}")
