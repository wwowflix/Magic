# PowerShell script to patch trends_scraper.py with Reddit support

$pyFile = "D:\MAGIC\scripts\trends_scraper.py"

# Insert Reddit import lines if missing
(Get-Content $pyFile) -replace "(import pandas as pd)", "import pandas as pd`nimport praw`nimport datetime" | Set-Content $pyFile

# Define Reddit scraping function
$redditFunction = @'
def scrape_reddit(subreddits, client_id, client_secret, user_agent):
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

    rows = []
    for sub in subreddits:
        subreddit = reddit.subreddit(sub)
        for submission in subreddit.hot(limit=10):
            rows.append({
                "date": datetime.datetime.fromtimestamp(submission.created_utc).strftime("%Y-%m-%d"),
                "keyword": submission.title,
                "metric": submission.score,
                "platform": "reddit",
                "author": str(submission.author) if submission.author else "N/A"
            })

    df = pd.DataFrame(rows)
    return df
