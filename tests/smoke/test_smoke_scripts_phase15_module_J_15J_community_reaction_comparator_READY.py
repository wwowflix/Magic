import importlib, types

def test_import_scripts_phase15_module_J_15J_community_reaction_comparator_READY():
    mod = importlib.import_module("scripts.phase15.module_J.15J_community_reaction_comparator_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
