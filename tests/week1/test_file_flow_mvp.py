from pathlib import Path

from tools.mvp.file_flow_mvp import scan_folder, FileRecord


def test_file_flow_basic() -> None:
    here = Path(__file__).resolve().parents[2] / "tools"
    records = scan_folder(here)
    assert isinstance(records, list)

    if records:
        first = records[0]
        assert isinstance(first, FileRecord)
        assert isinstance(first.path, str)
        assert isinstance(first.size, int)
