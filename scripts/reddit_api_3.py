import praw

CLIENT_ID = "E5gkpBqsI6_szr6Cv9KqeQ"
CLIENT_SECRET = "YWiL0a28T2KIWCoxfOltNeUL5a4IXw"
USER_AGENT = "MAGICZephyr/0.1 by u/AffectionateRoom6084"

def fetch_reddit_trends(subreddits):
    try:
        reddit = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            user_agent=USER_AGENT,
            check_for_async=False,
            read_only=True
        )

        print("✅ Connected to Reddit API")

        posts = []
        for subreddit_name in subreddits:
            print(f"🔍 Fetching: {subreddit_name}")
            subreddit = reddit.subreddit(subreddit_name)
            for post in subreddit.hot(limit=3):
                posts.append({
                    'subreddit': subreddit_name,
                    'title': post.title,
                    'score': post.score,
                    'url': post.url
                })
        return posts
    except Exception as e:
        print(f"❌ Error fetching Reddit data: {e}")
        return []

if __name__ == "__main__":
    subreddits = ["technology", "machinelearning", "AI"]
    for sub in subreddits:
        try:
            print(f"\n🌐 Checking: {sub}")
            results = fetch_reddit_trends([sub])
            for post in results:
                print(f"📌 {post['title']} ({post['score']} pts)")
        except Exception as e:
            print(f"❌ Failed for {sub}: {e}")
