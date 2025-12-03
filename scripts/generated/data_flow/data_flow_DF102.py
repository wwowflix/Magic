from __future__ import annotations

'''MAGIC Week 1 Auto-generated data flow module DF102.'''

from typing import Any, Dict
from scripts.data_flow_mvp import DataModule


def build_module() -> DataModule:
    '''Return a configured DataModule instance for DF102.'''
    return DataModule(
        module_id="DF102",
        name="Auto Data Module 102",
        category="data_flow",
        phase=2,
        enabled=True,
        tags=["week1", "auto"],
    )


def as_dict() -> Dict[str, Any]:
    '''Return this module definition as a plain dict.'''
    mod = build_module()
    return mod.to_dict()
