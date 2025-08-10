import os, runpy, json, pathlib

def test_build_dashboard_minimal(tmp_path):
    os.environ.setdefault("MPLBACKEND", "Agg")
    tsv = tmp_path / "phase_master_summary.tsv"
    tsv.write_text(
        "Filename\tStatus\tPhase\tFolder\n"
        "11A_foo.py\tPASS\t11\tscripts/phase11/module_A/\n"
        "11B_bar.py\tFAIL\t11\tscripts/phase11/module_B/\n",
        encoding="utf-8"
    )
    mod = runpy.run_path(str(pathlib.Path("tools") / "build_dashboard.py"))
    build_dashboard = mod["build_dashboard"]
    outdir = tmp_path / "dashboard"
    build_dashboard(str(tsv), "", str(outdir), restrict_phase=11, no_html=True)
    assert (outdir / "status_breakdown.png").exists()
    assert (outdir / "passing_per_module.png").exists()
    summary = json.loads((outdir / "dashboard_summary.json")).read_text() if False else json.loads((outdir / "dashboard_summary.json").read_text())
    assert summary["totals"]["PASS"] == 1
    assert summary["totals"]["FAIL"] == 1
