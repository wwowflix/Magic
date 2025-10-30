import importlib, types


def test_import_scripts_phase00_INBOX_umath_tests_4C71C87A_4C71C87A():
    mod = importlib.import_module("scripts.phase00.INBOX.umath_tests_4C71C87A_4C71C87A")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
