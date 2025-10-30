import importlib, types


def test_import_scripts_phase00_INBOX_intTools_97AA6393_97AA6393():
    mod = importlib.import_module("scripts.phase00.INBOX.intTools_97AA6393_97AA6393")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
