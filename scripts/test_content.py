# -*- coding: utf-8 -*-
import pytest
import json

# Example AI content generator stub
def example_ai_generator():
    # Returns AI generated text output (string)
    return 'This is AI-generated text.'

def test_ai_text_not_empty():
    text = example_ai_generator()
    assert isinstance(text, str), 'AI output should be a string'
    assert text.strip() != '', 'AI output should not be empty'

def test_ai_output_valid_json():
    # Simulate AI outputting JSON string
    json_output = '{\"key\": \"value\"}'
    try:
        parsed = json.loads(json_output)
        assert isinstance(parsed, dict), 'AI JSON output should parse to dict'
    except json.JSONDecodeError:
        pytest.fail('AI output is not valid JSON')

def test_ai_output_no_offensive_content():
    # Simulate offensive content check
    text = example_ai_generator()
    offensive_words = ['badword1', 'badword2']
    assert not any(word in text.lower() for word in offensive_words), 'AI output contains offensive words'



