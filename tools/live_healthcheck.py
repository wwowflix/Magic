import json
import os


def main() -> int:
    status = {"ok": True, "msg": "MAGIC container healthy", "cwd": os.getcwd()}
    print(json.dumps(status))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
