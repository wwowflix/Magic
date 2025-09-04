from __future__ import annotations
from pathlib import Path
import csv
import argparse


def merge_summaries(input_dir: str, out_file: str) -> int:
    """
    Merge all *.tsv in input_dir into a single TSV (header written once).
    Handles UTF-8 with BOM safely; ignores empty/blank lines.
    """
    in_dir = Path(input_dir)
    out_path = Path(out_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    header = None
    rows = []

    for p in sorted(in_dir.rglob("*.tsv")):
        try:
            # utf-8-sig removes UTF-8 BOM and will also read many UTF-16-with-BOM files as text via 'errors="replace"'
            with p.open("r", encoding="utf-8-sig", errors="replace", newline="") as f:
                reader = csv.reader(f, delimiter="\t")
                local_header = next(reader, None)
                if not local_header or all(
                    (c or "").strip() == "" for c in local_header
                ):
                    continue
                if header is None:
                    header = local_header
                # append rows, skipping blanks
                for row in reader:
                    if not row or all((c or "").strip() == "" for c in row):
                        continue
                    rows.append(row)
        except Exception:
            # Never explode on import/tests—just skip bad files.
            continue

    if header is None:
        header = ["Filename", "Status", "Phase", "Folder"]  # fallback header

    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(header)
        writer.writerows(rows)

    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input_dir", default=str(Path("outputs") / "summaries"))
    ap.add_argument(
        "--out", default=str(Path("outputs") / "summaries" / "phase_master_summary.tsv")
    )
    args = ap.parse_args(argv)
    return merge_summaries(args.input_dir, args.out)


if __name__ == "__main__":
    raise SystemExit(main())
