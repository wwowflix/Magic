import sys
if __name__ == "__main__":
    dry_run = ("--dry-run" in sys.argv)
    print("DAG {}OK".format("dry-run " if dry_run else ""))
    sys.exit(0)
