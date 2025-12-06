"""
MAGIC WEEK-1 — AI Flow Auto-Generated Module
ID: AI105
Seed: spark
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
import json
from pathlib import Path
import random
from typing import List


OUTPUT = Path(__file__).resolve().parents[2] / "outputs" / "week1" / "ai" / "ai_AI105.json"


@dataclass
class AIRecord:
    module: str
    seed: str
    score: float
    tags: List[str]


def run_ai() -> AIRecord:
    """
    Very small fake AI flow for Week-1 MVP auto-gen.

    - score: random float 0.4–0.99
    - tags: ["auto", seed, "week1"]
    """
    score = round(random.uniform(0.40, 0.99), 3)
    tags = ["auto", "spark", "week1"]
    return AIRecord(
        module="AI105",
        seed="spark",
        score=score,
        tags=tags,
    )


def save(rec: AIRecord) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(asdict(rec), indent=2), encoding="utf-8")


def main() -> None:
    rec = run_ai()
    save(rec)
    print("[AUTO-AI]", rec.score, rec.tags)


if __name__ == "__main__":
    main()
