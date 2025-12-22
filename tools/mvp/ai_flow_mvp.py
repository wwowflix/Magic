from __future__ import annotations
from dataclasses import dataclass, asdict
import json
from pathlib import Path
from typing import Dict, Any

OUTPUT = Path(__file__).resolve().parents[1] / "outputs" / "week1_ai_output.json"


@dataclass
class AIResponse:
    prompt: str
    result: str
    meta: Dict[str, Any]


def run_ai(prompt: str = "hello-world") -> AIResponse:
    """
    Week1 AI flow MVP.
    Simulated AI  returns uppercase string + metadata
    """
    return AIResponse(
        prompt=prompt,
        result=prompt.upper(),
        meta={"mvp": True, "len": len(prompt)},
    )


def save_output(resp: AIResponse) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(asdict(resp), indent=2), encoding="utf-8")


def main():
    resp = run_ai("test-run")
    save_output(resp)
    print("[W1-AI] OK ", resp.result, "meta:", resp.meta)


if __name__ == "__main__":
    main()
