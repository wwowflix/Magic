from __future__ import annotations

"""
MAGIC shim for scripts.benchmark.

The original module used cu2qu, fontTools, and cython to run curve conversion
benchmarks. For MAGIC Week 0 we only need:

- the module to import cleanly
- a couple of lightweight placeholders

No real benchmarking or heavy dependencies are required here.
"""

from dataclasses import dataclass
from typing import Any, Iterable, List


@dataclass
class BenchmarkResult:
    """Minimal container for a benchmark result."""

    name: str
    iterations: int
    seconds: float


def run_all_benchmarks() -> List[BenchmarkResult]:
    """
    Return an empty list of benchmark results.

    This keeps the public shape simple and safe for callers that just expect
    an iterable of results.
    """
    return []


def main(args: Iterable[Any] | None = None) -> int:
    """
    Optional entrypoint-style helper.

    Prints any benchmark results if present, then returns an exit code.
    In this MAGIC shim, the list is empty, so this is effectively a no-op.
    """
    for result in run_all_benchmarks():
        print(f"{result.name}: {result.iterations} in {result.seconds:.3f}s")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
