import json

with open("phase_manifest.json", "r", encoding="utf-8-sig") as f:
    data = json.load(f)

print("\n✅ First 3 items in phase_manifest.json:")
for item in data[:3]:
    print(item)
