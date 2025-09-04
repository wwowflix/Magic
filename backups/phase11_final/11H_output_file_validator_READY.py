import os

for file in os.listdir("outputs/data"):
    if not file.endswith(".csv"):
        print(f"? Unexpected output file: {file}")
print("? Output file validation complete.")
