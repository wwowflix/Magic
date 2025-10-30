import importlib, types


def test_import_scripts_phase00_INBOX_legacy_A06BD866_A06BD866():
    mod = importlib.import_module("scripts.phase00.INBOX.legacy_A06BD866_A06BD866")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
