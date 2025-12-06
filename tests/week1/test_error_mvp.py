from tools.mvp.error_mvp import collect_errors, summarize, ErrorRecord


def test_error_flow_basic() -> None:
    errors = collect_errors()
    assert isinstance(errors, list)
    assert errors

    first = errors[0]
    assert isinstance(first, ErrorRecord)

    summary = summarize(errors)
    assert summary["total"] == len(errors)
    assert "high" in summary
