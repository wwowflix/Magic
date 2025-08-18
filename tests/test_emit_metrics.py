from pathlib import Path
import json
from tools.emit_metrics_from_summaries import emit_metrics


def test_emit_metrics_builds_json(tmp_path: Path):
    sdir = tmp_path / "outputs" / "summaries"
    sdir.mkdir(parents=True)
    (sdir / "sample.tsv").write_text(
        "Filename\tStatus\tPhase\tFolder\n"
        "11A_a.py\tPASS\t11\ta\n"
        "11B_b.py\tFAIL\t11\tb\n"
        "12A_c.py\tPASS\t12\tc\n",
        encoding="utf-8",
    )
    out = tmp_path / "outputs" / "logs" / "agent_metrics"
    p = emit_metrics(str(sdir), str(out))
    data = json.loads(Path(p).read_text(encoding="utf-8"))
    assert data["totals"]["PASS"] == 2
    assert data["totals"]["FAIL"] == 1
    assert data["by_phase"]["11"]["FAIL"] == 1
