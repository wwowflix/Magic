import importlib, types


def test_import_scripts_phase00_INBOX_mcmc_09233C32_09233C32():
    mod = importlib.import_module("scripts.phase00.INBOX.mcmc_09233C32_09233C32")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
