import os
import sys

manifest_file = 'phase_manifest.json'

def load_manifest():
    import json
    with open(manifest_file, 'r', encoding='utf-8-sig') as f:
        return json.load(f)

def ensure_placeholders(manifest):
    for script_path in manifest:
        if not os.path.exists(script_path):
            print(f"Creating placeholder for missing script: {script_path}")
            os.makedirs(os.path.dirname(script_path), exist_ok=True)
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write('pass\n')

if __name__ == '__main__':
    manifest = load_manifest()
    ensure_placeholders(manifest)
