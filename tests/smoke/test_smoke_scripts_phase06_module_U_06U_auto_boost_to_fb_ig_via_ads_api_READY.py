import importlib, types

def test_import_scripts_phase06_module_U_06U_auto_boost_to_fb_ig_via_ads_api_READY():
    mod = importlib.import_module("scripts.phase06.module_U.06U_auto_boost_to_fb_ig_via_ads_api_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
