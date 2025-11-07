import importlib
import types


def test_import_scripts_phase18_module_M_18M_sponsorship_offer_expiry_notifier_READY():
    mod = importlib.import_module(
        "scripts.phase18.module_M.18M_sponsorship_offer_expiry_notifier_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
