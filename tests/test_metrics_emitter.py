import os, subprocess, sys

def test_metrics_emitter(tmp_path):
    # Create fake summary TSV
    out_dir = tmp_path / "outputs" / "summaries"
    out_dir.mkdir(parents=True)
    (out_dir / "phase11_module_C_summary.tsv").write_text("Script\tStatus\nx.py\tPASS\ny.py\tFAIL\n", encoding="utf-8")

    # Copy emitter into tmp
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    src = os.path.join(repo_root, "tools", "emit_metrics_from_summaries.py")
    tools_dir = tmp_path / "tools"
    tools_dir.mkdir()
    (tools_dir / "emit_metrics_from_summaries.py").write_text(open(src, "r", encoding="utf-8").read(), encoding="utf-8")

    # Run
    result = subprocess.run([sys.executable, str(tools_dir / "emit_metrics_from_summaries.py")], cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 0
    # Verify JSON emitted
    metrics_dir = tmp_path / "outputs" / "metrics"
    files = list(metrics_dir.glob("*.json"))
    assert files, "metrics json not written"
