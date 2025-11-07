# -*- coding: utf-8 -*-
import argparse


def main(argv=None):
    parser = argparse.ArgumentParser(prog="configtool", add_help=True)
    parser.add_argument("--version", action="store_true")
    parser.add_argument("--cflags", action="store_true")
    parser.add_argument("--pkgconfigdir", action="store_true")

    argv = [] if argv is None else list(argv)
    args, _unknown = parser.parse_known_args(argv)

    # Minimal behavior for smoke tests:
    if args.version:
        try:
            from . import __version__ as _v  # optional
        except Exception:
            _v = "0"
        print(_v)
        return 0

    if args.cflags:
        print("")
        return 0

    if args.pkgconfigdir:
        from pathlib import Path as _P

        print(str((_P(__file__).parent).resolve()))
        return 0

    # Default no-op
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
