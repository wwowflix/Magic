import importlib, types


def test_import_scripts_phase00_INBOX_c_parser_wrapper_B9AD05FB_B9AD05FB():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.c_parser_wrapper_B9AD05FB_B9AD05FB"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
