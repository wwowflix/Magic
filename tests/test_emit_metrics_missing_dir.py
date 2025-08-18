from pathlib import Path
import json
from tools.emit_metrics_from_summaries import emit_metrics


def test_emit_metrics_missing_dir(tmp_path: Path):
    missing = tmp_path / "no_summaries_here"
    out = tmp_path / "metrics"
    emit_metrics(str(missing), str(out))
    data = json.loads((out / "agent_metrics.json").read_text(encoding="utf-8"))
    assert data["totals"] == {}
    assert data["by_phase"] == {}
