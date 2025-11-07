import importlib, types


def test_import_scripts_phase00_INBOX__n_a_m_e_2D8C9228_2D8C9228():
    mod = importlib.import_module("scripts.phase00.INBOX._n_a_m_e_2D8C9228_2D8C9228")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
