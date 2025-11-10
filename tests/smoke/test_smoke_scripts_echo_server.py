import importlib, types


def test_import_scripts_echo_server():
    mod = importlib.import_module("scripts.echo-server")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
