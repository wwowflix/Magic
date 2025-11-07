import importlib, types


def test_import_scripts__appengine_environ():
    mod = importlib.import_module("scripts._appengine_environ")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
