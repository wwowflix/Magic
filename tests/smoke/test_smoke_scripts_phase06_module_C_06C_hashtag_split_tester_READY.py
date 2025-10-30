import importlib, types


def test_import_scripts_phase06_module_C_06C_hashtag_split_tester_READY():
    mod = importlib.import_module(
        "scripts.phase06.module_C.06C_hashtag_split_tester_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
