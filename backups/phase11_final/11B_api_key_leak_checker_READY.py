import os
import re

# CONFIG
TARGET_DIR = "scripts"
LOG_FILE = "outputs/logs/api_key_leak_report.txt"

# Patterns that match common API key formats
key_patterns = [
    r"(?i)api[_-]?key\s*=\s*[\"'][\w\-]{16,}[\"']",
    r"(?i)secret\s*=\s*[\"'][\w\-]{16,}[\"']",
    r"(?i)sk_live_[\w\-]{16,}",
    r"(?i)ghp_[\w]{36,}",
    r"(?i)AIza[0-9A-Za-z-_]{35}",
    r"(?i)xox[baprs]-[0-9a-zA-Z]{10,}",
]

# Recursively scan for leaks
leaks = []

for root, dirs, files in os.walk(TARGET_DIR):
    for file in files:
        if file.endswith(".py") or file.endswith(".env"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    for pattern in key_patterns:
                        if re.search(pattern, content):
                            leaks.append(
                                f"❗ Potential leak in {path} (pattern: {pattern})"
                            )
            except:
                continue

# Write report
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
with open(LOG_FILE, "w", encoding="utf-8") as f:
    if not leaks:
        f.write("✅ No API key leaks detected.\n")
    else:
        f.write("❌ Potential API key leaks found:\n")
        for line in leaks:
            f.write(f"{line}\n")

print(f"🔐 Leak scan complete. Results saved to {LOG_FILE}")
