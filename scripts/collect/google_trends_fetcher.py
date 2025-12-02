from __future__ import annotations

"""
Week 0 stub for `scripts.collect.google_trends_fetcher`.

The original module calls out to Google Trends and requires command-line
arguments like `--keywords`. For MAGIC Week 0 smoke-import tests we only
need this module to import cleanly and for `main()` to be callable
without raising SystemExit.
"""

from typing import Any, Dict, List, Optional


def fetch_google_trends(
    keywords: List[str],
    regions: Optional[List[str]] = None,
    timeframe: str = "today 7-d",
) -> Dict[str, Any]:
    """
    Stubbed Google Trends fetcher.

    Returns a dummy payload describing what would have been requested.
    No real network calls are performed.
    """
    return {
        "keywords": list(keywords),
        "regions": list(regions or []),
        "timeframe": timeframe,
        "data": [],
    }


def main(argv: Optional[List[str]] = None) -> int:
    """
    Minimal CLI entry point stub.

    In Week 0 this does nothing and always returns success so that the
    smoke test can call `mod.main()` without needing CLI args.
    """
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
