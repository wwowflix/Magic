import importlib, types


def test_import_scripts_phase14_module_E_14E_content_lifecycle_advisor_READY():
    mod = importlib.import_module(
        "scripts.phase14.module_E.14E_content_lifecycle_advisor_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
