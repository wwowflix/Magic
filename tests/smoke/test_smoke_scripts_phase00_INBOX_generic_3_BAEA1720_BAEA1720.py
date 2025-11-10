import importlib, types


def test_import_scripts_phase00_INBOX_generic_3_BAEA1720_BAEA1720():
    mod = importlib.import_module("scripts.phase00.INBOX.generic_3_BAEA1720_BAEA1720")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
