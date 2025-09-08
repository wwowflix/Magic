import csv, json
from pathlib import Path

SRC = Path("phase_master_summary.tsv")
OUT = Path("retry_queue.json")


def main():
    fails = []
    if SRC.exists():
        with SRC.open("r", encoding="utf-8", newline="") as f:
            rd = csv.DictReader(f, delimiter="\t")
            for r in rd:
                if (r.get("STATUS") or "").upper() == "FAIL":
                    fails.append(
                        {
                            "phase": r.get("PHASE"),
                            "module": r.get("MODULE"),
                            "script": r.get("SCRIPT"),
                        }
                    )
    OUT.write_text(json.dumps(fails, indent=2), encoding="utf-8")
    print(f"[OK] retry_queue size={len(fails)} -> {OUT}")


if __name__ == "__main__":
    main()
