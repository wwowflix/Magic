import importlib, types

def test_import_scripts__io_epoll():
    mod = importlib.import_module("scripts._io_epoll")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
