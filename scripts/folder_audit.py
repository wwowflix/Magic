from pathlib import Path
import sys

EXPECTED = {
    "scripts": {".py"},
    "outputs/trends": {".csv", ".tsv"},
    "logs/archive": {".log"},
    "docs": {".md"},
}


def main():
    root = Path(__file__).resolve().parents[1]
    issues = []
    for rel, exts in EXPECTED.items():
        p = root / rel
        if not p.exists():
            issues.append(f"[MISSING] {rel}/")
            continue
        for f in p.rglob("*"):
            if f.is_file() and f.suffix and exts and f.suffix.lower() not in exts:
                issues.append(f"[ODD] {f.relative_to(root)} (ext {f.suffix})")
    if issues:
        print("\n".join(issues))
        sys.exit(1)
    print("folder_audit: OK")


if __name__ == "__main__":
    main()
