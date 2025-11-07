import importlib, types


def test_import_scripts_phase00_INBOX_structure_tree_FF22F40D_FF22F40D():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.structure_tree_FF22F40D_FF22F40D"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
