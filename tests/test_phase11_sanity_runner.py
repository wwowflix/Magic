import tools.phase11_sanity_runner as runner


def test_sanity_runner_creates_log(tmp_path, monkeypatch):
    # Redirect log folder to temp
    log_dir = tmp_path / "logs"
    monkeypatch.setattr(runner, "LOG_DIR", log_dir)

    # Run the sanity runner (simulate Phase 11 Module A)
    runner.main(["11", "A"])

    # Check that a log file was created
    logs = list(log_dir.rglob("*.log"))
    assert logs, "No logs were created by sanity runner"

    # Ensure the log has content
    content = logs[0].read_text()
    assert "Sanity" in content or "Running" in content
