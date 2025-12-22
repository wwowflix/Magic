from __future__ import annotations

import importlib
from typing import Any, Dict, List


# Week 1 registry of generated flows
DATA_MODULE_IDS: List[str] = [
    "DF101",
    "DF102",
    "DF103",
    "DF104",
    "DF105",
]

AI_MODULE_IDS: List[str] = [
    "AI101",
    "AI102",
    "AI103",
    "AI104",
    "AI105",
]


def _load_data_module_dict(module_id: str) -> Dict[str, Any]:
    """
    Import scripts.generated.data_flow.data_flow_<id> and return its as_dict().
    """
    mod_name = f"scripts.generated.data_flow.data_flow_{module_id}"
    mod = importlib.import_module(mod_name)

    if not hasattr(mod, "as_dict"):
        raise AttributeError(f"{mod_name} is missing as_dict()")

    data = mod.as_dict()
    if not isinstance(data, dict):
        raise TypeError(f"{mod_name}.as_dict() did not return a dict")

    return data


def _load_ai_module_dict(module_id: str) -> Dict[str, Any]:
    """
    Import scripts.generated.ai_flow.ai_flow_<id> and return its as_dict().
    """
    mod_name = f"scripts.generated.ai_flow.ai_flow_{module_id}"
    mod = importlib.import_module(mod_name)

    if not hasattr(mod, "as_dict"):
        raise AttributeError(f"{mod_name} is missing as_dict()")

    data = mod.as_dict()
    if not isinstance(data, dict):
        raise TypeError(f"{mod_name}.as_dict() did not return a dict")

    return data


def list_data_modules() -> List[Dict[str, Any]]:
    """
    Return a list of dicts for all Week 1 data-flow modules.
    """
    return [_load_data_module_dict(mid) for mid in DATA_MODULE_IDS]


def list_ai_modules() -> List[Dict[str, Any]]:
    """
    Return a list of dicts for all Week 1 AI-flow modules.
    """
    return [_load_ai_module_dict(mid) for mid in AI_MODULE_IDS]


def list_all_modules() -> List[Dict[str, Any]]:
    """
    Return a combined list of all data + AI flow module dicts.
    """
    items: List[Dict[str, Any]] = []
    items.extend(list_data_modules())
    items.extend(list_ai_modules())
    return items
