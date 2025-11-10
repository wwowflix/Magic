import csv
from pathlib import Path

PLAN_TSV = Path("outputs/reports/cleanup_plan.tsv")
OUT_TSV = Path("outputs/reports/storage_diff.tsv")

TARGET_GB = 10.0  # target from roadmap (>= 10 GB freed)


def main() -> None:
    if not PLAN_TSV.exists():
        raise SystemExit(f"Cleanup plan not found: {PLAN_TSV}")

    total_bytes = 0
    with PLAN_TSV.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            try:
                b = int(row.get("bytes", "0"))
            except ValueError:
                continue
            total_bytes += b

    freed_gb = total_bytes / (1024 * 1024 * 1024)

    OUT_TSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_TSV.open("w", encoding="utf-8", newline="") as f:
        f.write("freed_bytes\tfreed_gb\tmeets_target_10gb\n")
        meets = "yes" if freed_gb >= TARGET_GB else "no"
        f.write(f"{total_bytes}\t{freed_gb:.6f}\t{meets}\n")

    print(f"Estimated space freed from quarantine: {freed_gb:.6f} GB")
    print(f"Diff written to {OUT_TSV}")


if __name__ == "__main__":
    main()
