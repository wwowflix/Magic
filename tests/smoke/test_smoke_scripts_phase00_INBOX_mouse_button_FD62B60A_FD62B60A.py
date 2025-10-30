import importlib, types


def test_import_scripts_phase00_INBOX_mouse_button_FD62B60A_FD62B60A():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.mouse_button_FD62B60A_FD62B60A"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
