import os

# CONFIG
SCRIPTS_DIR = "scripts/"
LOG_FILE = "outputs/logs/broken_scripts_log.txt"

broken_scripts = []

for root, _, files in os.walk(SCRIPTS_DIR):
    for file in files:
        if file.endswith("_READY.py"):
            path = os.path.join(root, file)
            try:
                compile(open(path, encoding="utf-8").read(), path, 'exec')
            except Exception as e:
                broken_scripts.append(f"{file} → ❌ {e}")

# Write log
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
with open(LOG_FILE, "w", encoding="utf-8") as f:
    if not broken_scripts:
        f.write("✅ No broken scripts found.\n")
    else:
        f.write("❌ Broken Scripts:\n")
        for entry in broken_scripts:
            f.write(f"{entry}\n")

print(f"🔍 Check complete. Broken: {len(broken_scripts)}")
print(f"📄 See report: {LOG_FILE}")
