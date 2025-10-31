import importlib
import types


def test_import_scripts_phase18_module_B_18B_affiliate_click_tracking_READY():
    mod = importlib.import_module(
        "scripts.phase18.module_B.18B_affiliate_click_tracking_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
