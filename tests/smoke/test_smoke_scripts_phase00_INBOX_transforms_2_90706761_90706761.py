import importlib, types


def test_import_scripts_phase00_INBOX_transforms_2_90706761_90706761():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.transforms_2_90706761_90706761"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
