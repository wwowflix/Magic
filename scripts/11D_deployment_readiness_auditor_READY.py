import os

# CONFIG
CHECKLIST = [
    (".env", "ðŸ” .env file"),
    ("venv", "ðŸ Python virtual environment"),
    ("requirements.txt", "ðŸ“¦ requirements.txt"),
    ("scripts", "ðŸ“ scripts directory"),
]

missing = []

# Core Checks
for path, label in CHECKLIST:
    if not os.path.exists(path):
        missing.append(label)

# Phase folders check
PHASES_OK = True
for i in range(18):
    phase_folder = f"scripts/phase{i}"
    if not os.path.exists(phase_folder):
        PHASES_OK = False
        print(f"âŒ Missing: {phase_folder}")
    else:
        has_ready = any(f.endswith("_READY.py") for f in os.listdir(phase_folder))
        if not has_ready:
            PHASES_OK = False
            print(f"âš ï¸  No _READY scripts in {phase_folder}")

# Summary
if not missing and PHASES_OK:
    print("âœ… Deployment Readiness: All checks passed.")
else:
    print("âŒ Deployment readiness issues detected:")
    for m in missing:
        print(f" - {m}")
