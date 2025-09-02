import os

# CONFIG
SCRIPT_ROOT = "scripts/"
REQUIRED_ORCHESTRATORS = [
    "orchestrator.py",
    "orchestration_engine.py",
    "central_controller.py",
]

found_files = []
missing_orchestration = []

# Search for orchestrators
for root, _, files in os.walk(SCRIPT_ROOT):
    for f in files:
        if f in REQUIRED_ORCHESTRATORS:
            found_files.append(f)

# Determine missing orchestrators
for required in REQUIRED_ORCHESTRATORS:
    if required not in found_files:
        missing_orchestration.append(required)

if not missing_orchestration:
    print("✅ Orchestration layer is consistent.")
else:
    print("❌ Missing orchestrator components:")
    for m in missing_orchestration:
        print(f" - {m}")
