import os
import csv
import re

# Base scripts folder (adjust if needed)
BASE_DIR = r"D:\MAGIC\scripts"

# Output CSV file path
OUTPUT_CSV = r"D:\MAGIC\magic_patch.csv"

# Regex to extract phase and module from folder path
# e.g. scripts\phase11\module_A
PHASE_REGEX = re.compile(r"phase(\d+)", re.IGNORECASE)
MODULE_REGEX = re.compile(r"module_([A-Z])", re.IGNORECASE)

# Regex to extract prefix and filename from file name
# e.g. 11A_some_script_READY.py
FILE_PREFIX_REGEX = re.compile(r"^(\d+[A-Z])_(.+)")

def get_phase_module_from_path(path):
    # Extract phase and module from path string
    phase_match = PHASE_REGEX.search(path)
    module_match = MODULE_REGEX.search(path)
    phase = phase_match.group(1) if phase_match else ""
    module = module_match.group(1) if module_match else ""
    return phase, module

def get_prefix_filename(file_name):
    match = FILE_PREFIX_REGEX.match(file_name)
    if match:
        prefix = match.group(1)
        filename = file_name
        return prefix, filename
    else:
        # fallback if no prefix pattern found
        return "", file_name

def generate_patch_csv():
    rows = []

    for root, dirs, files in os.walk(BASE_DIR):
        # Ignore hidden/system folders if needed
        for file in files:
            if not file.endswith(".py"):
                continue
            full_path = os.path.join(root, file)
            phase, module = get_phase_module_from_path(root)
            prefix, filename = get_prefix_filename(file)
            status = "Ready"  # you can customize status detection here

            rows.append({
                "Filename": filename,
                "Phase": phase,
                "Module": module,
                "Prefix": prefix,
                "Status": status,
                "Path": full_path
            })

    # Write CSV
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["Filename", "Phase", "Module", "Prefix", "Status", "Path"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Patch CSV generated: {OUTPUT_CSV}")

if __name__ == "__main__":
    generate_patch_csv()
