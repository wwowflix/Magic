from importlib import import_module


MODULE_IDS = [
    "DF101",
    "DF102",
    "DF103",
    "DF104",
    "DF105",
]


def _import_module(module_id: str):
    mod_name = f"tools.mvp.data_flow_{module_id}"
    return import_module(mod_name)


def test_generated_data_flows_import_and_run_main(capsys):
    """
    Light smoke:
    - Each generated module imports
    - main() runs without raising
    - prints a line containing [AUTO-DATA]
    """
    for mid in MODULE_IDS:
        mod = _import_module(mid)
        assert hasattr(mod, "main"), f"{mid} has no main()"

        # Run main and capture output
        mod.main()
        captured = capsys.readouterr()
        assert "[AUTO-DATA]" in captured.out
