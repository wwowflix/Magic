import importlib, types


def test_import_scripts_phase00_INBOX_ext_4EE95D24_4EE95D24():
    mod = importlib.import_module("scripts.phase00.INBOX.ext_4EE95D24_4EE95D24")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
