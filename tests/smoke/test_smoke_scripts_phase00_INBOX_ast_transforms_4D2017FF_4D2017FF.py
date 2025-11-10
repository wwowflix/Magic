import importlib, types


def test_import_scripts_phase00_INBOX_ast_transforms_4D2017FF_4D2017FF():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.ast_transforms_4D2017FF_4D2017FF"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
