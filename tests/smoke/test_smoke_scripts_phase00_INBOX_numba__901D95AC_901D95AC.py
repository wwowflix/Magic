import importlib, types


def test_import_scripts_phase00_INBOX_numba__901D95AC_901D95AC():
    mod = importlib.import_module("scripts.phase00.INBOX.numba__901D95AC_901D95AC")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
