import importlib, types

def test_import_scripts_phase00_INBOX_bbcode_D03D3D51_D03D3D51():
    mod = importlib.import_module("scripts.phase00.INBOX.bbcode_D03D3D51_D03D3D51")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
