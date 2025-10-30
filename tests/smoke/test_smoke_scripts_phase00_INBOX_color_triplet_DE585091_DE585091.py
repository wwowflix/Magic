import importlib, types


def test_import_scripts_phase00_INBOX_color_triplet_DE585091_DE585091():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.color_triplet_DE585091_DE585091"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
