import importlib, types


def test_import_scripts_phase00_INBOX_dtype_5_CC03427B_CC03427B():
    mod = importlib.import_module("scripts.phase00.INBOX.dtype_5_CC03427B_CC03427B")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
