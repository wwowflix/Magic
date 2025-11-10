import importlib, types


def test_import_scripts_phase00_INBOX__eventloop_2_B7FB40C0_B7FB40C0():
    mod = importlib.import_module(
        "scripts.phase00.INBOX._eventloop_2_B7FB40C0_B7FB40C0"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
