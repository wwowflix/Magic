# Self-Healing Runner Design Plan

## 1. Detect missing scripts
- Check manifest entries against file system.
- If missing, create placeholder script.

## 2. Placeholder creation
- Simple .py files with 'pass' inside.
- Naming pattern: <script_name>_PLACEHOLDER.py.

## 3. Quarantine mechanism
- Detect scripts that fail multiple times.
- Move to quarantine/ folder for review.

## 4. Backup before overwrite
- Copy original files to ackups/ with timestamp.

## 5. Runner integration
- Add --auto-heal flag.
- On errors, call agents sequentially.
- Retry script after healing attempts.

---

Plan complete. Implement step-by-step agents.
