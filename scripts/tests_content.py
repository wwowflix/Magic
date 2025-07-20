# -*- coding: utf-8 -*-
import pytest
import json
import os

def test_generated_content_not_empty():
    content_path = 'path/to/ai_outputs/sample_output.json'
    assert os.path.exists(content_path), 'Output file missing'
    with open(content_path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert len(content) > 0, 'Generated content should not be empty'

def test_json_structure_valid():
    content_path = 'path/to/ai_outputs/sample_output.json'
    with open(content_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert isinstance(data, dict), 'Content JSON root should be an object'
    assert 'title' in data, 'Content JSON must have a title field'
    assert 'body' in data, 'Content JSON must have a body field'



