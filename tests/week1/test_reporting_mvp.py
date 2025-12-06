from tools.mvp.reporting_mvp import build_report, RunReport


def test_reporting_mvp_basic() -> None:
    report = build_report(total_flows=5, successful=3, failed=2)
    assert isinstance(report, RunReport)
    assert report.total_flows == 5
    assert report.successful == 3
    assert report.failed == 2
    assert report.meta.get("mvp") is True
