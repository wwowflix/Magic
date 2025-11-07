import importlib, types


def test_import_scripts_phase00_INBOX_mips_F6BAAEA1_F6BAAEA1():
    mod = importlib.import_module("scripts.phase00.INBOX.mips_F6BAAEA1_F6BAAEA1")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
