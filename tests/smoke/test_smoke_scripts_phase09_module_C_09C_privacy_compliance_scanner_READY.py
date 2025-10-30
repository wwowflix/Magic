import importlib, types


def test_import_scripts_phase09_module_C_09C_privacy_compliance_scanner_READY():
    mod = importlib.import_module(
        "scripts.phase09.module_C.09C_privacy_compliance_scanner_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
