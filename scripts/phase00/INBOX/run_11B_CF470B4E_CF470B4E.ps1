import os
import re

module_b_folder = r"D:\MAGIC\scripts\phase11\module_B"

# Regex to find print statements with \u2705 emoji
emoji_pattern = re.compile(r"print\((['\"]).*\\u2705.*\1\)")

for filename in os.listdir(module_b_folder):
    if filename.endswith("_READY.py"):
        full_path = os.path.join(module_b_folder, filename)
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Remove the emoji \u2705 from print statements
        # Replace print statements containing \u2705 with the same string but without \u2705
        new_content = re.sub(r"\\u2705\s*", "", content)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"Processed {filename}")
