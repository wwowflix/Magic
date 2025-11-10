import importlib, types


def test_import_scripts_phase00_INBOX_sax_09D3B1BA_09D3B1BA():
    mod = importlib.import_module("scripts.phase00.INBOX.sax_09D3B1BA_09D3B1BA")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
