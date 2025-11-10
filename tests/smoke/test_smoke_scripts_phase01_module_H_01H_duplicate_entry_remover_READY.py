import importlib, types


def test_import_scripts_phase01_module_H_01H_duplicate_entry_remover_READY():
    mod = importlib.import_module(
        "scripts.phase01.module_H.01H_duplicate_entry_remover_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
