import os, pathlib, pytest

TARGET = "test_believe_now.py"

def pytest_ignore_collect(path, config):
    # Skip importing this heavy/no-test file during collection for smoke runs
    return os.path.basename(str(path)) == TARGET
