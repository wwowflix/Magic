import importlib, types


def test_import_scripts_phase00_INBOX__io_kqueue_BD20DAC0_BD20DAC0():
    mod = importlib.import_module("scripts.phase00.INBOX._io_kqueue_BD20DAC0_BD20DAC0")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
