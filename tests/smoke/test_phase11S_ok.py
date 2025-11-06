import pathlib
from ._smoke_utils import run_target

MOD = pathlib.Path('scripts/phase11/module_S')
targets = sorted(MOD.rglob('*_READY.py'))

def test_phase11_ok():
    assert targets, f"No READY scripts found under {MOD}"
    for t in targets:
        run_target(t)
