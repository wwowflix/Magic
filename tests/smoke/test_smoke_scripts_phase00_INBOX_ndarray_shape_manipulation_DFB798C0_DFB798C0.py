import importlib, types


def test_import_scripts_phase00_INBOX_ndarray_shape_manipulation_DFB798C0_DFB798C0():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.ndarray_shape_manipulation_DFB798C0_DFB798C0"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
