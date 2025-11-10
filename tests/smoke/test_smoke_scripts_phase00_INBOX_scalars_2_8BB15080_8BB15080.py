import importlib, types


def test_import_scripts_phase00_INBOX_scalars_2_8BB15080_8BB15080():
    mod = importlib.import_module("scripts.phase00.INBOX.scalars_2_8BB15080_8BB15080")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
