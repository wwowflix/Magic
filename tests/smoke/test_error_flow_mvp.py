from __future__ import annotations

import scripts.error_flow_mvp as err


def test_imports_and_classes_exist() -> None:
    assert hasattr(err, "MagicError")
    assert hasattr(err, "DataFlowError")
    assert hasattr(err, "AiFlowError")
    assert hasattr(err, "FileFlowError")
    assert hasattr(err, "ErrorReport")
    assert hasattr(err, "ensure_non_empty")
    assert hasattr(err, "log_error")


def test_error_hierarchy() -> None:
    assert issubclass(err.DataFlowError, err.MagicError)
    assert issubclass(err.AiFlowError, err.MagicError)
    assert issubclass(err.FileFlowError, err.MagicError)


def test_ensure_non_empty_pass() -> None:
    out = err.ensure_non_empty("demo", field="name")
    assert out == "demo"


def test_ensure_non_empty_raises_on_empty() -> None:
    try:
        err.ensure_non_empty("   ", field="name")
    except err.DataFlowError as exc:
        msg = str(exc)
        assert "cannot be empty" in msg
    else:
        raise AssertionError("Expected DataFlowError for empty value")


def test_log_error_shape() -> None:
    exc = err.AiFlowError("model timeout")
    report = err.log_error(exc, kind="ai_flow", context={"module": "AI101"})

    assert isinstance(report, err.ErrorReport)
    assert report.kind == "ai_flow"
    assert "timeout" in report.message
    assert report.context["module"] == "AI101"
    assert report.context["exc_type"] == "AiFlowError"
