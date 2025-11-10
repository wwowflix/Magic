import importlib
import types


def test_import_scripts_phase18_module_P_18P_format_specific_roi_splitter_READY():
    mod = importlib.import_module(
        "scripts.phase18.module_P.18P_format_specific_roi_splitter_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
