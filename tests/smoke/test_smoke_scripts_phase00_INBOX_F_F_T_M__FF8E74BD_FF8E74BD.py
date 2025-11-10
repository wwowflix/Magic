import importlib, types


def test_import_scripts_phase00_INBOX_F_F_T_M__FF8E74BD_FF8E74BD():
    mod = importlib.import_module("scripts.phase00.INBOX.F_F_T_M__FF8E74BD_FF8E74BD")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
