# Create docs folder if not exists
if (-Not (Test-Path ".\docs")) { New-Item -ItemType Directory -Path ".\docs" }

# 1. Create self_healing_plan.md
$planContent = @"
# Self-Healing Runner Design Plan

## 1. Detect missing scripts
- Check manifest entries against file system.
- If missing, create placeholder script.

## 2. Placeholder creation
- Simple `.py` files with 'pass' inside.
- Naming pattern: `<script_name>_PLACEHOLDER.py`.

## 3. Quarantine mechanism
- Detect scripts that fail multiple times.
- Move to `quarantine/` folder for review.

## 4. Backup before overwrite
- Copy original files to `backups/` with timestamp.

## 5. Runner integration
- Add `--auto-heal` flag.
- On errors, call agents sequentially.
- Retry script after healing attempts.

---

Plan complete. Implement step-by-step agents.
"@
Set-Content -Path ".\docs\self_healing_plan.md" -Value $planContent -Encoding UTF8

# Create agents folder if not exists
if (-Not (Test-Path ".\agents")) { New-Item -ItemType Directory -Path ".\agents" }

# 2. Placeholder Recovery Agent
$placeholderAgent = @"
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
"@
Set-Content -Path ".\agents\self_heal_placeholder.py" -Value $placeholderAgent -Encoding UTF8

# 3. Quarantine Agent
$quarantineAgent = @"
import os
import shutil
import sys

QUARANTINE_DIR = 'quarantine'

def quarantine_script(script_path):
    if not os.path.exists(QUARANTINE_DIR):
        os.makedirs(QUARANTINE_DIR)
    base_name = os.path.basename(script_path)
    dest = os.path.join(QUARANTINE_DIR, base_name)
    print(f'Moving {script_path} to quarantine.')
    shutil.move(script_path, dest)

if __name__ == '__main__':
    # Example usage: pass failing script path as argument
    if len(sys.argv) < 2:
        print('Usage: python quarantine_agent.py <script_path>')
        sys.exit(1)
    script = sys.argv[1]
    quarantine_script(script)
"@
Set-Content -Path ".\agents\quarantine_agent.py" -Value $quarantineAgent -Encoding UTF8

# 4. Backup Agent
$backupAgent = @"
import os
import shutil
from datetime import datetime

BACKUP_DIR = 'backups'

def backup_file(filepath):
    if not os.path.exists(filepath):
        print(f'File {filepath} does not exist, skipping backup.')
        return
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_name = os.path.basename(filepath)
    backup_name = f'{base_name}_{timestamp}.bak'
    dest = os.path.join(BACKUP_DIR, backup_name)
    print(f'Backing up {filepath} to {dest}')
    shutil.copy2(filepath, dest)

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python backup_agent.py <file_path>')
        sys.exit(1)
    backup_file(sys.argv[1])
"@
Set-Content -Path ".\agents\backup_agent.py" -Value $backupAgent -Encoding UTF8

Write-Host "Week 3 agents and plan document created in docs/ and agents/ folders."
Write-Host "Next, you can implement runner auto-healing integration step-by-step."
