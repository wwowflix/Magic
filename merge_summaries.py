import glob
import os

SUMMARY_DIR = "outputs/summaries"
MASTER_SUMMARY = "outputs/phase_master_summary.tsv"

with open(MASTER_SUMMARY, "w", encoding="utf-8") as master_file:
    master_file.write("Phase_Module\tScript\tStatus\n")
    for summary_file in glob.glob(os.path.join(SUMMARY_DIR, "*_summary.tsv")):
        phase_module = os.path.basename(summary_file).replace("_summary.tsv", "")
        with open(summary_file, "r", encoding="utf-8") as f:
            next(f)  # Skip header line
            for line in f:
                master_file.write(f"{phase_module}\t{line}")
print(f"Master summary saved to {MASTER_SUMMARY}")
