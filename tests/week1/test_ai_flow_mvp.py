from tools.mvp.ai_flow_mvp import run_ai, AIResponse


def test_ai_flow_basic():
    resp = run_ai("magic")
    assert isinstance(resp, AIResponse)
    assert resp.result == "MAGIC"
    assert resp.meta["len"] == 5
