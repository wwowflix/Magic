import importlib, types

def test_import_scripts_phase08_module_J_08J_content_recipe_optimizer_READY():
    mod = importlib.import_module("scripts.phase08.module_J.08J_content_recipe_optimizer_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
