import os
import json

# Load manifest as list of script paths
with open("phase_manifest.json", "r", encoding="utf-8-sig") as f:
    manifest = json.load(f)


def ensure_placeholder(script_path):
    if not os.path.exists(script_path):
        print(f"⚠️ Missing script detected: {script_path}")
        os.makedirs(os.path.dirname(script_path), exist_ok=True)
        with open(script_path, "w", encoding="utf-8") as f:
            f.write("# Placeholder script - auto-generated\npass\n")
        print(f"✅ Placeholder created: {script_path}")


def main():
    print(f"▶ Running Placeholder Recovery on {len(manifest)} scripts...\n")
    for script_path in manifest:
        # Normalize path for OS compatibility
        normalized_path = os.path.normpath(script_path)

        # Extract phase and module for logging (optional)
        parts = normalized_path.split(os.sep)
        try:
            phase = parts[-3].replace("phase", "")
            module = parts[-2].replace("module_", "")
        except IndexError:
            # Path format unexpected, just continue
            phase = "unknown"
            module = "unknown"

        ensure_placeholder(normalized_path)

    print("\n✅ Placeholder recovery complete.")


if __name__ == "__main__":
    main()
