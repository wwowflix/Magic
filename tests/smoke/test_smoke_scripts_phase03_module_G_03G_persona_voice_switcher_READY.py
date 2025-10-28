import importlib, types

def test_import_scripts_phase03_module_G_03G_persona_voice_switcher_READY():
    mod = importlib.import_module("scripts.phase03.module_G.03G_persona_voice_switcher_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
