import importlib, types


def test_import_scripts_phase00_INBOX_py3k_2_D8408B34_D8408B34():
    mod = importlib.import_module("scripts.phase00.INBOX.py3k_2_D8408B34_D8408B34")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
