import importlib, types


def test_import_scripts_phase00_INBOX_C_B_L_C__617970A2_617970A2():
    mod = importlib.import_module("scripts.phase00.INBOX.C_B_L_C__617970A2_617970A2")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
