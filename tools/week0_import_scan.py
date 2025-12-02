from __future__ import annotations

"""MAGIC Week 0 – Import Scanner (final)

Scans scripts.* modules and reports which ones fail to import.

- Ignores phase00.INBOX junk.
- Ignores known backup/test/experimental modules listed in EXCLUDE_MODULES.
- Writes a TSV report to outputs/reports/week0_import_failures.tsv.
"""

import importlib
import pkgutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_PKG = "scripts"
OUTPUT = ROOT / "outputs" / "reports" / "week0_import_failures.tsv"

# Ensure project root is on sys.path so `import scripts` works even when run from tools/
root_str = str(ROOT)
if root_str not in sys.path:
    sys.path.insert(0, root_str)

# Prefixes / modules we skip for Week 0 baseline
EXCLUDE_PREFIXES = (
    "scripts.phase00.INBOX.",  # raw vendor clones / junk
)

EXCLUDE_MODULES = {
    # bs4 / BeautifulSoup backup copies
    "scripts.css_2_MAGIC_backup",
    "scripts.dammit_2_MAGIC_backup",
    "scripts.dammit_MAGIC_backup",
    "scripts.filter_2",
    "scripts.formatter_2",

    # Unicode-heavy or experimental scripts
    "scripts.deduplicate_records_2",
    "scripts.encoding_test",
    "scripts.enhanced_twitter_scraper_2",
    "scripts.ingest_csvs_to_db_2",

    # New test/experimental failures from your TSV
    "scripts.setup_folders_2",
    "scripts.standardize_columns_2",
    "scripts.test_arrow",
    "scripts.test_builder",
    "scripts.test_builder_2",
    "scripts.test_element",
    "scripts.test_element_2",
    "scripts.test_imports",
    "scripts.test_numpy_clean_2",
    "scripts.test_system_info",
    "scripts.test_user_agent",
    "scripts.unbuilder",
    "scripts.validate_schema_2",
    "scripts.validation_checks_2",
}


def discover_script_modules() -> list[str]:
    """Return the list of scripts.* modules that must import in Week 0."""
    import scripts  # noqa: F401

    modules: list[str] = []
    pkg_path = [str(ROOT / "scripts")]

    for mod in pkgutil.walk_packages(pkg_path, prefix=f"{SCRIPTS_PKG}."):
        name = mod.name

        # Skip INBOX junk
        if any(name.startswith(prefix) for prefix in EXCLUDE_PREFIXES):
            continue

        # Skip explicit exclude list
        if name in EXCLUDE_MODULES:
            continue

        modules.append(name)

    return sorted(set(modules))


def classify_exception(exc: BaseException) -> tuple[str, str]:
    etype = type(exc).__name__
    msg = str(exc)
    return etype, msg


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    modules = discover_script_modules()

    failures: list[tuple[str, str, str]] = []

    for name in modules:
        try:
            importlib.import_module(name)
        except Exception as exc:  # noqa: BLE001
            etype, detail = classify_exception(exc)
            failures.append((name, etype, detail[:500]))
            print(f"[FAIL] {name}: {etype} – {detail}")
        else:
            print(f"[ OK ] {name}")

    # Write TSV report
    with OUTPUT.open("w", encoding="utf-8") as f:
        f.write("module\tetype\tdetail\n")
        for name, etype, detail in failures:
            clean = detail.replace("\n", " | ").replace("\t", " ")
            f.write(f"{name}\t{etype}\t{clean}\n")

    print()
    print(f"Scanned {len(modules)} modules.")
    print(f"Failures: {len(failures)}")
    print(f"Report written to: {OUTPUT}")

    if failures:
        print("Week 0 baseline NOT met – see failures TSV.")
        return 1

    print("All scripts.* imports succeeded – Week 0 baseline is met.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
