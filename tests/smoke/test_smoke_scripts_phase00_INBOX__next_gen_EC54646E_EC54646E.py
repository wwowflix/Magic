import importlib, types


def test_import_scripts_phase00_INBOX__next_gen_EC54646E_EC54646E():
    mod = importlib.import_module("scripts.phase00.INBOX._next_gen_EC54646E_EC54646E")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
