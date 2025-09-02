import os
import csv
import datetime

SUMMARY_DIR = os.path.join("outputs", "summaries")
DAILY_STATUS_FILE = os.path.join(SUMMARY_DIR, "daily_status.csv")


def aggregate_status():
    summary_files = [f for f in os.listdir(SUMMARY_DIR) if f.endswith("_summary.tsv")]
    daily_records = []

    for summary_file in summary_files:
        phase_module = summary_file.replace("_summary.tsv", "")

        if "_module_" not in phase_module:
            print(f"⚠️ Skipping summary file with unexpected name format: {summary_file}")
            continue

        try:
            phase, module = phase_module.split("_module_")
        except ValueError:
            print(f"⚠️ Could not unpack phase/module from: {phase_module}")
            continue

        summary_path = os.path.join(SUMMARY_DIR, summary_file)

        with open(summary_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            total = 0
            passed = 0
            failed = 0

            for row in reader:
                total += 1
                status = row.get("Status", "").upper()
                if status == "PASS":
                    passed += 1
                elif status == "FAIL":
                    failed += 1

            daily_records.append(
                {
                    "Date": datetime.date.today().isoformat(),
                    "Phase": phase,
                    "Module": module,
                    "Total Scripts": total,
                    "Passed": passed,
                    "Failed": failed,
                }
            )

    with open(DAILY_STATUS_FILE, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Date", "Phase", "Module", "Total Scripts", "Passed", "Failed"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in daily_records:
            writer.writerow(record)

    print(f"✅ Daily status aggregation complete. Output file: {DAILY_STATUS_FILE}")


if __name__ == "__main__":
    aggregate_status()
