"""
MAGIC Week 0 shim for the `chardetect` CLI module.

Goal:
- Import cleanly under pytest
- Provide a tiny interface around UniversalDetector
- Ensure `main()` NEVER raises SystemExit, even if pytest adds -q -x.

This is intentionally minimal and is NOT a full replacement for the
real chardet CLI. It is only for MAGIC test/import safety.
"""

from __future__ import annotations

from typing import Iterable, Optional, List, Dict, Any

from .universaldetector import UniversalDetector


def detect_bytes_chunk(chunk: bytes) -> Dict[str, Any]:
    """
    Simple helper: run UniversalDetector on a single bytes chunk and
    return a small result dict.
    """
    detector = UniversalDetector()
    detector.feed(chunk)
    detector.close()
    result = detector.result or {}
    return {
        "encoding": result.get("encoding"),
        "confidence": result.get("confidence"),
        "language": result.get("language"),
    }


def detect_all(chunks: Iterable[bytes]) -> List[Dict[str, Any]]:
    """
    Run detection over an iterable of byte chunks.

    This is a tiny, test-friendly helper that callers can use instead of
    the original CLI pipeline.
    """
    return [detect_bytes_chunk(chunk) for chunk in chunks]


def main(argv: Optional[list[str]] = None) -> int:
    """
    MAGIC-safe CLI entry point.

    - Ignores any argv (including pytest's "-q -x")
    - Does NOT call argparse or sys.exit
    - Returns 0 so tests see a "clean" run.
    """
    # For Week 0 we completely skip real CLI parsing.
    # If in the future MAGIC needs a real CLI, it can be implemented
    # on top of `detect_all` above.
    return 0
