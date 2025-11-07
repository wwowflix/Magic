import importlib, types


def test_import_scripts_phase00_INBOX__musllinux_FCA1A063_FCA1A063():
    mod = importlib.import_module("scripts.phase00.INBOX._musllinux_FCA1A063_FCA1A063")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
