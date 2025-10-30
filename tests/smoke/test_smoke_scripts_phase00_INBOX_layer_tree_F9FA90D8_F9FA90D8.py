import importlib, types


def test_import_scripts_phase00_INBOX_layer_tree_F9FA90D8_F9FA90D8():
    mod = importlib.import_module("scripts.phase00.INBOX.layer_tree_F9FA90D8_F9FA90D8")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
