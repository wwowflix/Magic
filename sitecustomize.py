import builtins, sys
_BLOCK = {"_dtype","_iotools","_methods","_type_aliases","_ufunc_config","core_4","defchararray","fromnumeric","function_base_2","generate_numpy_api","memmap","misc_util","npyio","numeric","overrides","records","setup_3","utils_4","_multiarray_umath","__config__","__config___2"}
_real_import = builtins.__import__

def _guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
    # Always allow real NumPy
    if name.startswith("numpy."):
        return _real_import(name, globals, locals, fromlist, level)
    # Guard project modules that mimic NumPy internals
    if name.startswith("scripts."):
        base = name.rsplit(".", 1)[-1]
        if base in _BLOCK:
            raise ImportError(f"Blocked import of shadowed project module '{name}'. Reserved name.")
    return _real_import(name, globals, locals, fromlist, level)

if not getattr(sys, "_magic_import_guard_installed", False):
    builtins.__import__ = _guarded_import
    sys._magic_import_guard_installed = True