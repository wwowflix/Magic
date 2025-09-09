"""
Smoke runner: import a target script as a module (no __main__),
fail only if import raises.
"""
import sys, runpy, os

TARGET = r"D:\MAGIC\scripts\11AA_failure_memory_builder_READY.py"

def main() -> int:
    try:
        # run_name != "__main__" prevents any `if __name__ == "__main__":` block
        runpy.run_path(TARGET, run_name="__probe__")
        return 0
    except SystemExit as e:
        # Treat explicit SystemExit from import as failure if code != 0
        code = int(getattr(e, "code", 1) or 0)
        return 0 if code == 0 else 1
    except Exception as e:
        print(f"[SMOKE] Import failed: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
