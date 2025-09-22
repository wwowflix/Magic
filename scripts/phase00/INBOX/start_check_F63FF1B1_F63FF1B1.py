import sys
import os

REQUIRED_FILES = ["README.md", "docs/naming.md"]
REQUIRED_DIRS = ["scripts", "outputs/trends", "logs/archive"]


def main():
    missing = []
    for f in REQUIRED_FILES:
        if not os.path.isfile(f):
            missing.append(f)
    for d in REQUIRED_DIRS:
        if not os.path.isdir(d):
            missing.append(d)
    if missing:
        print("start_check: MISSING -> " + ", ".join(missing))
        sys.exit(1)
    print("start_check: OK")


if __name__ == "__main__":
    main()
