import importlib, types


def test_import_scripts_phase00_INBOX_renderer_6ED72F00_6ED72F00():
    mod = importlib.import_module("scripts.phase00.INBOX.renderer_6ED72F00_6ED72F00")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
