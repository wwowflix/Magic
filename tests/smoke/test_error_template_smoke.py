from __future__ import annotations

from pathlib import Path


def test_error_template_file_exists() -> None:
    path = Path("templates") / "template_error_ops.j2"
    assert path.exists(), "template_error_ops.j2 should exist"


def test_error_template_has_placeholders() -> None:
    path = Path("templates") / "template_error_ops.j2"
    text = path.read_text(encoding="utf-8")

    # Check for a few key markers so we know the layout is intact
    assert "{{ class_name }}" in text
    assert "{{ error_code }}" in text
    assert "MAGIC Week 1 – Error Module Template" in text
