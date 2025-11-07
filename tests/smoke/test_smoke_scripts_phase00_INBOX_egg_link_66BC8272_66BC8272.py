import importlib, types


def test_import_scripts_phase00_INBOX_egg_link_66BC8272_66BC8272():
    mod = importlib.import_module("scripts.phase00.INBOX.egg_link_66BC8272_66BC8272")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
