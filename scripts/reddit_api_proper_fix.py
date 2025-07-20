import sys
from pathlib import Path

# Read original file
file_path = Path(".\reddit_api.py")
content = file_path.read_text(encoding='utf-8')

# Fix indentation
fixed_content = content.replace(
    'if subreddit_list is None:    subreddits =',
    'if subreddit_list is None:\n    subreddits ='
)

# Write fixed file
fixed_path = Path(".\reddit_api_proper_fix.py")
fixed_path.write_text(fixed_content, encoding='utf-8')

print("✅ Reddit script fixed and saved as reddit_api_proper_fix.py")

