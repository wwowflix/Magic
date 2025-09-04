import praw
import pandas as pd
from datetime import datetime
from secrets import *

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD,
)

subreddits = ["technology", "futurology", "worldnews", "ArtificialInteligence"]
limit = 25
data = []

print("?? Scraping Reddit trending posts...")

for sub in subreddits:
    for post in reddit.subreddit(sub).hot(limit=limit):
        data.append(
            {
                "date": datetime.utcnow().isoformat(),
                "subreddit": sub,
                "title": post.title,
                "score": post.score,
                "comments": post.num_comments,
                "url": post.url,
            }
        )

df = pd.DataFrame(data)
df.to_csv("outputs/reddit_scrape.csv", index=False)
print(f"? Scraped {len(df)} posts into outputs/reddit_scrape.csv")
