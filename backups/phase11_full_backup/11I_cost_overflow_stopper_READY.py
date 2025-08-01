import os
import re

# CONFIG
TARGET_FOLDER = 'outputs/logs/costs/'  # Folder where usage logs are stored
LOG_FILE = 'outputs/logs/cost_overflow_alerts.txt'
COST_LIMIT_USD = 10.00
TOKEN_LIMIT = 75000

alerts = []

# ✅ FIXED LINE — THIS IS CORRECT
cost_pattern = re.compile(r'Total Cost[:=]\s*\$?([0-9]+\.[0-9]+)', re.IGNORECASE)
token_pattern = re.compile(r'Tokens Used[:=]\s*([0-9]+)', re.IGNORECASE)

os.makedirs(TARGET_FOLDER, exist_ok=True)

for root, _, files in os.walk(TARGET_FOLDER):
    for file in files:
        if file.endswith('.txt') or file.endswith('.log'):
            path = os.path.join(root, file)
            try:
                with open(path, encoding='utf-8') as f:
                    content = f.read()
                    cost_match = cost_pattern.search(content)
                    token_match = token_pattern.search(content)
                    if cost_match:
                        cost_val = float(cost_match.group(1))
                        if cost_val > COST_LIMIT_USD:
                            alerts.append(f"{path} → 🚨 Cost exceeded: ")
                    if token_match:
                        token_val = int(token_match.group(1))
                        if token_val > TOKEN_LIMIT:
                            alerts.append(f"{path} → 🚨 Token limit exceeded: {token_val}")
            except Exception as e:
                alerts.append(f"{path} → ⚠️ {e}")

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
with open(LOG_FILE, 'w', encoding='utf-8') as f:
    if alerts:
        f.write("🚨 Cost overflow alerts:\n" + "\n".join(alerts))
    else:
        f.write("✅ All cost/token usage within safe limits.\n")

print(f"💰 Cost monitoring complete. Report saved to: {LOG_FILE}")
