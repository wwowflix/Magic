import os
import io
import sys
import ast
import re
from pathlib import Path

# ---- Config ----
ROOT = Path(__file__).resolve().parents[1]
INCLUDE_SUFFIXES = {".py"}  # scan only Python sources
EXCLUDE_TOP = {
    ".git",
    "venv",
    "outputs",
    "backups",
    "quarantine",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "__pycache__",
}
MAX_LINE_LEN = 120

SMART_JUNK = re.compile(
    r"[\uFFFD\u200B\u2018\u2019\u201C\u201D\u2013\u2014]"
)  # replacement/ZWSP/smart quotes/dashes


def iter_repo_files():
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        # exclude top-level dirs quickly
        parts = p.relative_to(ROOT).parts
        if parts and parts[0] in EXCLUDE_TOP:
            continue
        if p.suffix.lower() in INCLUDE_SUFFIXES:
            yield p


def read_bytes(path: Path) -> bytes:
    with open(path, "rb") as fh:
        return fh.read()


def read_text_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="strict")


def has_bom(data: bytes) -> bool:
    return data.startswith(b"\xef\xbb\xbf")


def newline_style(data: bytes) -> str:
    # detects if CRLF present
    return "CRLF" if b"\r\n" in data else "LF"


# ---------- Tests ----------


def test_utf8_decodable_and_no_bom():
    bad = []
    for p in iter_repo_files():
        b = read_bytes(p)
        # No BOM
        if has_bom(b):
            bad.append(f"{p}  (BOM present)")
            continue
        # UTF-8 strict decode must succeed
        try:
            b.decode("utf-8", "strict")
        except UnicodeDecodeError as e:
            bad.append(f"{p}  (decode error: {e})")
    assert not bad, "Files failed UTF-8 strict decode or contain BOM:\n" + "\n".join(
        bad
    )


def test_no_crlf_in_python_sources():
    offenders = []
    for p in iter_repo_files():
        if newline_style(read_bytes(p)) == "CRLF":
            offenders.append(str(p))
    assert not offenders, "Found CRLF newlines in .py files (use LF):\n" + "\n".join(
        offenders
    )


def test_no_tabs_and_no_trailing_spaces():
    issues = []
    for p in iter_repo_files():
        for i, line in enumerate(read_text_utf8(p).splitlines()):
            if "\t" in line:
                issues.append(f"{p}:{i+1}  contains TAB")
            if line.rstrip() != line:
                issues.append(f"{p}:{i+1}  trailing whitespace")
    assert not issues, "Tab or trailing space violations:\n" + "\n".join(issues)


def test_line_lengths_under_limit():
    long_lines = []
    for p in iter_repo_files():
        for i, line in enumerate(read_text_utf8(p).splitlines()):
            if len(line) > MAX_LINE_LEN:
                long_lines.append(f"{p}:{i+1}  {len(line)} > {MAX_LINE_LEN}")
    assert not long_lines, f"Lines exceed {MAX_LINE_LEN} columns:\n" + "\n".join(
        long_lines
    )


def test_no_smart_quotes_or_zwsp_or_fffd():
    bad = []
    for p in iter_repo_files():
        text = read_text_utf8(p)
        if SMART_JUNK.search(text):
            bad.append(str(p))
    assert not bad, "Smart quotes/ZWSP/FFFD found in:\n" + "\n".join(bad)


def test_ast_parses_cleanly():
    errors = []
    for p in iter_repo_files():
        try:
            ast.parse(read_text_utf8(p), filename=str(p))
        except SyntaxError as e:
            errors.append(f"{p}:{e.lineno}:{e.offset}  {e.msg}")
    assert not errors, "AST parse errors:\n" + "\n".join(errors)


# ---- Optional: Black check (skips if black not installed) ----
def test_black_is_clean_if_available():
    try:
        import black  # noqa: F401
    except Exception:
        import pytest

        pytest.skip("black not installed")
    else:
        # Run black in check mode via its API for speed
        from black import Mode, FileMode
        from black import format_str

        failures = []
        mode = Mode() if hasattr(Mode, "__call__") else FileMode()
        for p in iter_repo_files():
            src = read_text_utf8(p)
            try:
                formatted = format_str(src, mode=mode)
            except Exception as e:
                failures.append(f"{p}  black error: {e}")
                continue
            if formatted != src:
                failures.append(str(p))
        assert not failures, "Black would reformat these files:\n" + "\n".join(failures)


# ---- Optional: mypy check (skips if mypy not installed) ----
def test_mypy_repo_if_available():
    try:
        from mypy import api as mypy_api
    except Exception:
        import pytest

        pytest.skip("mypy not installed")
        return
    # Limit scope to speed; adjust as needed
    args = ["--exclude", r"(backups|quarantine|outputs|venv)", str(ROOT)]
    out, err, status = mypy_api.run(args)
    if status != 0:
        raise AssertionError("mypy errors:\n" + out + err)
