import importlib
import types


def test_import_scripts_phase18_module_R_18R_affiliate_link_expiration_watcher_READY():
    mod = importlib.import_module(
        "scripts.phase18.module_R.18R_affiliate_link_expiration_watcher_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
