"""
Tiny local shim for the 'plotly' package for Week 0 import tests.
We only expose 'express' with dummy constructors so that
import plotly.express as px works in vendored scripts.
"""
from . import express
__all__ = ["express"]
