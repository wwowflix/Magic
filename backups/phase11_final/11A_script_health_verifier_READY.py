import os

# Config
SCRIPTS_ROOT = "scripts/"
LOG_OUTPUT = "outputs/logs/script_health_report.txt"

results = []

# Walk through script directory
for root, _, files in os.walk(SCRIPTS_ROOT):
    for file in files:
        if file.endswith("_READY.py"):
            full_path = os.path.join(root, file)
            issues = []
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if not content.strip():
                        issues.append("Empty File")
                    if not content.startswith("#!"):
                        issues.append("Missing Shebang")
                    try:
                        compile(content, full_path, "exec")
                    except SyntaxError:
                        issues.append("Syntax Error")
            except Exception as e:
                issues.append(f"Read Error: {e}")

            if issues:
                results.append(f"{full_path} âŒ {' | '.join(issues)}")
            else:
                results.append(f"{full_path} âœ… Healthy")

# Write log
os.makedirs(os.path.dirname(LOG_OUTPUT), exist_ok=True)
with open(LOG_OUTPUT, "w", encoding="utf-8") as f:
    for line in results:
        f.write(line + "\n")

print(
    f"ðŸ” Health scan complete. âœ…={sum('âœ…' in l for l in results)}, âŒ={sum('âŒ' in l for l in results)}"
)
print(f"ðŸ“„ See report: {LOG_OUTPUT}")
