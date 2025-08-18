import os

# CONFIG
DECISION_LOGS_FOLDER = "outputs/logs/decisions/"  # where AI decisions would be logged
LOG_FILE = "outputs/logs/ai_decision_watchdog_report.txt"

# Keywords that indicate risky decisions
RISKY_DECISION_KEYWORDS = [
    "hallucinated",
    "unauthorized access",
    "misclassified",
    "low confidence",
    "escalate to human",
    "retracted",
]

matches = []

# Create test folder if it doesn't exist
os.makedirs(DECISION_LOGS_FOLDER, exist_ok=True)

for root, _, files in os.walk(DECISION_LOGS_FOLDER):
    for file in files:
        if file.endswith(".txt") or file.endswith(".log"):
            path = os.path.join(root, file)
            try:
                with open(path, encoding="utf-8") as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines, 1):
                        for keyword in RISKY_DECISION_KEYWORDS:
                            if keyword.lower() in line.lower():
                                matches.append(f"{path} → Line {i}: '{keyword}' found")
            except Exception as e:
                matches.append(f"{path} → ⚠️ {e}")

# Save results
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
with open(LOG_FILE, "w", encoding="utf-8") as f:
    if matches:
        f.write("🚨 Risky AI decisions flagged:\n" + "\n".join(matches))
    else:
        f.write("✅ No risky AI decisions found.\n")

print(f"📄 AI Decision Watchdog scan complete. Report saved to: {LOG_FILE}")
