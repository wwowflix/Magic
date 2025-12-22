# ---- MAGIC SHIM: _serialization ----
"""
MAGIC stub for cryptography-like serialization classes.
Prevents ImportError from cryptography.hazmat.primitives.serialization.
"""

class Encoding:
    PEM = "PEM"
    DER = "DER"

class PrivateFormat:
    PKCS8 = "PKCS8"

class PublicFormat:
    SubjectPublicKeyInfo = "SubjectPublicKeyInfo"

class NoEncryption:
    def __repr__(self):
        return "<NoEncryption>"

def load_pem_private_key(data, password=None, backend=None):
    return None  # shim

def load_pem_public_key(data, backend=None):
    return None  # shim

# ---- END MAGIC SHIM ----
