import importlib, types


def test_import_scripts_dashboard_magic_ops_dashboard():
    mod = importlib.import_module("scripts.dashboard.magic_ops_dashboard")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
