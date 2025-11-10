import argparse
import re
import csv
import pathlib


def main() -> None:
    parser = argparse.ArgumentParser("MAGIC gap report")
    parser.add_argument("--snapshot", required=True)
    parser.add_argument("--phases", required=True, help="like 0-18")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    lo, hi = map(int, args.phases.split("-"))
    expected = [f"{i:02d}" for i in range(lo, hi + 1)]

    # read snapshot tolerating BOM, just in case
    text = pathlib.Path(args.snapshot).read_text(encoding="utf-8-sig")

    seen = set()
    for line in text.splitlines():
        # match: 03B_something_READY.py
        m = re.search(r"(\\d{2})[A-Z]_.*?_READY\\.py", line)
        if m:
            seen.add(m.group(1))

    rows = []
    for ph in expected:
        if ph in seen:
            rows.append({"phase": ph, "found": "✅", "note": ""})
        else:
            rows.append({"phase": ph, "found": "❌", "note": "missing placeholders"})

    out_path = pathlib.Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["phase", "found", "note"], delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Gap report written to {args.out}")


if __name__ == "__main__":
    main()
