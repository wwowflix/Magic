import json, os
import tools.self_healing_runner_v5_parallel as run

def test_build_task_list_from_manifest(tmp_path, monkeypatch):
    # minimal manifest with two entries
    entries = {"entries":[
        {"path":"scripts/phase0/module_a/A_READY.py","phase":0,"module":"A"},
        {"path":"scripts/phase1/module_b/B_READY.py","phase":1,"module":"B"},
    ], "count":2}
    mpath = tmp_path / "phase_manifest.json"; mpath.write_text(json.dumps(entries))
    tasks = run.load_tasks_from_manifest(str(mpath), phases=[0,1])
    assert len(tasks) == 2
    assert tasks[0]["phase"] == 0 and tasks[1]["phase"] == 1

def test_dry_run_executes_no_scripts(tmp_path, monkeypatch):
    monkeypatch.setattr(run, "execute_task", lambda *a, **k: 0)  # would be called if not dry-run
    rc, ran = run.run_from_manifest({"entries":[]}, dry_run=True)
    assert rc == 0 and ran == 0
