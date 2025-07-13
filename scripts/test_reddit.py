import sys
sys.path.append(r'D:\MAGIC\scripts')

from load_api_key import load_api_key
import praw

# Load credentials from vault
client_id = load_api_key("REDDIT_CLIENT_ID")
client_secret = load_api_key("REDDIT_CLIENT_SECRET")
user_agent = load_api_key("REDDIT_USER_AGENT")

print("Using CLIENT_ID:", client_id)
print("Using USER_AGENT:", user_agent)

# Initialize Reddit API client
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

# Test: fetch top 3 posts from r/python
print("Fetching top posts from r/python...")
for submission in reddit.subreddit("python").top(limit=3):
    print(f"- {submission.title} | Score: {submission.score}")
