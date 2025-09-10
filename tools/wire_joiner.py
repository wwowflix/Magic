import csv
import os
import py_compile
import re
import shutil
import sys
import time

ROOT = r"D:\MAGIC"
SCRIPTS_DIR = os.path.join(ROOT, "scripts")
OUT_DIR = os.path.join(ROOT, "outputs", "wire_joiner")
BACKUP_DIR = os.path.join(
    ROOT, "backups", f"wire_joiner_{time.strftime('%Y%m%d_%H%M%S')}"
)

KEEP_SUFFIX = "_READY.py"
BAD_CHARS = {
    "\ufeff": "",  # UTF-8 BOM
    "»": "",
    "«": "",
    "\u00a0": " ",  # NBSP -> space
    "\r\n": "\n",  # CRLF -> LF
}
PLACEHOLDER_RE = re.compile(
    r'^\s*("""|\'\'\')\s*Placeholder.*?\1\s*$', re.IGNORECASE | re.DOTALL
)
IMPORT_RE = re.compile(
    r"^\s*(from\s+([a-zA-Z0-9_\.]+)\s+import|import\s+([a-zA-Z0-9_\.]+))", re.MULTILINE
)


def ensure_dirs():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)


def rel(p):
    return os.path.relpath(p, ROOT)


def normalize_text(text: str) -> str:
    for bad, good in BAD_CHARS.items():
        text = text.replace(bad, good)
    # normalize fancy quotes
    return text.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")


def is_placeholder_only(text: str) -> bool:
    return bool(PLACEHOLDER_RE.match(text.strip()))


def backup_file(path: str):
    dst = os.path.join(BACKUP_DIR, rel(path))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(path, dst)


