"""
MAGIC Week 1 – Generated Data Flow Modules smoketest (W1D1-4)

Covers:
- Import safety for scripts.generated.data_flow.data_flow_DF101..DF105
- Basic contract: build_module() and as_dict() shape
"""

import importlib


MODULE_IDS = [
    "DF101",
    "DF102",
    "DF103",
    "DF104",
    "DF105",
]


def _import_module(module_id: str):
    mod_name = f"scripts.generated.data_flow.data_flow_{module_id}"
    return importlib.import_module(mod_name)


def test_generated_modules_import_and_shape():
    for mid in MODULE_IDS:
        mod = _import_module(mid)

        # Must expose factory + dict helper
        assert hasattr(mod, "build_module"), f"{mid} missing build_module()"
        assert hasattr(mod, "as_dict"), f"{mid} missing as_dict()"

        dm = mod.build_module()
        data = mod.as_dict()

        # Basic type + keys check
        assert isinstance(data, dict)
        assert data.get("module_id") == mid
        assert "name" in data
        assert "category" in data
        assert "phase" in data
        assert isinstance(data.get("tags"), list)
