from __future__ import annotations
import importlib


def test_ai_flow_imports():
    mod = importlib.import_module("scripts.ai_flow_mvp")
    assert hasattr(mod, "run_ai_pipeline")


def test_ai_pipeline_output_shape():
    mod = importlib.import_module("scripts.ai_flow_mvp")
    out = mod.run_ai_pipeline("AI001", "hello world")

    assert isinstance(out, dict)
    assert out["module_id"] == "AI001"
    assert out["prompt"] == "hello world"
    assert out["result"].startswith("[dummy-response]")
