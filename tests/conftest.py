# -*- coding: utf-8 -*-
import sys
from pathlib import Path

# Ensure project root is importable so "import tools" works in CI
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
