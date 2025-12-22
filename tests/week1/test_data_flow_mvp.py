from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import json
import pytest

from tools.mvp.data_flow_mvp import NormalizedRecord, normalize, load_raw


def test_normalize_basic() -> None:
    raw: Dict[str, Any] = {
        "id": "test-1",
        "source": "unit-test",
        "status": "ok",
        "foo": 123,
    }
    rec = normalize(raw)
    assert isinstance(rec, NormalizedRecord)
    assert rec.id == "test-1"
    assert rec.source == "unit-test"
    assert rec.status == "ok"
    assert rec.payload["foo"] == 123


def test_load_raw_returns_reasonable_dict() -> None:
    data = load_raw()
    assert isinstance(data, dict)
    assert "id" in data
    assert "source" in data
    assert "status" in data


@pytest.mark.skipif(
    pytest.importorskip("jinja2", reason="jinja2 not installed") is None,
    reason="jinja2 not available",
)
def test_data_flow_template_renders() -> None:
    # If our Week-0/Week-1 shim is not ready, do not hard-fail Week-1 MVP.
    try:
        from jinja2 import Environment, FileSystemLoader  # type: ignore[import]
    except ImportError:
        pytest.skip("jinja2 shim not available yet")

    env = Environment()
    template = env.from_string(
        '{"id": "{{ record.id }}", "source": "{{ record.source }}", "status": "{{ record.status }}"}'
    )

    sample_record = NormalizedRecord(
        id="tmpl-1",
        source="template-test",
        status="ok",
        payload={"extra": {"note": "template smoke"}},
    )

    rendered = template.render(record=sample_record)

    assert '"id": "tmpl-1"' in rendered
    assert '"source": "template-test"' in rendered
    assert '"status": "ok"' in rendered
