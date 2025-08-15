import json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(os.path.dirname(ROOT), "phase_manifest.json")

REAL_FILES = [
    "scripts/phase11/module_C/11C_script_integrity_checker_READY.py",
    "scripts/phase11/module_C/11C_manifest_consistency_checker_READY.py",
]

def main():
    with open(MANIFEST, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        print("Manifest JSON must be a list"); sys.exit(1)

    new_data = []
    removed = 0
    added = 0

    for e in data:
        if not isinstance(e, dict):
            continue
        phase = e.get("PhaseNumber", e.get("Phase"))
        mod   = e.get("Module")
        fname = str(e.get("FinalFilename", "")).replace("\\","/")
        # Drop C placeholders
        if str(phase) == "11" and str(mod).lower() == "c" and "placeholder" in fname.lower():
            removed += 1
            continue
        new_data.append(e)

    # Ensure the two real C entries exist (idempotent)
    existing = { str(e.get("FinalFilename","")).replace("\\","/") for e in new_data }
    for rel in REAL_FILES:
        if rel not in existing:
            new_data.append({"Phase": 11, "Module": "C", "FinalFilename": rel})
            added += 1

    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=2, ensure_ascii=False)
    print(f"Patched manifest: removed={removed} added={added} total={len(new_data)}")

if __name__ == "__main__":
    main()
