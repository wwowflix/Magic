import importlib, pytest


@pytest.mark.parametrize(
    "mod",
    [
        "scripts._asarray",
        "scripts.multiarray",
        "scripts._add_newdocs",
        "scripts._add_newdocs_scalars",
    ],
)
def test_allowed_shims_import(mod):
    importlib.import_module(mod)


@pytest.mark.parametrize(
    "mod",
    [
        "scripts.overrides",
        "scripts.fromnumeric",
        "scripts._methods",
        "scripts._dtype",
        "scripts._type_aliases",
        "scripts._ufunc_config",
    ],
)
def test_forbidden_shadow_names_blocked(mod):
    with pytest.raises(ImportError):
        importlib.import_module(mod)
