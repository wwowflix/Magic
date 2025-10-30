import importlib, types


def test_import_scripts_phase00_INBOX__vegafusion_data_857633C0_857633C0():
    mod = importlib.import_module(
        "scripts.phase00.INBOX._vegafusion_data_857633C0_857633C0"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
