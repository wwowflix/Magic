import importlib, types


def test_import_scripts_phase00_INBOX_pointInsidePen_9E8114BC_9E8114BC():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.pointInsidePen_9E8114BC_9E8114BC"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
