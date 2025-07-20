from secrets import *

print("🔐 Testing secrets.py values...\n")

print(f"✅ REDDIT_CLIENT_ID: {REDDIT_CLIENT_ID}")
print(f"✅ REDDIT_CLIENT_SECRET: {REDDIT_CLIENT_SECRET}")
print(f"✅ REDDIT_USER_AGENT: {REDDIT_USER_AGENT}")
print(f"✅ REDDIT_USERNAME: {REDDIT_USERNAME}")
print(f"✅ REDDIT_PASSWORD: {'*' * len(REDDIT_PASSWORD)}")

if all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, REDDIT_USERNAME, REDDIT_PASSWORD]):
    print("\n✅ All secrets loaded successfully!")
else:
    print("\n❌ One or more secrets are missing or empty.")
