import subprocess

def run_notion_sync():
    print("\n🔄 Triggering Notion Sync via PowerShell...")
    try:
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "run_magic_sync.ps1"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Notion Sync Failed: {e}")

# After script runs and summaries are written:
run_notion_sync()
