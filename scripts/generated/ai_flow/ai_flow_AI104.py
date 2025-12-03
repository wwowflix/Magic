{#
  MAGIC Week 1 - AI Flow Module Template (W1D2-2)

  This template is used by the auto-writer to generate AI Flow
  modules that describe how to call run_ai_pipeline in a structured way.
#}
from __future__ import annotations

"""
MAGIC Auto-Generated AI Flow Module

Generated from: template_ai_flow.j2
Week: 1
Stage: 2.2 - AI Flow MVP
"""

from typing import Any, Dict
from scripts.ai_flow_mvp import run_ai_pipeline


def build_ai_config() -> Dict[str, Any]:
    """
    Return a simple config dict describing this AI flow module.
    The auto-writer fills in these values.
    """
    return {
        "module_id": "AI104",
        "name": "Auto AI Module 104",
        "model_name": "{{ model_name | default('gpt-4.1-mini') }}",
        "max_tokens": {{ max_tokens | default(512) }},
        "temperature": {{ temperature | default(0.2) }},
        "tags": {{ tags | default(['week1', 'ai-flow']) }},
    }


def run(prompt: str) -> Dict[str, Any]:
    """
    Convenience wrapper around run_ai_pipeline using this module's config.
    """
    cfg = build_ai_config()
    return run_ai_pipeline(cfg["module_id"], prompt)
