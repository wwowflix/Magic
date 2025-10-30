import importlib, types


def test_import_scripts_phase10_module_U_10U_shorts_hashtag_auto_matcher_READY():
    mod = importlib.import_module(
        "scripts.phase10.module_U.10U_shorts_hashtag_auto_matcher_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
