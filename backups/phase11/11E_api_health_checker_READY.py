import os
import requests

# CONFIG
ENDPOINTS = [
    "https://api.github.com",
    "https://www.google.com",
    "https://nonexistent.openai.com"
]
LOG_FILE = "outputs/logs/api_health_check_log.txt"

os.makedirs("outputs/logs", exist_ok=True)
with open(LOG_FILE, "w", encoding="utf-8") as f:
    for url in ENDPOINTS:
        try:
            r = requests.get(url, timeout=3)
            status = f"{url} → ✅ {r.status_code}"
        except Exception as e:
            status = f"{url} → ❌ {e}"
        print(status)
        f.write(status + "\n")

print(f"📄 API health report saved to: {LOG_FILE}")
