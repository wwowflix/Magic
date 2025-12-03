from __future__ import annotations

import scripts.flow_registry as reg


def test_registry_lists_data_modules():
    data = reg.list_data_modules()
    assert isinstance(data, list)
    ids = {m["module_id"] for m in data}
    assert ids == {"DF101", "DF102", "DF103", "DF104", "DF105"}


def test_registry_lists_ai_modules():
    items = reg.list_ai_modules()
    assert isinstance(items, list)
    ids = {m["module_id"] for m in items}
    assert ids == {"AI101", "AI102", "AI103", "AI104", "AI105"}


def test_registry_lists_all_modules():
    all_items = reg.list_all_modules()
    ids = {m["module_id"] for m in all_items}
    # 5 data + 5 ai = 10 total
    assert ids == {
        "DF101",
        "DF102",
        "DF103",
        "DF104",
        "DF105",
        "AI101",
        "AI102",
        "AI103",
        "AI104",
        "AI105",
    }
