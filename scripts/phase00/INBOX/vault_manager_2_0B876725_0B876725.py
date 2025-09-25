# -*- coding: utf-8 -*-
import json
import os


def _vault_paths():
    here = os.path.dirname(__file__)
    return [
        os.path.normpath(os.path.join(here, "..", "data", "vault.json")),
        os.path.normpath(os.path.join(here, "vault.json")),
    ]


def load_secret(key):
    for path in _vault_paths():
        if not os.path.exists(path):
            continue
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            continue
        if key in data:
            return data[key]
    raise KeyError(f"Secret '{key}' not found in any vault: {_vault_paths()}")


def save_secret(key, value):
    path = _vault_paths()[0]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    except:
        data = {}
    data[key] = value
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
