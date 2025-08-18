import json
from pathlib import Path
from tools.emit_metrics_from_summaries import emit_metrics


def test_emit_metrics_with_phase_column_but_no_rows(tmp_path: Path):
    sdir = tmp_path / "outputs" / "summaries"
    sdir.mkdir(parents=True)
    # header only, no data rows
    (sdir / "empty.tsv").write_text("Filename\tStatus\tPhase\tFolder\n", encoding="utf-8")
    out = tmp_path / "outputs" / "metrics"
    emit_metrics(str(sdir), str(out))
    data = json.loads((out / "agent_metrics.json").read_text(encoding="utf-8"))
    assert data["totals"] == {}
    assert data["by_phase"] == {}
