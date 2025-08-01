import os

# CONFIG
SCRIPTS_ROOT = 'scripts/'
BANNED_TERMS = ['scrape', 'hack', 'exploit', 'bypass']
LOG_FILE = 'outputs/logs/legal_terms_violation_log.txt'

violations = []

for root, _, files in os.walk(SCRIPTS_ROOT):
    for file in files:
        if file.endswith('.py'):
            path = os.path.join(root, file)
            try:
                with open(path, encoding='utf-8') as f:
                    content = f.read().lower()
                    for term in BANNED_TERMS:
                        if term in content:
                            violations.append(f"{path} → 🚫 contains '{term}'")
            except Exception as e:
                violations.append(f"{path} → ⚠️ {e}")

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
with open(LOG_FILE, 'w', encoding='utf-8') as f:
    if violations:
        f.write("❌ Violations Found:\n")
        f.write('\n'.join(violations))
    else:
        f.write("✅ No legal term violations found.\n")

print(f"📄 Report saved to: {LOG_FILE}")
