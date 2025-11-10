import importlib, types


def test_import_scripts_phase00_INBOX_shapes_C6F05421_C6F05421():
    mod = importlib.import_module("scripts.phase00.INBOX.shapes_C6F05421_C6F05421")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
