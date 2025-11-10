import importlib
import types


def test_import_scripts_phase18_module_B_18B_link_cloaking_bitly_integration_READY():
    mod = importlib.import_module(
        "scripts.phase18.module_B.18B_link_cloaking_bitly_integration_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
