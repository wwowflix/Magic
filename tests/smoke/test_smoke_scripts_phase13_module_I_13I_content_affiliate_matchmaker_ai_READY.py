import importlib, types


def test_import_scripts_phase13_module_I_13I_content_affiliate_matchmaker_ai_READY():
    mod = importlib.import_module(
        "scripts.phase13.module_I.13I_content_affiliate_matchmaker_ai_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
