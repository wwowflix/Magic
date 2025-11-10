import importlib, types


def test_import_scripts_phase00_INBOX_install_egg_info_5C37C15E_5C37C15E():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.install_egg_info_5C37C15E_5C37C15E"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
