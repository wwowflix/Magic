import importlib
import types


def test_import_scripts_phase7_phase7_affiliate_handler_READY():
    mod = importlib.import_module("scripts.phase7.phase7_affiliate_handler_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
