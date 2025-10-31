import importlib
import types


def test_import_scripts_pkcs7():
    mod = importlib.import_module("scripts.pkcs7")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
