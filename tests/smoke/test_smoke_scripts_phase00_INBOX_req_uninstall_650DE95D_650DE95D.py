import importlib, types


def test_import_scripts_phase00_INBOX_req_uninstall_650DE95D_650DE95D():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.req_uninstall_650DE95D_650DE95D"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
