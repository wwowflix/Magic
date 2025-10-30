import importlib, types


def test_import_scripts_phase08_module_B_08B_user_reaction_scraper_READY():
    mod = importlib.import_module(
        "scripts.phase08.module_B.08B_user_reaction_scraper_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
