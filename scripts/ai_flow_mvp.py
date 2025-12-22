from __future__ import annotations

"""
MAGIC Week 1 – AI Flow MVP (W1D2-1)

Simulated AI pipeline:
- deterministic (for tests)
- no external API calls
- always returns normalized structure
"""

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class AIResponse:
    module_id: str
    prompt: str
    result: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "module_id": self.module_id,
            "prompt": self.prompt,
            "result": self.result,
        }


def _dummy_llm(prompt: str) -> str:
    return f"[dummy-response] {prompt}"


def run_ai_pipeline(module_id: str, prompt: str) -> Dict[str, Any]:
    output = _dummy_llm(prompt)
    response = AIResponse(
        module_id=module_id,
        prompt=prompt,
        result=output,
    )
    return response.to_dict()
