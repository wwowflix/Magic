import importlib, types


def test_import_scripts_phase00_INBOX_BitmapGlyphMetrics_F607063D_F607063D():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.BitmapGlyphMetrics_F607063D_F607063D"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
