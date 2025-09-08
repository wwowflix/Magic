import shutil, time
from pathlib import Path

SRC = Path("phase_manifest.json")
DST = Path("backups/manifest")
DST.mkdir(parents=True, exist_ok=True)


def main():
    if not SRC.exists():
        print("[WARN] missing:", SRC)
        return
    ts = time.strftime("%Y%m%d_%H%M%S")
    out = DST / f"manifest_{ts}.json"
    shutil.copy2(SRC, out)
    print("[OK] backed up to", out)


if __name__ == "__main__":
    main()
