import os
import shutil
from dotenv import load_dotenv

# 🌱 Load .env for Notion Token
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")

# 📁 Paths
SCRIPTS_DIR = "scripts"
BACKUP_DIR = "backups"
LOGS_DIR = "logs"
PATCH_CSV = "outputs/notion_export/magic_patch.csv"


# 🧠 Self-Healing Actions
def restore_missing_scripts():
    print("🔍 Checking for missing scripts...")
    restored = 0
    for root, _, files in os.walk(BACKUP_DIR):
        for file in files:
            if file.endswith("_READY.py"):
                rel_path = os.path.relpath(root, BACKUP_DIR)
                target_path = os.path.join(SCRIPTS_DIR, rel_path, file)
                if not os.path.exists(target_path):
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    shutil.copy2(os.path.join(root, file), target_path)
                    print(f"♻️ Restored: {target_path}")
                    restored += 1
    if restored == 0:
        print("✅ All scripts intact!")
    else:
        print(f"✅ {restored} scripts restored.")


def clean_logs():
    print("🧹 Cleaning logs...")
    if not os.path.exists(LOGS_DIR):
        print("⚠️ Logs folder missing.")
        return
    for file in os.listdir(LOGS_DIR):
        path = os.path.join(LOGS_DIR, file)
        if os.path.isfile(path) and file.endswith(".log"):
            os.remove(path)
            print(f"🗑 Deleted: {file}")
    print("✅ Logs cleaned.")


def notion_sync():
    print("🔁 (Placeholder) Sync to Notion... ✅")


def run_all():
    restore_missing_scripts()
    clean_logs()
    notion_sync()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Dry run only")
    parser.add_argument(
        "--restore", action="store_true", help="Only restore missing scripts"
    )
    parser.add_argument("--clean", action="store_true", help="Only clean logs")
    parser.add_argument("--all", action="store_true", help="Full heal cycle")
    args = parser.parse_args()

    if args.test:
        print("🧪 Running TEST mode (no actions)...")
        print("✅ Notion Token loaded" if NOTION_TOKEN else "❌ Notion Token missing!")
        print(f"📁 Backups present: {os.path.exists(BACKUP_DIR)}")
        print(f"📄 Patch CSV: {os.path.exists(PATCH_CSV)}")
    elif args.restore:
        restore_missing_scripts()
    elif args.clean:
        clean_logs()
    elif args.all:
        run_all()
    else:
        parser.print_help()
