import os
from dotenv import dotenv_values

# CONFIG
REQUIRED_KEYS = [
    "NOTION_TOKEN",
    "NOTION_DATABASE_ID",
    "OPENAI_API_KEY",
    "GITHUB_TOKEN",
    "YOUTUBE_API_KEY"
]

ENV_PATH = ".env"
LOG_FILE = "outputs/logs/env_key_integrity_report.txt"

# Load .env contents
env_data = dotenv_values(ENV_PATH)
missing = []
empty = []
unknown = []

# Check each required key
for key in REQUIRED_KEYS:
    if key not in env_data:
        missing.append(key)
    elif env_data[key].strip() == "":
        empty.append(key)

# Detect extra keys
for key in env_data.keys():
    if key not in REQUIRED_KEYS:
        unknown.append(key)

# Write report
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
with open(LOG_FILE, "w", encoding="utf-8") as f:
    if not missing and not empty:
        f.write("[PASS] All required keys are present and non-empty.\n")
    else:
        if missing:
            f.write("❌ Missing keys:\n")
            for key in missing:
                f.write(f" - {key}\n")
        if empty:
            f.write("⚠️ Empty keys:\n")
            for key in empty:
                f.write(f" - {key}\n")
    if unknown:
        f.write("\n🧪 Extra (unknown) keys:\n")
        for key in unknown:
            f.write(f" - {key}\n")

print(f"🔐 Vault check complete. See: {LOG_FILE}")

