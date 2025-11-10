import importlib, types


def test_import_scripts_phase00_INBOX_solver_B8C78FC1_B8C78FC1():
    mod = importlib.import_module("scripts.phase00.INBOX.solver_B8C78FC1_B8C78FC1")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
