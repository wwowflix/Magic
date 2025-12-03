from __future__ import annotations
import importlib

MODULE_IDS = ["AI101","AI102","AI103","AI104","AI105"]

def test_generated_ai_modules_import():
    for mid in MODULE_IDS:
        mod = importlib.import_module(f"scripts.generated.ai_flow.ai_flow_{mid}")
        assert hasattr(mod, "run_ai_pipeline")

def test_ai_generated_output_shape():
    for mid in MODULE_IDS:
        mod = importlib.import_module(f"scripts.generated.ai_flow.ai_flow_{mid}")
        out = mod.run_ai_pipeline(mid, "hello ai")

        assert isinstance(out, dict)
        assert out["module_id"] == mid
        assert out["prompt"] == "hello ai"
        assert out["result"].startswith("[dummy-response]")
