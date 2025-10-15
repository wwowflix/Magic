"""Phase 0A sorter demo stub"""
import argparse

def main():
    parser = argparse.ArgumentParser(description="MAGIC sorter demo")
    parser.add_argument("--dry-run", action="store_true", help="Run without moving files")
    args = parser.parse_args()
    print("Sorter ran. Dry run:", args.dry_run)

if __name__ == "__main__":
    main()
