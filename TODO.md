# MAGIC – Smoke Import Stabilization TODO

## Status: in progress

- [x] Add scripts\__init__.py
- [x] Shim magic_logging module
- [x] Shim magic_functools (wraps etc.)
- [x] Shim magic_typing
- [x] Fix scripts\B_A_S_E_ KeyError by providing full otBase implementation
- [x] Remove stray/duplicated parens in Blocks.py imports
- [x] Replace deprecated pandas cast import; add soft_convert_objects shim
- [x] Make PandasArray import version-safe
- [x] Make SparseDtype import version-safe
- [ ] Make NumpyBlock base version-safe (CURRENT STEP)
- [ ] Re-run 	ests\smoke\test_smoke_scripts_Blocks.py
- [ ] Run full smoke: pytest -q tests\smoke -x
- [ ] Patch any remaining pandas-internal API drifts the tests reveal

### How close are we?
We’re very close on scripts.Blocks: most import-time issues are patched. The current blocker is a single base class name change (NumpyBlock), which the patch above addresses. After that, we’ll rerun and handle any remaining stragglers (if any).
