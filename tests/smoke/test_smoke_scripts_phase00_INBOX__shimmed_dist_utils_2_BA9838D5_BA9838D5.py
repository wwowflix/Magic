import importlib, types


def test_import_scripts_phase00_INBOX__shimmed_dist_utils_2_BA9838D5_BA9838D5():
    mod = importlib.import_module(
        "scripts.phase00.INBOX._shimmed_dist_utils_2_BA9838D5_BA9838D5"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
