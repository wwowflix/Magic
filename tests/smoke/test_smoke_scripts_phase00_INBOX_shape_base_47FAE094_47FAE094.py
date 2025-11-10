import importlib, types


def test_import_scripts_phase00_INBOX_shape_base_47FAE094_47FAE094():
    mod = importlib.import_module("scripts.phase00.INBOX.shape_base_47FAE094_47FAE094")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
