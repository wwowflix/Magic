# ---- MAGIC SHIM: _pickle ----
"""
MAGIC stub for vendored _pickle variants.

Goal: Ensure clean import for scripts that reference a CPython-internal module.
This file provides a thin wrapper around Python's builtin pickle.
"""

import pickle as _pickle

# Re-export everything from builtin pickle
from pickle import *

# Minimal stand-ins for internal C-accelerated APIs
def dump(obj, file, protocol=None):
    return _pickle.dump(obj, file, protocol=protocol)

def dumps(obj, protocol=None):
    return _pickle.dumps(obj, protocol=protocol)

def load(file):
    return _pickle.load(file)

def loads(data):
    return _pickle.loads(data)

# Provide minimal PickleBuffer shim
class PickleBuffer(bytes):
    """Fallback shim for PickleBuffer."""
    pass

# ---- END MAGIC SHIM ----
