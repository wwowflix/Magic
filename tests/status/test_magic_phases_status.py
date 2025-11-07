import os
from pathlib import Path
from datetime import datetime, timedelta

ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT / "outputs" / "reports"
SNAPSHOT = REPORTS_DIR / "release_status_snapshot.txt"
WORKFLOW = ROOT / ".github" / "workflows" / "tests.yml"
COVERAGE_XML = REPORTS_DIR / "coverage.xml"


def read_snapshot_lines():
    if not SNAPSHOT.exists():
        return {}
    data = {}
    raw = SNAPSHOT.read_text(encoding="utf-8")
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        # strip BOM if present
        if key.startswith("\ufeff"):
            key = key.lstrip("\ufeff")
        data[key] = val
    return data


def test_phase1_restore_visibility():
    """
    PHASE 1 – RESTORE VISIBILITY
    """
    assert REPORTS_DIR.exists(), "outputs/reports must exist (Phase 1.1 / 1.3)"
    snap = read_snapshot_lines()
    assert snap, "release_status_snapshot.txt must exist and be readable"

    # minimal required fields
    assert "Date" in snap, f"snapshot must contain Date (got keys: {list(snap.keys())})"
    assert "Repo" in snap, "snapshot must contain Repo"
    assert "Reports" in snap, "snapshot must contain Reports"

    # scheduler line must NOT kill the run – any safe text is allowed
    sched = snap.get("Scheduler", "")
    assert sched != "", "snapshot should contain Scheduler line"
    assert any(
        word in sched for word in ("SKIPPED", "MISSING", "OK", "access denied")
    ), f"unexpected scheduler line: {sched}"


def test_phase2_stabilize_via_ci_files_present():
    """
    PHASE 2 – STABILIZE VIA CI
    """
    assert WORKFLOW.exists(), ".github/workflows/tests.yml must exist"

    wf_text = WORKFLOW.read_text(encoding="utf-8")
    must_have = [
        "Upload dashboard artifacts",
        "actions/upload-artifact@v4",
        "path: outputs/reports/",
    ]
    for needle in must_have:
        assert needle in wf_text, f"workflow missing required line: {needle}"


def test_phase2_coverage_fresh_enough():
    """
    PHASE 2 – coverage should be produced recently.
    """
    assert COVERAGE_XML.exists(), "coverage.xml must exist (you had it locally)"
    mtime = datetime.fromtimestamp(COVERAGE_XML.stat().st_mtime)
    age = datetime.now() - mtime
    assert age < timedelta(days=1, hours=1), f"coverage.xml too old: {age}"


def test_phase3_not_started_but_safe():
    """
    PHASE 3 – CLEAN + RELEASE
    """
    assert SNAPSHOT.exists(), "Phase 3 cannot start if visibility snapshot is missing"
