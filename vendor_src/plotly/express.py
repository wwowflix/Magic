"""
Minimal shim for plotly.express used only for import-time tests.

Any px.*(...) call will return a DummyFigure object with a no-op show
and update_layout, so vendored sample code can run without the real plotly.
"""

from typing import Any, Callable

class DummyFigure:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs

    def update_layout(self, *args: Any, **kwargs: Any) -> 'DummyFigure':
        return self

    def show(self, *args: Any, **kwargs: Any) -> None:
        pass

def _make_figure(*args: Any, **kwargs: Any) -> DummyFigure:
    return DummyFigure(*args, **kwargs)

def line(*args: Any, **kwargs: Any) -> DummyFigure:
    return _make_figure(*args, **kwargs)

def scatter(*args: Any, **kwargs: Any) -> DummyFigure:
    return _make_figure(*args, **kwargs)

def bar(*args: Any, **kwargs: Any) -> DummyFigure:
    return _make_figure(*args, **kwargs)

def histogram(*args: Any, **kwargs: Any) -> DummyFigure:
    return _make_figure(*args, **kwargs)

def area(*args: Any, **kwargs: Any) -> DummyFigure:
    return _make_figure(*args, **kwargs)

def pie(*args: Any, **kwargs: Any) -> DummyFigure:
    return _make_figure(*args, **kwargs)

def __getattr__(name: str) -> Callable[..., DummyFigure]:
    return _make_figure
