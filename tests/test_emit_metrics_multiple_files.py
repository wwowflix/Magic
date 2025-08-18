import json
from pathlib import Path
from tools.emit_metrics_from_summaries import emit_metrics


def test_emit_metrics_multiple_files(tmp_path: Path):
    sdir = tmp_path / "outputs" / "summaries"
    sdir.mkdir(parents=True)
    # first file
    (sdir / "one.tsv").write_text(
        "Filename\tStatus\tPhase\tFolder\n" "a.py\tPASS\t1\tphase1\n", encoding="utf-8"
    )
    # second file
    (sdir / "two.tsv").write_text(
        "Filename\tStatus\tPhase\tFolder\n" "b.py\tFAIL\t2\tphase2\n", encoding="utf-8"
    )
    out = tmp_path / "outputs" / "metrics"
    emit_metrics(str(sdir), str(out))
    data = json.loads((out / "agent_metrics.json").read_text(encoding="utf-8"))
    assert data["totals"]["PASS"] == 1
    assert data["totals"]["FAIL"] == 1
    assert "1" in data["by_phase"]
    assert "2" in data["by_phase"]
