import argparse
from pathlib import Path

SMART = {
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u2013": "-",
    "\u2014": "-",
}
INVIS = ["\u200b", "\u200c", "\u200d", "\ufeff", "\u2060", "\u00a0"]
TRANS = str.maketrans(SMART)


def looks_binary(data: bytes) -> bool:
    # simple heuristic
    return b"\x00" in data[:4096]


def normalize_text(txt: str) -> str:
    for ch in INVIS:
        txt = txt.replace(ch, "")
    txt = txt.translate(TRANS)
    txt = txt.replace("\r\n", "\n").replace("\r", "\n")
    if not txt.endswith("\n"):
        txt += "\n"
    return txt


def process_file(path: Path, apply: bool) -> tuple[bool, str]:
    try:
        raw = path.read_bytes()
        if looks_binary(raw):
            return False, "binary-skip"

        try:
            txt = raw.decode("utf-8")
        except UnicodeDecodeError:
            # try common fallback and then encode to utf-8
            try:
                txt = raw.decode("utf-8-sig")
            except UnicodeDecodeError:
                try:
                    txt = raw.decode("cp1252")
                except UnicodeDecodeError:
                    return False, "decode-failed"

        fixed = normalize_text(txt)
        changed = fixed != txt

        if apply and changed:
            bak = path.with_suffix(path.suffix + ".bak")
            bak.write_bytes(raw)
            path.write_text(fixed, encoding="utf-8", newline="\n")
        return changed, "ok" if not changed else ("fixed" if apply else "would-fix")
    except Exception as e:
        return False, f"error:{e}"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("root", nargs="?", default=".")
    p.add_argument(
        "--apply", action="store_true", help="Write changes (creates .bak backups)"
    )
    p.add_argument("--ext", default=".py", help="File extension to scan (default: .py)")
    p.add_argument(
        "--max-bytes", type=int, default=2_000_000, help="Skip files larger than this"
    )
    args = p.parse_args()

    root = Path(args.root).resolve()
    changed = skipped = ok = 0
    for path in root.rglob(f"*{args.ext}"):
        try:
            if path.stat().st_size > args.max_bytes:
                skipped += 1
                continue
        except FileNotFoundError:
            continue
        c, status = process_file(path, args.apply)
        if status.startswith("error") or status == "decode-failed":
            print(f"[!] {status:12s} {path}")
        elif status in ("fixed", "would-fix"):
            changed += 1
            print(f"[+] {status:12s} {path}")
        else:
            ok += 1

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"\nMode: {mode} | changed={changed} ok={ok} skipped={skipped}")


if __name__ == "__main__":
    main()
