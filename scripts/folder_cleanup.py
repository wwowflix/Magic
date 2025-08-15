from pathlib import Path
import time
CUTOFF_DAYS = 30
def main():
    cutoff = time.time() - (CUTOFF_DAYS * 86400)
    archive = Path("logs/archive")
    removed = 0
    if archive.exists():
        for log in archive.glob("*.log"):
            if log.stat().st_mtime < cutoff:
                try:
                    log.unlink(); removed += 1
                except Exception as e:
                    print(f"skip {log}: {e}")
    print(f"folder_cleanup: removed {removed} old logs")
if __name__ == "__main__":
    main()
