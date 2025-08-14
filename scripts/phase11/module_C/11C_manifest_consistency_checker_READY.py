# 11C_manifest_consistency_checker_READY.py
import json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
MANIFEST = os.path.join(ROOT, "phase_manifest.json")

def normalize_entry(e):
    """
    Accepts either:
      { "PhaseNumber": 11, "Module": "C", "FinalFilename": "11C_foo_READY.py" }
    or:
      { "Phase": 99, "Module": "ZZ", "FinalFilename": "scripts/phase99/module_ZZ/99ZZ_dummy.py" }
    Returns (phase:int, module:str lower, relpath:str using forward slashes)
    """
    # Phase
    if "PhaseNumber" in e:
        phase = int(e["PhaseNumber"])
    elif "Phase" in e:
        phase = int(e["Phase"])
    else:
        raise ValueError(f"Bad entry (missing Phase/PhaseNumber): {e}")

    # Module
    if "Module" not in e or not str(e["Module"]).strip():
        raise ValueError(f"Bad entry (missing Module): {e}")
    module = str(e["Module"]).strip().lower()  # tolerate "ZZ" etc.

    # FinalFilename (either a filename or a relative path under scripts/)
    if "FinalFilename" not in e or not str(e["FinalFilename"]).strip():
        raise ValueError(f"Bad entry (missing FinalFilename): {e}")

    final = e["FinalFilename"].replace("\\", "/").strip()
    if final.startswith("scripts/"):
        rel = final  # already a path
    else:
        rel = f"scripts/phase{phase}/module_{module}/{final}"

    return phase, module, rel

def main():
    try:
        with open(MANIFEST, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as ex:
        print(f"Manifest read error: {ex}")
        sys.exit(1)

    missing = []
    bad = []
    total = 0

    for entry in data:
        try:
            phase, module, rel = normalize_entry(entry)
            abs_path = os.path.join(ROOT, rel)
            total += 1
            if not os.path.exists(abs_path):
                missing.append(rel)
        except Exception as ex:
            bad.append(f"{entry} :: {ex}")

    if bad or missing:
        print("Manifest consistency FAIL:")
        if bad:
            print("  Bad entries:")
            for b in bad[:50]:
                print("   -", b)
            if len(bad) > 50:
                print(f"   ... and {len(bad)-50} more")
        if missing:
            print("  Missing files:")
            for m in missing[:50]:
                print("   -", m)
            if len(missing) > 50:
                print(f"   ... and {len(missing)-50} more")
        print(f"Checked={total}  Bad={len(bad)}  Missing={len(missing)}")
        sys.exit(1)

    print(f"Manifest OK. Checked={total} Missing=0 Bad=0")
    sys.exit(0)

if __name__ == "__main__":
    main()
