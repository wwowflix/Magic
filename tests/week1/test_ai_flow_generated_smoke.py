from importlib import import_module


MODULE_IDS = ["AI101", "AI102", "AI103", "AI104", "AI105"]


def _import_module(mid: str):
    return import_module(f"tools.mvp.ai_flow_{mid}")


def test_generated_ai_flows_import_and_run_main(capsys):
    """
    Light smoke:
    - Each generated module imports
    - main() runs without raising
    - prints a line containing [AUTO-AI]
    """
    for mid in MODULE_IDS:
        mod = _import_module(mid)
        assert hasattr(mod, "run_ai")
        assert hasattr(mod, "main")

        mod.main()
        captured = capsys.readouterr()
        assert "[AUTO-AI]" in captured.out
