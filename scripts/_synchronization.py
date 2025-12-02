# ---- MAGIC SHIM: _synchronization ----
"""
MAGIC stub for trio-like synchronization primitives.
Provides minimal no-op versions of core sync objects.
"""

class Lock:
    def __init__(self):
        pass
    async def acquire(self): return True
    async def release(self): return None

class Event:
    def __init__(self):
        self._flag = False
    async def wait(self): return True
    def set(self): self._flag = True

class CapacityLimiter:
    def __init__(self, max_value=1):
        self.max_value = max_value
    def acquire(self): return True
    def release(self): return None

# ---- END MAGIC SHIM ----
