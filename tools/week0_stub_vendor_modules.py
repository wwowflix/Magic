from __future__ import annotations

"""
MAGIC Week 0 – Vendor/Experimental Module Stubber (final)

Goal:
- For any scripts.* module that is experimental, backup, or too heavy
  for Week 0 (CLI, unicode experiments, bs4 copies, etc.),
  replace it with a tiny Week 0 stub that is safe to import.
- Always keep a *.magic_bak_week0 backup of the original.

USAGE:
    (venv) PS E:\\MAGIC> python tools/week0_stub_vendor_modules.py
"""

from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"

# Week 0: list of modules (filenames, no ".py") to stub
STUB_MODULES: list[str] = [
    # bs4 backup copies
    "css_2_MAGIC_backup",
    "dammit_2_MAGIC_backup",
    "dammit_MAGIC_backup",
    "filter_2",
    "formatter_2",

    # Unicode / encoding experiments
    "deduplicate_records_2",
    "encoding_test",
    "enhanced_twitter_scraper_2",
    "ingest_csvs_to_db_2",
    "setup_folders_2",
    "standardize_columns_2",
    "test_imports",
    "test_numpy_clean_2",
    "validate_schema_2",
    "validation_checks_2",

    # bs4 tests relying on bs4 as a package
    "test_builder",
    "test_builder_2",
    "test_element",
    "test_element_2",
    "test_arrow",

    # env-specific tests
    "test_system_info",
    "test_user_agent",

    # table unbuilder which imports missing TableUnbuilder
    "unbuilder",
]


def stub_content(name: str) -> str:
    """
    Generic minimal stub.

    It keeps imports happy for Week 0, while the original file is
    preserved as name.py.magic_bak_week0 for future real implementation.
    """
    return dedent(
        f"""\
        from __future__ import annotations

        \\"\\\"MAGIC Week 0 stub for scripts.{name}.

        This module was auto-generated to keep imports cheap and safe.
        The original file is preserved as {name}.py.magic_bak_week0.
        \\"\\\"

        def _magic_week0_stub() -> None:  # pragma: no cover
            \\"\\\"No-op placeholder for Week 0.\\"\\\"
            return None
        """
    )


def main() -> int:
    for mod in STUB_MODULES:
        target = SCRIPTS_DIR / f"{mod}.py"
        backup = SCRIPTS_DIR / f"{mod}.py.magic_bak_week0"

        if not target.exists():
            print(f"[SKIP] {mod}: {target} does not exist")
            continue

        if not backup.exists():
            target.rename(backup)
            print(f"[BACKUP] {mod}: {backup.name} created")
        else:
            print(f"[BACKUP] {mod}: backup already exists")

        content = stub_content(mod)
        target.write_text(content, encoding="utf-8")
        print(f"[STUB] {mod}: replaced with Week 0 stub")

    print("Week 0 stubbing pass complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
