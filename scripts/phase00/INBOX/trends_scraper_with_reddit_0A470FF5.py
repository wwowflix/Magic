# -*- coding: utf-8 -*-
#!/usr/bin/env python
import argparse
import json
import os
import sys
from datetime import datetime
import pandas as pd
from pytrends.request import TrendReq
import praw
from cost_manager import CostManager

# Load vault
VAULT_PATH = os.path.join(os.path.dirname(__file__), 'vault.json')
with open(VAULT_PATH, 'r', encoding='utf-8-sig') as vf:
    vault = json.load(vf)

cost_mgr = CostManager()

def scrape_google(keywords):
    pytrends = TrendReq()
    rows = []
    for kw in keywords:
        cost_mgr.record_api_call('pytrends')
        df = pytrends.get_interest_over_time()[[kw]].reset_index()
        if df.empty:
            continue
        for _, row in df.iterrows():
            rows.append({
                'date': row['date'].strftime('%Y-%m-%d'),
                'keyword': kw,
                'platform': 'Google',
                'metric': row[kw]
            })
    return pd.DataFrame(rows)

def scrape_youtube():
    # stub – your existing YouTube code goes here
    return pd.DataFrame([])

def scrape_tiktok():
    # stub – your existing TikTok code goes here
    return pd.DataFrame([])

def scrape_reddit(subreddits, limit=25):
    creds = vault.get('reddit', {})
    reddit = praw.Reddit(
        client_id=creds['client_id'],
        client_secret=creds['client_secret'],
        user_agent=creds['user_agent']
    )
    rows = []
    for sub in subreddits:
        cost_mgr.record_api_call('reddit')
        for post in reddit.subreddit(sub).hot(limit=limit):
            rows.append({
                'date': datetime.utcnow().strftime('%Y-%m-%d'),
                'keyword': post.title,
                'platform': 'Reddit',
                'metric': post.score
            })
    return pd.DataFrame(rows)

def main():
    parser = argparse.ArgumentParser(description='Zephyr trends scraper')
    parser.add_argument('--source', choices=['google','youtube','tiktok','reddit'], required=True)
    parser.add_argument('--keywords', nargs='+', help='For Google: list of terms')
    parser.add_argument('--subreddits', nargs='+', default=['all'], help='For Reddit: subreddits')
    parser.add_argument('--limit', type=int, default=25, help='Reddit: number of posts')
    args = parser.parse_args()

    if args.source == 'google':
        if not args.keywords: parser.error('Google requires --keywords')
        df = scrape_google(args.keywords)
    elif args.source == 'youtube':
        df = scrape_youtube()
    elif args.source == 'tiktok':
        df = scrape_tiktok()
    elif args.source == 'reddit':
        df = scrape_reddit(args.subreddits, args.limit)

    if df.empty:
        print(f'? No data returned for {args.source}')
        sys.exit(1)

    out = os.path.join(os.path.dirname(__file__), '..', 'data', f'{args.source}_trending.csv')
    df.to_csv(out, index=False, encoding='utf-8-sig')
    print(f'[OK] {args.source.capitalize()} trending data saved to {out}')

if __name__ == '__main__':
    main()



