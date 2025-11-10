"""MAGIC shim: minimal stub for pycparser-style _ast_gen.

This only provides ASTCodeGenerator so that importing
`scripts._build_tables` in smoke tests succeeds without running any
code generation.
"""


class ASTCodeGenerator:  # pragma: no cover
    def __init__(self, *args, **kwargs):
        pass

    def generate(self, *args, **kwargs):
        # no-op: in our tests we only need the class to exist
        return ""
