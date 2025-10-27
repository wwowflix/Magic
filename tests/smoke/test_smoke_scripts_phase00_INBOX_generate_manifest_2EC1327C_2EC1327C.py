import importlib, types

def test_import_scripts_phase00_INBOX_generate_manifest_2EC1327C_2EC1327C():
    mod = importlib.import_module("scripts.phase00.INBOX.generate_manifest_2EC1327C_2EC1327C")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
