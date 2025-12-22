"""
MAGIC Week 0: safe stub for data_3 (VegaFusion data transformer).

Goal:
- Let "import scripts.data_3" succeed.
- Provide vegafusion_data_transformer with a tiny, safe interface.
- Avoid importing altair or any heavy dependencies.
"""

from __future__ import annotations

from typing import Any


class _VegaFusionDataTransformer:
    """
    Minimal stand-in for altair.utils._vegafusion_data.vegafusion_data_transformer.

    In real Altair this would:
    - Integrate with VegaFusion for server-side transforms.
    - Potentially rewrite data specs.

    For Week 0 we:
    - Accept any data.
    - Return it unchanged.
    """

    def __init__(self) -> None:
        # Flag kept only so future code can inspect it if needed.
        self.enabled: bool = False

    def __call__(self, data: Any, *args: Any, **kwargs: Any) -> Any:
        # Week 0: no transformation, just pass-through.
        return data


# Global transformer instance (what data_3 normally exposes)
vegafusion_data_transformer = _VegaFusionDataTransformer()

__all__ = ["vegafusion_data_transformer"]
