import pandas as pd

csv_path = "outputs/notion_export/magic_patch.csv"

df = pd.read_csv(csv_path)


# Fix Prefix if empty and Filename is valid
def extract_prefix(filename):
    if isinstance(filename, str) and "_" in filename:
        return filename.split("_")[0]
    return ""


missing_prefixes = df["Prefix"].isnull() | (df["Prefix"] == "")
df.loc[missing_prefixes, "Prefix"] = df.loc[missing_prefixes, "Filename"].apply(extract_prefix)

df.to_csv(csv_path, index=False)
print(f"✅ Fixed {missing_prefixes.sum()} missing Prefix entries in {csv_path}")
