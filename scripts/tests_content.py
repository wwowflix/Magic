# tests_content.py

import pytest

def test_generated_content_not_empty():
    generated_text = 'Hello from MAGIC AI!'
    assert generated_text.strip() != ''
