import os
import pandas as pd
from collections import defaultdict

PATCH_CSV_PATH = "outputs/notion_export/magic_patch.csv"
LOG_OUTPUT = "outputs/logs/flow_breakpoint_report.txt"

# Load data
df = pd.read_csv(PATCH_CSV_PATH)
df = df[df["Filename"].str.endswith("_READY.py")]

# Group by Phase → List of Modules
flow_map = defaultdict(set)
for _, row in df.iterrows():
    try:
        phase = int(row["Phase"])
        module = row["Module"]
        flow_map[phase].add(module)
    except:
        continue

# Detect breakpoints (missing intermediate modules)
log_lines = []
for phase in sorted(flow_map):
    modules = sorted(flow_map[phase])
    missing = []
    for i in range(ord("A"), ord("Z") + 1):
        mod = chr(i)
        if mod not in modules:
            if any(chr(j) in modules for j in range(i - 1, i + 2)):
                missing.append(mod)
    if missing:
        log_lines.append(f"Phase {phase}: ❗ Missing modules near continuity: {', '.join(missing)}")

# Write report
os.makedirs(os.path.dirname(LOG_OUTPUT), exist_ok=True)
with open(LOG_OUTPUT, "w", encoding="utf-8") as f:
    if not log_lines:
        f.write("✅ All phase/module chains appear continuous.\n")
    else:
        f.write("❌ Flow Breakpoints Detected:\n")
        for line in log_lines:
            f.write(f"{line}\n")

print(f"📊 Continuity scan complete. Report saved to {LOG_OUTPUT}")
