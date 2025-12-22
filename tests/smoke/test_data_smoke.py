"""
MAGIC Week 1 – Data Flow MVP smoketest (W1D1-3)

Covers:
- Import safety for scripts.data_flow_mvp.
- End-to-end pipeline over data/demo.json.
"""

from pathlib import Path

from scripts import data_flow_mvp


def test_data_flow_mvp_imports():
    # Basic import smoke – nothing should explode at import time.
    assert hasattr(data_flow_mvp, "run_pipeline")


def test_data_flow_mvp_runs_end_to_end(tmp_path):
    demo_path = Path("data/demo.json")
    assert demo_path.exists(), "Expected data/demo.json to exist for Week-1 MVP"

    output_path = tmp_path / "normalized.json"

    result = data_flow_mvp.run_pipeline(demo_path, output_path)

    # Basic shape checks
    assert isinstance(result, dict)
    assert result.get("schema_version") == "1.0"
    assert isinstance(result.get("modules"), list)
    assert result.get("module_count") == len(result["modules"])

    # Output should be written
    assert output_path.exists()
    text = output_path.read_text(encoding="utf-8")
    assert "Demo Data Module" in text
