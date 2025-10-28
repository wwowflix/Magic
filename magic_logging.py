from logging import *
import logging as _pylogging

# give tests sane defaults if no handlers were configured
if not _pylogging.getLogger().handlers:
    _pylogging.basicConfig(level=_pylogging.INFO)
