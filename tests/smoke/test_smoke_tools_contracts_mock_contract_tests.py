import importlib
import types


def test_import_tools_contracts_mock_contract_tests():
    mod = importlib.import_module("tools.contracts.mock_contract_tests")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
