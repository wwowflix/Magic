import importlib
import types


def test_import_scripts_phase18_module_G_18G_dynamic_cta_tester_READY():
    mod = importlib.import_module(
        "scripts.phase18.module_G.18G_dynamic_cta_tester_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
