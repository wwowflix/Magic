import tools.phase11_sanity_runner as runner


def test_sanity_runner_writes_log(tmp_path, monkeypatch):
    log_dir = tmp_path / "logs"
    monkeypatch.setattr(runner, "LOG_DIR", log_dir)
    rc = runner.run_once()
    assert rc in (0, 1)
    logs = list(log_dir.glob("*.log"))
    assert logs
