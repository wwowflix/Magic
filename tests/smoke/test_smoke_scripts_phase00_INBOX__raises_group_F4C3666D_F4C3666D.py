import importlib, types


def test_import_scripts_phase00_INBOX__raises_group_F4C3666D_F4C3666D():
    mod = importlib.import_module(
        "scripts.phase00.INBOX._raises_group_F4C3666D_F4C3666D"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
