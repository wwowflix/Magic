import json
with open("phase_manifest.json", encoding="utf-8-sig") as f:
    data = json.load(f)
print("✅ Loaded", len(data), "entries from manifest")
print("Sample:", data[:3])
