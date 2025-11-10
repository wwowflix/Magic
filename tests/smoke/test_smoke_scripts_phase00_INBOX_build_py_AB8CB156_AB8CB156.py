import importlib, types


def test_import_scripts_phase00_INBOX_build_py_AB8CB156_AB8CB156():
    mod = importlib.import_module("scripts.phase00.INBOX.build_py_AB8CB156_AB8CB156")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
