# -*- coding: utf-8 -*-
import pytest
from ai_content import AIContentGenerator

def test_generate_with_valid_prompt():
    ai = AIContentGenerator()
    result = ai.generate("Tell me about AI.")
    assert isinstance(result, str)
    assert "AI Response" in result

def test_generate_with_empty_prompt():
    ai = AIContentGenerator()
    result = ai.generate("")
    assert result == "Error: Empty prompt."



