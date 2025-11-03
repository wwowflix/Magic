from __future__ import annotations

import argparse
import datetime
import json
import subprocess
import sys
from pathlib import Path

# project root Ã¢â€ â€™ E:\MAGIC
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def normalize_path(raw: str) -> Path:
    """Normalize manifest paths like '../scripts/...' into project-rooted paths."""
    if not raw:
        return PROJECT_ROOT
    raw_clean = raw.replace("\\", "/")
    p = Path(raw)

    # 1) absolute path Ã¢â€ â€™ just return
    if p.is_absolute():
        return p

    # 2) strip leading ../ segments
    while raw_clean.startswith("../"):
        raw_clean = raw_clean[3:]

    # 3) join with project root
    return (PROJECT_ROOT / raw_clean).resolve()


def load_manifest(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8-sig") as f:
        data = json.load(f)

    # your manifests are list-of-dicts, but we also support {"items": [...]} shape
    if isinstance(data, dict):
        items = data.get("items") or data.get("scripts") or []
    else:
        items = data
    return items


def run_script(script_path: Path) -> tuple[bool, str, str]:
    try:
        # run from project root so relative imports work
        proc = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
        )
        return proc.returncode == 0, proc.stdout, proc.stderr
    except Exception as e:  # pragma: no cover
        return False, "", str(e)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, help="Path to JSON manifest")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    items = load_manifest(manifest_path)

    print(f"Selected count: {len(items)}")

    results: list[tuple[str, str]] = []

    for item in items:
        raw_path = (
            item.get("Path")
            or item.get("path")
            or item.get("script")
            or item.get("FinalFilename")
            or ""
        )

        script_path = normalize_path(raw_path)
        print(f"-> {script_path}")

        if not script_path.exists():
            print(f"[MISS] {script_path} (file not found)")
            results.append((str(script_path), "MISS"))
            continue

        ok, out, err = run_script(script_path)
        if ok:
            # your stubs already print "[OK] ... executed (stub)." so don't duplicate too much
            msg = out.strip() or f"[OK] {script_path.name} executed."
            print(msg)
            results.append((str(script_path), "OK"))
        else:
            print(f"[FAIL] {script_path} -> {err.strip()}")
            results.append((str(script_path), "FAIL"))

    # write summary
    summaries_dir = PROJECT_ROOT / "tools" / "outputs" / "summaries"
    summaries_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_path = summaries_dir / f"phase11_module_{module}_summary_{ts}.tsv"
    with summary_path.open("w", encoding="utf-8", newline="") as f:
        f.write("script\tstatus\n")
        for script, status in results:
            f.write(f"{script}\t{status}\n")

    print(f"Wrote summary: {summary_path}")


if __name__ == "__main__":
    main()
