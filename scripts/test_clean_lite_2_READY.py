import pandas as pd
import snscrape.modules.twitter as sntwitter

print("âœ… Pandas version:", pd.__version__)
print("âœ… snscrape test:")

query = "AI lang:en"
tweets = []
for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    tweets.append(tweet.content)
    if i > 2:
        break

print("âœ… Sample tweet:", tweets[0][:80])
