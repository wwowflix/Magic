import os
import re

# CONFIG
SCRIPTS_ROOT = "scripts/"
LOG_FILE = "outputs/logs/privacy_audit_log.txt"

PATTERNS = {
    "Email": r"[\w\.-]+@[\w\.-]+",
    "IP Address": r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
    "Token": r'(secret|token|apikey|key)[\s:=]+["\']?\w+',
}

matches = []

for root, _, files in os.walk(SCRIPTS_ROOT):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            try:
                with open(path, encoding="utf-8") as f:
                    content = f.read()
                    for label, pattern in PATTERNS.items():
                        for match in re.findall(pattern, content, re.IGNORECASE):
                            matches.append(f"{path} → 🛑 {label}: {match}")
            except Exception as e:
                matches.append(f"{path} → ⚠️ {e}")

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
with open(LOG_FILE, "w", encoding="utf-8") as f:
    if matches:
        f.write("❌ Privacy risks detected:\n")
        f.write("\n".join(matches))
    else:
        f.write("✅ No privacy leaks found.\n")

print(f"📄 Report saved to: {LOG_FILE}")
