import importlib, types


def test_import_scripts_phase00_INBOX___pip_runner___127ADF2A_127ADF2A():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.__pip-runner___127ADF2A_127ADF2A"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