def write_file(path: str, text: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def compile_check(path: str):
    try:
        py_compile.compile(path, doraise=True)
        return True, ""
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def guess_missing_local_imports(py_path: str):
    txt = read_file(py_path)
    missing = set()
    for m in IMPORT_RE.finditer(txt):
        name = (m.group(2) or m.group(3) or "").split(".")[0]
        if not name:
            continue
        # basic stdlib skip list
        if name in {
            "os",
            "sys",
            "re",
            "json",
            "time",
            "pathlib",
            "shutil",
            "typing",
            "logging",
            "subprocess",
            "csv",
        }:
            continue
        candidate_file = os.path.join(SCRIPTS_DIR, f"{name}.py")
        candidate_pkg = os.path.join(SCRIPTS_DIR, name, "__init__.py")
        if not (os.path.exists(candidate_file) or os.path.exists(candidate_pkg)):
            missing.add(name)
    return sorted(missing)


def ensure_init_py(dir_path: str, apply: bool, report_rows: list):
    py_files = [n for n in os.listdir(dir_path) if n.endswith(".py")]
    if py_files and "__init__.py" not in py_files:
        init_path = os.path.join(dir_path, "__init__.py")
        if apply:
            os.makedirs(dir_path, exist_ok=True)
            write_file(init_path, "# added by wire_joiner\n")
            report_rows.append(
                ["CREATE_INIT", init_path, "Created", "Package missing __init__.py"]
            )
        else:
            report_rows.append(
                [
                    "CREATE_INIT",
                    init_path,
                    "Would create",
                    "Package missing __init__.py",
                ]
            )


def scan_and_fix(apply: bool):
    report, rename_plan = [], []
    for root, dirs, files in os.walk(SCRIPTS_DIR):
        # package hygiene
        try:
            ensure_init_py(root, apply, report)
        except Exception as e:
            report.append(["ERROR_INIT", root, "Skip", f"{e}"])

        for name in files:
            if not name.endswith(".py"):
                continue
            path = os.path.join(root, name)

            # suggest rename if not *_READY.py
            if not name.endswith(KEEP_SUFFIX):
                rename_plan.append(
                    [path, f"suggest rename -> {os.path.splitext(path)[0]}_READY.py"]
                )

            original = read_file(path)
            fixed = normalize_text(original)

            actions = []
            if fixed != original:
                actions.append("normalize-text")

            if is_placeholder_only(fixed):
                fixed = "# placeholder stub (wire_joiner)\npass\n"
                actions.append("placeholder->stub")

            if actions and apply:
                try:
                    backup_file(path)
                    write_file(path, fixed)
                    report.append(["FIX_TEXT", path, "Updated", ",".join(actions)])
                except Exception as e:
                    report.append(["ERROR_WRITE", path, "Skip", str(e)])
            elif actions:
                report.append(
                    ["WOULD_FIX_TEXT", path, "Would update", ",".join(actions)]
                )

            ok, err = compile_check(path)
            if not ok:
                report.append(["COMPILE_FAIL", path, "Review", err])

            missing = guess_missing_local_imports(path)
            if missing:
                report.append(
                    [
                        "IMPORT_MAYBE_MISSING",
                        path,
                        "Check",
                        f"Unresolved? {', '.join(missing)}",
                    ]
                )

    return report, rename_plan


def write_reports(report, rename_plan):
    os.makedirs(OUT_DIR, exist_ok=True)
    rep = os.path.join(OUT_DIR, "wire_joiner_report.tsv")
    with open(rep, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["Issue", "Path", "Action", "Notes"])
        w.writerows(report)

    ren = os.path.join(OUT_DIR, "suggestions_rename.tsv")
    with open(ren, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["Path", "Suggestion"])
        w.writerows(rename_plan)
    return rep, ren


def main():
    apply = "--apply" in sys.argv
    ensure_dirs()
    report, rename_plan = scan_and_fix(apply)
    rep, ren = write_reports(report, rename_plan)
    print(f"Report: {rep}")
    print(f"Rename plan: {ren}")
    if apply:
        print(f"Backups saved under: {BACKUP_DIR}")
    else:
        print("Dry run (no changes). Add --apply to write fixes.")


if __name__ == "__main__":
    main()
# --- extra mojibake mappings (appended by setup) ---
BAD_CHARS.update(
    {"ðŸ": "", "â€™": "'", "â€œ": '"', "â€�": '"', "â€“": "-", "â€”": "-", "Â": ""}
)
# --- expanded mojibake/odd-char mappings (appended) ---
BAD_CHARS.update(
    {
        # C1 controls / non-printables commonly seen in logs
        "\u0080": "",
        "\u0081": "",
        "\u0082": "",
        "\u0083": "",
        "\u0084": "",
        "\u0085": "",
        "\u0086": "",
        "\u0087": "",
        "\u0088": "",
        "\u0089": "",
        "\u008a": "",
        "\u008b": "",
        "\u008c": "",
        "\u008d": "",
        "\u008e": "",
        "\u008f": "",
        "\u0090": "",
        "\u0091": "",
        "\u0092": "",
        "\u0093": "",
        "\u0094": "",
        "\u0095": "",
        "\u0096": "",
        "\u0097": "",
        "\u0098": "",
        "\u0099": "",
        "\u009a": "",
        "\u009b": "",
        "\u009c": "",
        "\u009d": "",
        "\u009e": "",
        "\u009f": "",
        # Latin-1 symbols often appearing broken
        "\u00a4": "",
        "\u00a5": "",
        "\u00a6": "",
        "\u00a8": "",
        "\u00ae": "",
        "\u00b0": "",
        "\u00b3": "",
        "\u00b4": "",
        "\u00b8": "",
        "\u00b9": "",
        # punctuation/dashes/quotes
        "\u2018": "'",
        "\u2019": "'",
        "\u201a": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u20ac": "€",
        "\u2122": "TM",
        # stray prefixes often seen with NBSP/Â
        "Â": "",
        "ðŸ": "",
        "â€™": "'",
        "â€œ": '"',
        "â€�": '"',
        "â€“": "-",
        "â€”": "-",
    }
)
