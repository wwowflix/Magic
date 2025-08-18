# tests/test_phase11_sanity_runner_extra.py
import tools.phase11_sanity_runner as runner
import os
import stat


def test_main_no_args_prints_usage(capsys):
    rc = runner.main([])
    out = capsys.readouterr().out + capsys.readouterr().err
    assert rc != 0
    assert "Usage:" in out or "phase" in out


def test_run_once_ok(tmp_path, monkeypatch):
    monkeypatch.setattr(runner, "LOG_DIR", tmp_path / "logs")
    assert runner.run_once() is True


def test_run_once_handles_io_error(tmp_path, monkeypatch):
    # Make LOG_DIR unwritable
    bad = tmp_path / "bad"
    bad.mkdir()
    os.chmod(bad, stat.S_IREAD)  # readonly
    monkeypatch.setattr(runner, "LOG_DIR", bad)
    try:
        assert runner.run_once() in (False, None)
    finally:
        # restore to allow tmp cleanup on Windows
        os.chmod(bad, stat.S_IWRITE)
