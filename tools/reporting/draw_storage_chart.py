import csv
from pathlib import Path

OUT_PNG = Path("outputs/reports/storage_chart.png")
PLAN_TSV = Path("outputs/reports/cleanup_plan.tsv")


def main() -> None:
    if not PLAN_TSV.exists():
        print(f"No cleanup plan at {PLAN_TSV}, nothing to chart.")
        return

    total_mb = 0.0
    with PLAN_TSV.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            try:
                mb = float(row.get("mb", "0") or 0.0)
            except ValueError:
                continue
            total_mb += mb

    try:
        import matplotlib.pyplot as plt  # type: ignore[import]

        OUT_PNG.parent.mkdir(parents=True, exist_ok=True)

        fig, ax = plt.subplots()
        ax.bar(["Freed"], [total_mb])
        ax.set_ylabel("MB freed")
        ax.set_title("Cleanup Space Freed")

        plt.tight_layout()
        plt.savefig(OUT_PNG)
        plt.close(fig)

        print(f"Chart saved to {OUT_PNG} (total ~ {total_mb:.3f} MB)")
    except ImportError:
        print("matplotlib is not installed; skipping PNG chart.")
        print(f"Total estimated freed space: {total_mb:.3f} MB")


if __name__ == "__main__":
    main()
