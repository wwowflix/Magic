from secrets import *

print("ðŸ” Testing secrets.py values...\n")

print(f"âœ… REDDIT_CLIENT_ID: {REDDIT_CLIENT_ID}")
print(f"âœ… REDDIT_CLIENT_SECRET: {REDDIT_CLIENT_SECRET}")
print(f"âœ… REDDIT_USER_AGENT: {REDDIT_USER_AGENT}")
print(f"âœ… REDDIT_USERNAME: {REDDIT_USERNAME}")
print(f"âœ… REDDIT_PASSWORD: {'*' * len(REDDIT_PASSWORD)}")

if all(
    [
        REDDIT_CLIENT_ID,
        REDDIT_CLIENT_SECRET,
        REDDIT_USER_AGENT,
        REDDIT_USERNAME,
        REDDIT_PASSWORD,
    ]
):
    print("\nâœ… All secrets loaded successfully!")
else:
    print("\nâŒ One or more secrets are missing or empty.")
