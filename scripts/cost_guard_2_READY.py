# -*- coding: utf-8 -*-
"""Cost guard placeholder: enforce daily API spend cap."""
from __future__ import annotations

MAX_DAILY_SPEND: float = 5.0  # dollars

def format_cap(cap: float) -> str:
    return f"Daily API spend is capped at ${cap:.2f}"

if __name__ == "__main__":
    print(format_cap(MAX_DAILY_SPEND))
