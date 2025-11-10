import importlib
import types


def test_import_scripts_phase18_module_K_18K_email_upsell_detector_READY():
    mod = importlib.import_module(
        "scripts.phase18.module_K.18K_email_upsell_detector_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
